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
// Approved exception (not in the Oct 2 rulebook wake table):
// - Personal space (90149893204, To-dos list 901423191614):
//     taskTagUpdated where the tag `basecamp` is added, or
//     taskCommentPosted on a task that already carries that tag
//       -> Basecamp
//   Any other Personal-space event is dropped. Personal-space events never
//   wake an HC bot. If WAKE_BASECAMP_URL or WAKE_BASECAMP_AUTH is unset, the
//   event is dropped with 200 and a log line that contains no secrets.
//
// ClickUp suspends a webhook immediately on 401 or 410, so this function never
// returns either: bad signature 403, no secret configured 503, failed forward or
// a transient ClickUp lookup failure 502 (ClickUp retries). A bot without a
// configured wake target is dropped with 200 and logged.

const wake = require('../lib/wake');

const TAG = 'clickup-relay';
const HANDLED_EVENTS = new Set(['taskStatusUpdated', 'taskCommentPosted']);
const PERSONAL_EVENTS = new Set(['taskTagUpdated', 'taskCommentPosted']);
const BASECAMP_TAG = 'basecamp';

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

function payloadListId(payload) {
  if (payload && payload.list_id != null && payload.list_id !== '') return String(payload.list_id);
  const items = Array.isArray(payload && payload.history_items) ? payload.history_items : [];
  for (const h of items) {
    if (h && h.parent_id != null && h.parent_id !== '') return String(h.parent_id);
  }
  return '';
}

function payloadSpaceId(payload) {
  if (payload && payload.space_id != null && payload.space_id !== '') return String(payload.space_id);
  return '';
}

function isPersonalPayload(payload) {
  return wake.isPersonalSpace(payloadSpaceId(payload)) || wake.isPersonalList(payloadListId(payload));
}

function tagWasAdded(item, name) {
  const want = String(name).trim().toLowerCase();
  const after = wake.tagNames(item && item.after);
  const before = wake.tagNames(item && item.before);
  return after.includes(want) && !before.includes(want);
}

function historyHasTagNames(item) {
  return wake.tagNames(item && item.after).length > 0 || wake.tagNames(item && item.before).length > 0;
}

function payloadTagNames(payload) {
  if (!payload || typeof payload !== 'object') return [];
  if (payload.tags) return wake.tagNames(payload.tags);
  if (payload.task && payload.task.tags) return wake.tagNames(payload.task.tags);
  return [];
}

async function lookupTask(taskId, detail) {
  try {
    return { task: await wake.getTask(taskId) };
  } catch (err) {
    if (err instanceof wake.LookupError && err.permanent) {
      return { response: wake.drop(TAG, `lookup_${err.code.toLowerCase()}${err.statusCode ? `_${err.statusCode}` : ''}`, detail()) };
    }
    wake.log(TAG, 502, `${detail()} action=lookup_failed reason=${err && err.code ? String(err.code).toLowerCase() : 'error'}`);
    return { response: wake.respond(502, { error: 'lookup failed' }) };
  }
}

async function routePersonal(payload, prefetchedTask) {
  const event = payload && payload.event;
  const taskId = typeof payload.task_id === 'string' ? payload.task_id : '';
  const detail = () => `event=${String(event || 'none').slice(0, 40)} list=personal task=${taskId || 'none'}`;

  if (!taskId) return wake.drop(TAG, 'no_task_id', `event=${String(event || 'none').slice(0, 40)}`);
  if (!PERSONAL_EVENTS.has(event)) return wake.drop(TAG, 'event_not_routed', detail());

  const fields = {
    source: 'clickup',
    event,
    list: 'personal',
    task_id: taskId,
    task_url: wake.taskUrl(taskId),
  };

  if (event === 'taskCommentPosted') {
    const item = historyItem(payload, 'comment');
    if (!item) return wake.drop(TAG, 'no_history_item', detail());
    const text = commentText(item);
    // Drop bot comments before spending a ClickUp call on them.
    if (wake.isBotComment(text)) return wake.drop(TAG, 'bot_comment', detail());
    fields.comment_text = text;
    fields.at = isoDate(item.date);

    let task = prefetchedTask || null;
    const fromPayload = payloadTagNames(payload);
    if (!task && !fromPayload.length) {
      const looked = await lookupTask(taskId, detail);
      if (looked.response) return looked.response;
      task = looked.task;
    }
    if (task && typeof task.name === 'string') fields.task_name = task.name;
    const hasTag = fromPayload.includes(BASECAMP_TAG) || wake.taskHasTag(task, BASECAMP_TAG);
    if (!hasTag) return wake.drop(TAG, 'no_basecamp_tag', detail());
    return wake.wake(TAG, 'basecamp', fields, detail());
  }

  const item = historyItem(payload, 'tag') || historyItem(payload, 'tags');
  if (!item) return wake.drop(TAG, 'no_history_item', detail());
  fields.at = isoDate(item.date);

  if (tagWasAdded(item, BASECAMP_TAG)) {
    if (prefetchedTask && typeof prefetchedTask.name === 'string') fields.task_name = prefetchedTask.name;
    return wake.wake(TAG, 'basecamp', fields, detail());
  }

  // History item is present but has no tag names: fetch the task and wake
  // only if it now carries the basecamp tag.
  if (!historyHasTagNames(item)) {
    let task = prefetchedTask || null;
    if (!task) {
      const looked = await lookupTask(taskId, detail);
      if (looked.response) return looked.response;
      task = looked.task;
    }
    if (task && typeof task.name === 'string') fields.task_name = task.name;
    if (wake.taskHasTag(task, BASECAMP_TAG)) return wake.wake(TAG, 'basecamp', fields, detail());
  }

  return wake.drop(TAG, 'basecamp_tag_not_added', detail());
}

async function route(payload) {
  const event = payload && payload.event;

  // Personal-space events never enter the HC router.
  if (isPersonalPayload(payload)) return routePersonal(payload);

  // Tag updates on Jobs/HQ/other lists stay dropped, with no lookup. If the
  // location is missing, one GET decides whether this is Personal.
  if (event === 'taskTagUpdated') {
    const listId = payloadListId(payload);
    const spaceId = payloadSpaceId(payload);
    const taskId = typeof payload.task_id === 'string' ? payload.task_id : '';
    if (listId || spaceId || !taskId) {
      return wake.drop(TAG, 'event_not_routed', `event=${String(event || 'none').slice(0, 40)}${taskId ? ` task=${taskId}` : ''}`);
    }
    const detail = () => `event=${event} list=unknown task=${taskId}`;
    const looked = await lookupTask(taskId, detail);
    if (looked.response) return looked.response;
    if (wake.isPersonalTask(looked.task)) return routePersonal(payload, looked.task);
    return wake.drop(TAG, 'event_not_routed', `event=${event} list=${listKey(looked.task && looked.task.list && looked.task.list.id) || 'unknown'} task=${taskId}`);
  }

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
    // Missing parent_id on a Personal card: divert, never wake an HC bot.
    if (wake.isPersonalTask(task)) return routePersonal(payload, task);
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
  return [
    process.env.CLICKUP_WEBHOOK_SECRET,
    process.env.CLICKUP_WEBHOOK_SECRET_JOBS,
    process.env.CLICKUP_WEBHOOK_SECRET_PERSONAL,
  ].filter(wake.hasValue);
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
