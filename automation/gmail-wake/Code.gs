/**
 * High Country Gmail wake script.
 *
 * Runs as alexdrew@highcountryfinish.com every 5 minutes. For each new message
 * since the last check it decides one of:
 *   alex_sent  - Alex sent it (Sent label, from Alex)
 *   new_thread - first message of a thread, from someone else, not automated
 *   reply      - a later message on a thread, from someone else, not automated
 *   (skip)     - automated mail, receipts, drafts, Alex's mail that isn't sent
 * and POSTs {kind, thread_id, message_id, from, subject, at} to the Netlify
 * gmail-relay, signed with HMAC-SHA256 (hex) of the body in X-Signature.
 * The relay decides which bot to wake.
 *
 * Script Properties (Project Settings > Script Properties):
 *   RELAY_URL          https://highcountryfinish.com/.netlify/functions/gmail-relay
 *   GMAIL_RELAY_SECRET the same long random string as Netlify's GMAIL_RELAY_SECRET
 * Kept by the script itself:
 *   LAST_CHECK_MS      newest message time handled (pausing resumes from here)
 *   SEEN_IDS           recent message ids already handled (dedupe)
 *   FAILS              per-message failure counts
 *
 * Run install() once to create the 5-minute trigger. Run uninstall() (or
 * delete the trigger) to pause. The marker is kept, so the next run after a
 * pause picks up from the last check.
 */

var ALEX_EMAIL = 'alexdrew@highcountryfinish.com';
var HANDLER = 'checkMail';
var OVERLAP_MS = 2 * 60 * 1000;
var MAX_LIST = 200;
var MAX_PER_RUN = 50;
var SEEN_CAP = 1000;
var MAX_FAILS = 6; // about 30 minutes of retries, then the message is skipped

// ---------------------------------------------------------------------------
// Pure helpers (no Google services). Tested in Node: scripts/test-gmail-wake.js

/** "Jane <Jane@Example.com>" -> "jane@example.com" */
function emailAddress(from) {
  if (typeof from !== 'string') return '';
  var m = /<([^>]+)>/.exec(from);
  var addr = (m ? m[1] : from).trim().toLowerCase();
  return /^[^\s@]+@[^\s@]+$/.test(addr) ? addr : '';
}

function domainOf(addr) {
  var at = addr.lastIndexOf('@');
  return at < 0 ? '' : addr.slice(at + 1);
}

function domainIs(domain, base) {
  return domain === base || domain.slice(-(base.length + 1)) === '.' + base;
}

/** Lower-cased header name -> value, from a Gmail API payload.headers array. */
function headerMap(headers) {
  var out = {};
  (headers || []).forEach(function (h) {
    if (h && typeof h.name === 'string') out[h.name.toLowerCase()] = String(h.value == null ? '' : h.value);
  });
  return out;
}

/**
 * Is this message automated (or a system notice) rather than client mail?
 * Yelp lead messages (messaging.yelp.com) are client mail even though they
 * carry bulk-mail headers.
 */
function isAutomated(addr, headers) {
  var h = headers || {};
  var domain = domainOf(addr);
  if (domainIs(domain, 'messaging.yelp.com')) return false;
  var local = addr.split('@')[0] || '';
  if (/(^|[._+-])(no-?reply|do-?not-?reply|donotreply|mailer-daemon|postmaster|notifications?|bounces?)([._+-]|$)/.test(local)) return true;
  if (/noreply|no-reply/.test(local)) return true;
  if (h['list-unsubscribe'] || h['list-id']) return true;
  if (/^(bulk|list|junk|auto_reply)$/i.test((h['precedence'] || '').trim())) return true;
  var auto = (h['auto-submitted'] || '').trim().toLowerCase();
  if (auto && auto !== 'no') return true;
  if (domainIs(domain, 'google.com') || domainIs(domain, 'yelp.com')) return true;
  return false;
}

