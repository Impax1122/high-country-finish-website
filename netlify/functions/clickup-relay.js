'use strict';

// ClickUp webhook relay: wakes the right bot for a ClickUp event.
//
// Routing (High Country Bot Rulebook, "How you get woken"):
// - Jobs list, status change          -> bot on duty for the NEW status
// - Jobs list, comment by Alex        -> bot on duty for the card's current status
// - HQ list, status change or comment by Alex
//                                     -> bot named in the card title, e.g. "[Billing] ..."
// - Bot comments ("[Name] ..."), new cards, field changes, other lists and
//   other events                      -> nobody (200, dropped)
//
// ClickUp suspends a webhook immediately on 401 or 410, so this function never
// returns either: bad signature 403, no secret configured 503, failed forward or
// a transient ClickUp lookup failure 502 (ClickUp retries). A bot without a
// configured wake target is dropped with 200 and logged.

const wake = require('../lib/wake');

const TAG = 'clickup-relay';
const HANDLED_EVENTS = new Set(['taskStatusUpdated', 'taskCommentPosted']);

function listKey(listId) {
  const id = listId == null ? '' : String(listId);
  if (id === wake.LISTS.jobs) return 'jobs';
  if (id === wake.LISTS.hq) return 'hq';
  return id ? 'other' : '';
}

function historyItem(payload, field) {
  const items = Array.isArray(payload.history_items) ? payload.history_items : [];
  return items.find((h) => h && h.field === field) || null;
}

function commentText(item) {
  const c = item && item.comment;
  if (!c) return '';
  if (typeof c.text_content === 'string') return c.text_content;
  if (Array.isArray(c.comment)) {
    return c.comment.map((p) => (p && typeof p.text === 'string' ? p.text : '')).join('');
  }
  return '';
}

function isoDate(ms) {
  const n = Number(ms);
  if (!Number.isFinite(n) || n <= 0) return new Date().toISOString();
  return new Date(n).toISOString();
}

function statusText(side) {
  if (!side) return null;
  if (typeof side === 'string') return side;
  return typeof side.status === 'string' ? side.status : null;
}

async function route(payload) {
  const event = payload && payload.event;
  if (!HANDLED_EVENTS.has(event)) return wake.drop(TAG, 'event_not_routed', `event=${String(event || 'none').slice(0, 40)}`);

  const taskId = typeof payload.task_id === 'string' ? payload.task_id : '';
  if (!taskId) return wake.drop(TAG, 'no_task_id', `event=${event}`);

  const item = historyItem(payload, event === 'taskStatusUpdated' ? 'status' : 'comment');
  if (!item) return wake.drop(TAG, 'no_history_item', `event=${event} task=${taskId}`);

  const fields = {
    source: 'clickup',
    event,
    task_id: taskId,
    task_url: wake.taskUrl(taskId),
    at: isoDate(item.date),
  };

  let text = '';
  if (event === 'taskCommentPosted') {
    text = commentText(item);
    // Drop bot comments before spending a ClickUp call on them.
    if (wake.isBotComment(text)) return wake.drop(TAG, 'bot_comment', `event=${event} task=${taskId}`);
    fields.comment_text = text;
  } else {
    fields.new_status = statusText(item.after);
    fields.previous_status = statusText(item.before);
  }

  let list = listKey(item.parent_id);
  let task = null;
  const detail = () => `event=${event} list=${list || 'unknown'} task=${taskId}`;

  // A Jobs status change needs no lookup. Everything else needs the card.
  const needsTask = !(event === 'taskStatusUpdated' && list === 'jobs');
  if (list === 'other') return wake.drop(TAG, 'other_list', detail());
  if (needsTask) {
    try {
      task = await wake.getTask(taskId);
    } catch (err) {
      if (err instanceof wake.LookupError && err.permanent) {
        return wake.drop(TAG, `lookup_${err.code.toLowerCase()}${err.statusCode ? `_${err.statusCode}` : ''}`, detail());
      }
      wake.log(TAG, 502, `${detail()} action=lookup_failed reason=${err && err.code ? String(err.code).toLowerCase() : 'error'}`);
      return wake.respond(502, { error: 'lookup failed' });
    }
    if (!list) list = listKey(task && task.list && task.list.id);
    fields.task_name = task && typeof task.name === 'string' ? task.name : null;
  }
  fields.list = list === 'jobs' || list === 'hq' ? list : null;

  if (list === 'jobs') {
    const status = event === 'taskStatusUpdated' ? fields.new_status : wake.taskStatus(task);
    if (event === 'taskCommentPosted') fields.new_status = status || null;
    const bot = wake.botForStatus(status);
    if (!bot) return wake.drop(TAG, wake.isKnownStatus(status) ? 'nobody_on_duty' : 'unknown_status', detail());
    return wake.wake(TAG, bot, fields, detail());
  }

  if (list === 'hq') {
    const bot = wake.botForHqTitle(fields.task_name);
    if (!bot) return wake.drop(TAG, 'no_bot_in_title', detail());
    if (event === 'taskCommentPosted') fields.new_status = wake.taskStatus(task) || null;
    return wake.wake(TAG, bot, fields, detail());
  }

  return wake.drop(TAG, 'other_list', detail());
}

function secrets() {
  return [process.env.CLICKUP_WEBHOOK_SECRET, process.env.CLICKUP_WEBHOOK_SECRET_JOBS].filter(wake.hasValue);
}

async function handle(event) {
  const method = String((event && event.httpMethod) || '').toUpperCase();
  if (method !== 'POST') {
    wake.log(TAG, 405, `method=${method || 'UNKNOWN'}`);
    return wake.respond(405, { error: 'method not allowed' }, { Allow: 'POST' });
  }

  if (wake.isPaused()) return wake.drop(TAG, 'paused');

  const keys = secrets();
  if (!keys.length) {
    wake.log(TAG, 503, 'not_configured');
    return wake.respond(503, { error: 'relay not configured' });
  }

  const body = wake.rawBody(event);
  const signature = wake.headerValue(event, 'x-signature');
  if (!keys.some((k) => wake.verifySignature(k, signature, body))) {
    wake.log(TAG, 403, 'bad_signature');
    return wake.respond(403, { error: 'forbidden' });
  }

  let payload;
  try {
    payload = JSON.parse(body.toString('utf8'));
  } catch (err) {
    return wake.drop(TAG, 'bad_json');
  }
  if (!payload || typeof payload !== 'object') return wake.drop(TAG, 'bad_json');
  return route(payload);
}

exports.handler = async function handler(event) {
  try {
    return await handle(event);
  } catch (err) {
    wake.log(TAG, 502, 'internal');
    return wake.respond(502, { error: 'relay failed' });
  }
};

exports.route = route;
exports.listKey = listKey;
exports.commentText = commentText;
