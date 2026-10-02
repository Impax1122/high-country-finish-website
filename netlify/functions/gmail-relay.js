'use strict';

// Gmail relay: the email script (automation/gmail-wake) POSTs one small JSON
// event per new message, signed with X-Signature = hex HMAC-SHA256 of the body
// keyed with GMAIL_RELAY_SECRET. This function decides which bot to wake.
//
// Routing (High Country Bot Rulebook, "How you get woken"):
// - new_thread (not from Alex, not automated, not a receipt) -> Front Desk
// - reply on an existing thread -> the bot on duty for the job card whose
//   description holds that thread id; Front Desk if that job is Closed or Lost,
//   and Front Desk if no job card matches (so a reply on a thread that never
//   became a job still reaches the inbox owner). On hold -> nobody.
// - alex_sent (Alex sent a draft on a thread) -> that job's bot on duty;
//   no matching job, or nobody on duty -> dropped.
// - anything else -> dropped (200).
//
// 503 when GMAIL_RELAY_SECRET isn't set, 403 on a bad signature, 502 when the
// wake target or the ClickUp lookup fails, so the script retries next run.

const wake = require('../lib/wake');

const TAG = 'gmail-relay';
const KINDS = new Set(['new_thread', 'reply', 'alex_sent']);

function cleanId(value) {
  return typeof value === 'string' && /^[0-9a-fA-F]{6,32}$/.test(value.trim()) ? value.trim().toLowerCase() : '';
}

function str(value) {
  return typeof value === 'string' ? value : null;
}

async function route(payload) {
  const kind = payload && payload.kind;
  if (!KINDS.has(kind)) return wake.drop(TAG, 'kind_not_routed', `kind=${String(kind || 'none').slice(0, 40)}`);

  const threadId = cleanId(payload.thread_id);
  const messageId = cleanId(payload.message_id);
  if (!threadId) return wake.drop(TAG, 'bad_thread_id', `kind=${kind}`);

  const detail = `kind=${kind} thread=${threadId}`;
  const fields = {
    source: 'gmail',
    event: kind,
    thread_id: threadId,
    message_id: messageId || null,
    from: str(payload.from),
    subject: str(payload.subject),
    at: str(payload.at) || new Date().toISOString(),
  };

  if (kind === 'new_thread') return wake.wake(TAG, 'front_desk', fields, detail);

  let job;
  try {
    job = await wake.findJobByThread(threadId);
  } catch (err) {
    if (err instanceof wake.LookupError && err.permanent) {
      return wake.drop(TAG, `lookup_${err.code.toLowerCase()}${err.statusCode ? `_${err.statusCode}` : ''}`, detail);
    }
    wake.log(TAG, 502, `${detail} action=lookup_failed reason=${err && err.code ? String(err.code).toLowerCase() : 'error'}`);
    return wake.respond(502, { error: 'lookup failed' });
  }

  if (job) {
    fields.list = 'jobs';
    fields.task_id = job.id || null;
    fields.task_name = typeof job.name === 'string' ? job.name : null;
    fields.task_url = job.url || wake.taskUrl(job.id);
    fields.new_status = wake.taskStatus(job) || null;
  }
  const jobDetail = `${detail}${job ? ` task=${job.id}` : ' task=none'}`;

  if (kind === 'reply') {
    if (!job) return wake.wake(TAG, 'front_desk', fields, `${jobDetail} reason=no_job`);
    const status = wake.taskStatus(job);
    if (wake.isClosedOrLost(status)) return wake.wake(TAG, 'front_desk', fields, `${jobDetail} reason=closed_or_lost`);
    const bot = wake.botForStatus(status);
    if (!bot) return wake.drop(TAG, wake.isKnownStatus(status) ? 'nobody_on_duty' : 'unknown_status', jobDetail);
    return wake.wake(TAG, bot, fields, jobDetail);
  }

  // alex_sent
  if (!job) return wake.drop(TAG, 'no_job', jobDetail);
  const bot = wake.botForStatus(wake.taskStatus(job));
  if (!bot) return wake.drop(TAG, 'nobody_on_duty', jobDetail);
  return wake.wake(TAG, bot, fields, jobDetail);
}

async function handle(event) {
  const method = String((event && event.httpMethod) || '').toUpperCase();
  if (method !== 'POST') {
    wake.log(TAG, 405, `method=${method || 'UNKNOWN'}`);
    return wake.respond(405, { error: 'method not allowed' }, { Allow: 'POST' });
  }

  if (wake.isPaused()) return wake.drop(TAG, 'paused');

  const secret = process.env.GMAIL_RELAY_SECRET;
  if (!wake.hasValue(secret)) {
    wake.log(TAG, 503, 'not_configured');
    return wake.respond(503, { error: 'relay not configured' });
  }

  const body = wake.rawBody(event);
  if (!wake.verifySignature(secret, wake.headerValue(event, 'x-signature'), body)) {
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