/**
 * msg: {id, threadId, labelIds, internalDate, headers (lower-cased map)}
 * opts: {alexEmail, receiptLabelIds: [...]}
 * Returns {kind: 'alex_sent'|'new_thread'|'reply'|null, reason}.
 */
function classifyMessage(msg, opts) {
  var labels = msg.labelIds || [];
  var alex = ((opts && opts.alexEmail) || ALEX_EMAIL).toLowerCase();
  var receiptIds = (opts && opts.receiptLabelIds) || [];
  var addr = emailAddress((msg.headers || {})['from']);
  if (labels.indexOf('DRAFT') >= 0) return { kind: null, reason: 'draft' };
  if (labels.indexOf('SPAM') >= 0 || labels.indexOf('TRASH') >= 0) return { kind: null, reason: 'spam_or_trash' };
  if (addr === alex) {
    if (labels.indexOf('SENT') >= 0) return { kind: 'alex_sent', reason: 'sent' };
    return { kind: null, reason: 'from_alex_not_sent' };
  }
  for (var i = 0; i < receiptIds.length; i++) {
    if (labels.indexOf(receiptIds[i]) >= 0) return { kind: null, reason: 'receipt' };
  }
  if (!addr) return { kind: null, reason: 'no_sender' };
  if (isAutomated(addr, msg.headers)) return { kind: null, reason: 'automated' };
  // Gmail gives a thread the id of its first message.
  if (msg.id === msg.threadId) return { kind: 'new_thread', reason: 'first_message' };
  return { kind: 'reply', reason: 'later_message' };
}

/** JSON with every non-ASCII character escaped, so the signed bytes are unambiguous. */
function asciiJson(obj) {
  return JSON.stringify(obj).replace(/[\u007f-\uffff]/g, function (c) {
    return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
  });
}

/** Signed bytes (-128..127, as Apps Script returns them) -> lowercase hex. */
function bytesToHex(bytes) {
  return bytes.map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}

function relayPayload(msg, kind) {
  var h = msg.headers || {};
  return {
    kind: kind,
    thread_id: msg.threadId,
    message_id: msg.id,
    from: (h['from'] || '').slice(0, 300),
    subject: (h['subject'] || '').slice(0, 300),
    at: new Date(Number(msg.internalDate)).toISOString()
  };
}

/** Which listed messages still need handling, oldest first. */
function pendingMessages(msgs, lastCheckMs, seenIds) {
  var seen = {};
  (seenIds || []).forEach(function (id) { seen[id] = true; });
  return msgs
    .filter(function (m) { return !seen[m.id] && Number(m.internalDate) > lastCheckMs - OVERLAP_MS; })
    .sort(function (a, b) { return Number(a.internalDate) - Number(b.internalDate); });
}

function rememberSeen(seenIds, id) {
  var out = (seenIds || []).filter(function (x) { return x !== id; });
  out.push(id);
  return out.length > SEEN_CAP ? out.slice(out.length - SEEN_CAP) : out;
}

// ---------------------------------------------------------------------------
// Apps Script entry points

function install() {
  uninstall();
  ScriptApp.newTrigger(HANDLER).timeBased().everyMinutes(5).create();
  var props = PropertiesService.getScriptProperties();
  if (!props.getProperty('LAST_CHECK_MS')) props.setProperty('LAST_CHECK_MS', String(Date.now()));
  console.log('gmail-wake installed: every 5 minutes');
}

function uninstall() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === HANDLER) ScriptApp.deleteTrigger(t);
  });
}

function checkMail() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return;
  try {
    run_();
  } finally {
    lock.releaseLock();
  }
}

