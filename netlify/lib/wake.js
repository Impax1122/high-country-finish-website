'use strict';

// Shared code for the bot wake-up relays (clickup-relay and gmail-relay).
//
// The routing table below is the "How you get woken" table of the High Country
// Bot Rulebook (Oct 2, 2026). Anything that isn't on it is dropped with 200.
//
// Safety rules carried over from the original relay (PR #3):
// - never return 401 or 410 (ClickUp suspends a webhook immediately on either);
// - a bad signature is 403, missing configuration is 503, a failed forward is 502;
// - never log request bodies, signatures, task names, comment text or env values.

const crypto = require('crypto');
const http = require('http');
const https = require('https');

const FORWARD_TIMEOUT_MS = 4000;
const LOOKUP_TIMEOUT_MS = 2500;
const LIST_PAGE_LIMIT = 10;

const LISTS = {
  jobs: '901421592255',
  hq: '901421591928',
};

// Bot keys and the env var prefix holding each bot's wake target.
const BOTS = {
  front_desk: { name: 'Front Desk', env: 'WAKE_FRONT_DESK' },
  billing: { name: 'Billing', env: 'WAKE_BILLING' },
  job_coordinator: { name: 'Job Coordinator', env: 'WAKE_JOB_COORDINATOR' },
  chief_of_staff: { name: 'Chief of Staff', env: 'WAKE_CHIEF_OF_STAFF' },
  web_presence: { name: 'Web Presence', env: 'WAKE_WEB_PRESENCE' },
};

// Jobs list status -> bot on duty. null means nobody is on duty.
const STATUS_DUTY = {
  'new': 'front_desk',
  'waiting on client': 'front_desk',
  'quoted': 'front_desk',
  'paid': 'front_desk',
  'pricing': 'billing',
  'price review': 'billing',
  'estimate': 'billing',
  'send estimate': 'billing',
  'deposit': 'billing',
  'send deposit': 'billing',
  'installed': 'billing',
  'send invoice': 'billing',
  'invoiced': 'billing',
  'won': 'job_coordinator',
  'scheduled': 'job_coordinator',
  'closed': null,
  'lost': null,
  'on hold': null,
};

// HQ card title prefix -> bot. "[Estimator]" is the old name for Billing.
const HQ_TITLE_BOTS = {
  'front desk': 'front_desk',
  'billing': 'billing',
  'estimator': 'billing',
  'job coordinator': 'job_coordinator',
  'chief of staff': 'chief_of_staff',
  'web presence': 'web_presence',
};

function normStatus(status) {
  return typeof status === 'string' ? status.trim().toLowerCase().replace(/\s+/g, ' ') : '';
}

// Returns a bot key, or null when nobody is on duty or the status is unknown.
function botForStatus(status) {
  const key = normStatus(status);
  if (!Object.prototype.hasOwnProperty.call(STATUS_DUTY, key)) return null;
  return STATUS_DUTY[key];
}

function isKnownStatus(status) {
  return Object.prototype.hasOwnProperty.call(STATUS_DUTY, normStatus(status));
}

function isClosedOrLost(status) {
  const key = normStatus(status);
  return key === 'closed' || key === 'lost';
}

// "[Billing] Receipts to categorize" -> 'billing'. Unknown or retired names -> null.
function botForHqTitle(title) {
  if (typeof title !== 'string') return null;
  const m = /^\s*\[([^\]\n]{1,40})\]/.exec(title);
  if (!m) return null;
  const key = m[1].trim().toLowerCase().replace(/\s+/g, ' ');
  return Object.prototype.hasOwnProperty.call(HQ_TITLE_BOTS, key) ? HQ_TITLE_BOTS[key] : null;
}

// Every bot comment is posted with Alex's ClickUp token, so the author field
// can't tell them apart. Bot comments start with "[Bot name]". Any leading
// bracketed name counts, so a bot that isn't in this file (COO, a retired bot)
// can't wake anyone either. "Alex (via CoS): ..." has no bracket and counts as Alex.
function isBotComment(text) {
  if (typeof text !== 'string') return false;
  return /^\s*\[[^\]\n]{1,40}\]/.test(text);
}

function rawBody(event) {
  const body = event && event.body != null ? event.body : '';
  if (typeof body !== 'string') return Buffer.alloc(0);
  // Netlify base64-encodes some bodies. The HMAC covers the exact bytes sent.
  if (event.isBase64Encoded) return Buffer.from(body, 'base64');
  return Buffer.from(body, 'utf8');
}

function headerValue(event, name) {
  const headers = (event && event.headers) || {};
  const want = name.toLowerCase();
  let value;
  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === want) value = headers[key];
  }
  if (Array.isArray(value)) value = value[0];
  return typeof value === 'string' ? value : '';
}

function hasValue(v) {
  return typeof v === 'string' && v.length > 0;
}

// Hex HMAC-SHA256 of the raw body, compared in constant time. Never throws.
function verifySignature(secret, signature, body) {
  if (!hasValue(secret)) return false;
  if (typeof signature !== 'string') return false;
  const provided = signature.trim().toLowerCase();
  if (provided.length !== 64 || !/^[0-9a-f]{64}$/.test(provided)) return false;
  const expected = crypto.createHmac('sha256', secret).update(body).digest();
  const actual = Buffer.from(provided, 'hex');
  return crypto.timingSafeEqual(expected, actual);
}

function isPaused() {
  return String(process.env.RELAY_PAUSED || '').trim().toLowerCase() === 'true';
}

function safeHeader(value) {
  return hasValue(value) && !/[\r\n\0]/.test(value);
}

// Chief of Staff keeps the target the original relay (PR #3) already used, so
// nothing new has to be pasted for it: WAKE_CHIEF_OF_STAFF_URL / _AUTH win if
// set, otherwise RELAY_TARGET_URL (default below) and RELAY_TARGET_AUTHORIZATION.
const DEFAULT_COS_TARGET = 'https://api2.cursor.sh/automations/webhook/6d7dec1b-159d-5f4d-a8a5-1beb74206318';

function envValue(name) {
  const v = process.env[name];
  return hasValue(v) ? v : '';
}

// The wake target for a bot, or null if its URL or Authorization isn't set.
function targetFor(bot) {
  const meta = BOTS[bot];
  if (!meta) return null;
  let url = envValue(`${meta.env}_URL`);
  let authorization = envValue(`${meta.env}_AUTH`);
  if (bot === 'chief_of_staff') {
    url = url || envValue('RELAY_TARGET_URL') || DEFAULT_COS_TARGET;
    authorization = authorization || envValue('RELAY_TARGET_AUTHORIZATION');
  }
  if (!hasValue(url) || !safeHeader(authorization)) return null;
  return { url: url.trim(), authorization };
}

function request(method, targetUrl, headers, body, timeoutMs) {
  return new Promise((resolve, reject) => {
    let settled = false;
    let url;
    try {
      url = new URL(targetUrl);
    } catch (err) {
      reject(Object.assign(new Error('request failed'), { code: 'BAD_URL' }));
      return;
    }
    if (url.protocol !== 'https:' && url.protocol !== 'http:') {
      reject(Object.assign(new Error('request failed'), { code: 'BAD_URL' }));
      return;
    }
    const lib = url.protocol === 'https:' ? https : http;
    const allHeaders = Object.assign({}, headers);
    if (body) allHeaders['Content-Length'] = body.length;
    const req = lib.request(
      {
        hostname: url.hostname,
        port: url.port || undefined,
        path: `${url.pathname}${url.search}`,
        method,
        headers: allHeaders,
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => done(null, { statusCode: res.statusCode || 0, body: Buffer.concat(chunks) }));
        res.on('error', () => done(Object.assign(new Error('request failed'), { code: 'ERROR' })));
      }
    );
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      req.destroy();
      done(Object.assign(new Error('timeout'), { code: 'TIMEOUT' }));
    }, timeoutMs);
    req.on('error', (err) => {
      if (timedOut) done(Object.assign(new Error('timeout'), { code: 'TIMEOUT' }));
      else done(Object.assign(new Error('request failed'), { code: (err && err.code) || 'ERROR' }));
    });
    req.end(body || undefined);

    function done(err, result) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (err) reject(err);
      else resolve(result);
    }
  });
}

// POST the normalized event to a wake target. Redirects are not followed.
async function forward(targetUrl, body, authorization, timeoutMs) {
  const res = await request(
    'POST',
    targetUrl,
    { 'Content-Type': 'application/json', Authorization: authorization },
    body,
    timeoutMs || FORWARD_TIMEOUT_MS
  );
  return { statusCode: res.statusCode };
}

// ClickUp API ---------------------------------------------------------------

function clickupBase() {
  return (process.env.CLICKUP_API_BASE || 'https://api.clickup.com/api/v2').replace(/\/+$/, '');
}

class LookupError extends Error {
  constructor(code, statusCode) {
    super('lookup failed');
    this.code = code;
    this.statusCode = statusCode || 0;
  }
  // 4xx from ClickUp (bad token, missing task) won't fix itself on retry.
  get permanent() {
    return this.code === 'NO_TOKEN' || (this.statusCode >= 400 && this.statusCode < 500);
  }
}

async function clickupGet(path) {
  const token = process.env.CLICKUP_API_TOKEN;
  if (!safeHeader(token)) throw new LookupError('NO_TOKEN');
  let res;
  try {
    res = await request('GET', `${clickupBase()}${path}`, { Authorization: token, Accept: 'application/json' }, null, LOOKUP_TIMEOUT_MS);
  } catch (err) {
    throw new LookupError(err && err.code === 'TIMEOUT' ? 'TIMEOUT' : 'NETWORK');
  }
  if (res.statusCode < 200 || res.statusCode >= 300) throw new LookupError('HTTP', res.statusCode);
  try {
    return JSON.parse(res.body.toString('utf8'));
  } catch (err) {
    throw new LookupError('BAD_JSON');
  }
}

async function getTask(taskId) {
  return clickupGet(`/task/${encodeURIComponent(taskId)}`);
}