function run_() {
  var props = PropertiesService.getScriptProperties();
  var relayUrl = props.getProperty('RELAY_URL');
  var secret = props.getProperty('GMAIL_RELAY_SECRET');
  if (!relayUrl || !secret) {
    console.warn('gmail-wake: RELAY_URL or GMAIL_RELAY_SECRET not set');
    return;
  }
  var lastCheck = Number(props.getProperty('LAST_CHECK_MS') || Date.now());
  var seen = JSON.parse(props.getProperty('SEEN_IDS') || '[]');
  var fails = JSON.parse(props.getProperty('FAILS') || '{}');

  var receiptLabelIds = (Gmail.Users.Labels.list('me').labels || [])
    .filter(function (l) { return l.name === 'Receipts' || l.name.indexOf('Receipts/') === 0; })
    .map(function (l) { return l.id; });

  var afterSec = Math.floor((lastCheck - OVERLAP_MS) / 1000);
  var listed = [];
  var pageToken;
  do {
    var res = Gmail.Users.Messages.list('me', { q: 'after:' + afterSec, maxResults: 100, pageToken: pageToken });
    (res.messages || []).forEach(function (m) { listed.push(m.id); });
    pageToken = res.nextPageToken;
  } while (pageToken && listed.length < MAX_LIST);

  var msgs = listed
    .filter(function (id) { return seen.indexOf(id) < 0; })
    .map(function (id) {
      var m = Gmail.Users.Messages.get('me', id, {
        format: 'metadata',
        metadataHeaders: ['From', 'Subject', 'List-Unsubscribe', 'List-Id', 'Precedence', 'Auto-Submitted']
      });
      return {
        id: m.id,
        threadId: m.threadId,
        labelIds: m.labelIds || [],
        internalDate: Number(m.internalDate),
        headers: headerMap(m.payload && m.payload.headers)
      };
    });

  var todo = pendingMessages(msgs, lastCheck, seen).slice(0, MAX_PER_RUN);
  for (var i = 0; i < todo.length; i++) {
    var msg = todo[i];
    var c = classifyMessage(msg, { alexEmail: ALEX_EMAIL, receiptLabelIds: receiptLabelIds });
    // An unsent draft is not remembered: if Alex sends it, the sent copy must
    // still be seen as alex_sent even when Gmail keeps the same message id.
    if (c.reason === 'draft') continue;
    if (c.kind) {
      var body = asciiJson(relayPayload(msg, c.kind));
      var sig = bytesToHex(Utilities.computeHmacSha256Signature(body, secret, Utilities.Charset.UTF_8));
      var code = 0;
      try {
        code = UrlFetchApp.fetch(relayUrl, {
          method: 'post',
          contentType: 'application/json',
          payload: body,
          headers: { 'X-Signature': sig },
          muteHttpExceptions: true,
          followRedirects: false
        }).getResponseCode();
      } catch (e) {
        code = 0;
      }
      if (code < 200 || code >= 300) {
        fails[msg.id] = (fails[msg.id] || 0) + 1;
        console.warn('gmail-wake: relay returned ' + code + ' for ' + msg.id + ' (try ' + fails[msg.id] + ')');
        if (fails[msg.id] < MAX_FAILS) break; // stop here; retry from this message next run
        console.error('gmail-wake: giving up on ' + msg.id + ' after ' + MAX_FAILS + ' tries');
      }
    }
    delete fails[msg.id];
    seen = rememberSeen(seen, msg.id);
    if (msg.internalDate > lastCheck) lastCheck = msg.internalDate;
  }

  props.setProperties({
    LAST_CHECK_MS: String(lastCheck),
    SEEN_IDS: JSON.stringify(seen),
    FAILS: JSON.stringify(fails)
  });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    emailAddress: emailAddress,
    headerMap: headerMap,
    isAutomated: isAutomated,
    classifyMessage: classifyMessage,
    asciiJson: asciiJson,
    bytesToHex: bytesToHex,
    relayPayload: relayPayload,
    pendingMessages: pendingMessages,
    rememberSeen: rememberSeen,
    OVERLAP_MS: OVERLAP_MS
  };
}