function taskText(task) {
  return [task.description, task.text_content, task.markdown_description]
    .filter((v) => typeof v === 'string')
    .join('\n');
}

function containsThreadId(text, threadId) {
  if (typeof text !== 'string' || !threadId) return false;
  const re = new RegExp(`(^|[^0-9a-f])${threadId.toLowerCase()}([^0-9a-f]|$)`);
  return re.test(text.toLowerCase());
}

// One paginated read of the Jobs list (closed cards included). Returns the card
// whose description mentions the thread id, preferring the most recently updated
// one if more than one does, or null.
async function findJobByThread(threadId) {
  const matches = [];
  for (let page = 0; page < LIST_PAGE_LIMIT; page++) {
    const data = await clickupGet(
      `/list/${LISTS.jobs}/task?include_closed=true&subtasks=false&archived=false&page=${page}`
    );
    const tasks = Array.isArray(data && data.tasks) ? data.tasks : [];
    for (const t of tasks) {
      if (containsThreadId(taskText(t), threadId)) matches.push(t);
    }
    if (data && data.last_page === false && tasks.length > 0) continue;
    break;
  }
  if (!matches.length) return null;
  matches.sort((a, b) => Number(b.date_updated || 0) - Number(a.date_updated || 0));
  return matches[0];
}

function taskStatus(task) {
  if (!task) return '';
  if (task.status && typeof task.status === 'object') return task.status.status || '';
  return typeof task.status === 'string' ? task.status : '';
}

function taskUrl(taskId) {
  return taskId ? `https://app.clickup.com/t/${taskId}` : null;
}

// Normalized event ----------------------------------------------------------

const EVENT_FIELDS = [
  'source', 'event', 'list', 'task_id', 'task_name', 'task_url', 'new_status',
  'previous_status', 'comment_text', 'thread_id', 'message_id', 'from', 'subject', 'at',
];

function clip(value, max) {
  if (value == null) return null;
  const s = String(value);
  return s.length > max ? s.slice(0, max) : s;
}

function normalizedEvent(fields, bot) {
  const out = {};
  for (const key of EVENT_FIELDS) out[key] = fields[key] == null ? null : fields[key];
  out.comment_text = clip(out.comment_text, 500);
  out.subject = clip(out.subject, 300);
  out.from = clip(out.from, 300);
  out.task_name = clip(out.task_name, 300);
  out.bot = BOTS[bot] ? BOTS[bot].name : null;
  return out;
}

// Wake a bot with a normalized event. Resolves to an HTTP response for the caller.
async function wake(tag, bot, fields, detail) {
  const target = targetFor(bot);
  if (!target) {
    log(tag, 200, `${detail} action=drop reason=no_target bot=${bot}`);
    return respond(200, { ok: true, dropped: 'no_target' });
  }
  const body = Buffer.from(JSON.stringify(normalizedEvent(fields, bot)), 'utf8');
  try {
    const upstream = await forward(target.url, body, target.authorization, FORWARD_TIMEOUT_MS);
    if (upstream.statusCode >= 200 && upstream.statusCode < 300) {
      log(tag, 200, `${detail} action=forward bot=${bot} upstream=${upstream.statusCode}`);
      return respond(200, { ok: true, bot });
    }
    log(tag, 502, `${detail} action=forward bot=${bot} upstream=${upstream.statusCode}`);
    return respond(502, { error: 'upstream rejected' });
  } catch (err) {
    const reason = err && err.code === 'TIMEOUT' ? 'timeout' : 'forward_failed';
    log(tag, 502, `${detail} action=forward bot=${bot} ${reason}`);
    return respond(502, { error: reason === 'timeout' ? 'upstream timeout' : 'upstream error' });
  }
}

function drop(tag, reason, detail) {
  log(tag, 200, `${detail ? `${detail} ` : ''}action=drop reason=${reason}`);
  return respond(200, { ok: true, dropped: reason });
}

function respond(statusCode, payload, extraHeaders) {
  return {
    statusCode,
    headers: Object.assign(
      { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
      extraHeaders || {}
    ),
    body: JSON.stringify(payload),
  };
}

// Status codes, event kinds, ids and short reasons only.
function log(tag, statusCode, detail) {
  console.log(`${tag} status=${statusCode}${detail ? ` ${detail}` : ''}`);
}

module.exports = {
  DEFAULT_COS_TARGET,
  FORWARD_TIMEOUT_MS,
  LOOKUP_TIMEOUT_MS,
  LISTS,
  BOTS,
  STATUS_DUTY,
  HQ_TITLE_BOTS,
  LookupError,
  botForStatus,
  botForHqTitle,
  isKnownStatus,
  isClosedOrLost,
  isBotComment,
  normStatus,
  rawBody,
  headerValue,
  hasValue,
  verifySignature,
  isPaused,
  targetFor,
  request,
  forward,
  getTask,
  findJobByThread,
  containsThreadId,
  taskStatus,
  taskUrl,
  normalizedEvent,
  wake,
  drop,
  respond,
  log,
};
