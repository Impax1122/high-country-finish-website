'use strict';

// Checks the pure parts of automation/gmail-wake/Code.gs (classification,
// signing format, dedupe) in Node. The Apps Script services aren't loaded.
// No test framework: `node scripts/test-gmail-wake.js`

const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const dir = path.join(__dirname, '..', 'automation', 'gmail-wake');
const source = fs.readFileSync(path.join(dir, 'Code.gs'), 'utf8');
const sandbox = { module: { exports: {} }, console };
vm.runInNewContext(source, sandbox, { filename: 'Code.gs' });
const gs = sandbox.module.exports;

const manifest = JSON.parse(fs.readFileSync(path.join(dir, 'appsscript.json'), 'utf8'));
assert.deepStrictEqual(manifest.oauthScopes.slice().sort(), [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/script.external_request',
  'https://www.googleapis.com/auth/script.scriptapp',
]);
assert.strictEqual(manifest.runtimeVersion, 'V8');
assert.strictEqual(manifest.dependencies.enabledAdvancedServices[0].serviceId, 'gmail');
assert.ok(/everyMinutes\(5\)/.test(source), 'install() creates a 5-minute trigger');
assert.ok(/LAST_CHECK_MS/.test(source));

const ALEX = 'alexdrew@highcountryfinish.com';
const OPTS = { alexEmail: ALEX, receiptLabelIds: ['Label_77'] };

function msg(from, extra) {
  const headers = Object.assign({ from, subject: 'Hello' }, (extra && extra.headers) || {});
  return Object.assign({ id: 'b2', threadId: 'b1', labelIds: ['INBOX'], internalDate: 1000, headers }, extra || {}, { headers });
}
const kind = (m) => gs.classifyMessage(m, OPTS).kind;
const reason = (m) => gs.classifyMessage(m, OPTS).reason;

// Addresses
assert.strictEqual(gs.emailAddress('Jane <Jane@Example.com>'), 'jane@example.com');
assert.strictEqual(gs.emailAddress('bob@x.co'), 'bob@x.co');
assert.strictEqual(gs.emailAddress('Undisclosed'), '');
assert.deepStrictEqual(
  JSON.parse(JSON.stringify(gs.headerMap([{ name: 'From', value: 'a@b.c' }, { name: 'List-Unsubscribe', value: '<x>' }]))),
  { from: 'a@b.c', 'list-unsubscribe': '<x>' }
);

// Client mail: first message -> new_thread, later -> reply
assert.strictEqual(kind(msg('Jane <jane@acmesigns.com>', { id: 'a1', threadId: 'a1' })), 'new_thread');
assert.strictEqual(kind(msg('Jane <jane@acmesigns.com>')), 'reply');
// Yelp lead messages ARE client mail, even with bulk headers.
assert.strictEqual(kind(msg('Yelp <reply+abc@messaging.yelp.com>', { id: 'y1', threadId: 'y1', headers: { 'list-unsubscribe': '<x>' } })), 'new_thread');
assert.strictEqual(kind(msg('Yelp <reply+abc@messaging.yelp.com>')), 'reply');

// Alex
assert.strictEqual(kind(msg(`Alex Drew <${ALEX}>`, { labelIds: ['SENT'] })), 'alex_sent');
assert.strictEqual(kind(msg(`Alex Drew <${ALEX.toUpperCase()}>`, { labelIds: ['SENT', 'INBOX'] })), 'alex_sent');
assert.strictEqual(kind(msg(`Alex Drew <${ALEX}>`, { labelIds: ['INBOX'] })), null);
assert.strictEqual(reason(msg(`Alex Drew <${ALEX}>`, { labelIds: ['DRAFT'] })), 'draft');
assert.strictEqual(reason(msg('Jane <jane@acmesigns.com>', { labelIds: ['DRAFT'] })), 'draft');

// Automated senders and headers
for (const from of [
  'Google <no-reply@accounts.google.com>',
  'X <noreply@wave.com>',
  'X <donotreply@bank.com>',
  'X <do-not-reply@bank.com>',
  'Mail Delivery Subsystem <mailer-daemon@googlemail.com>',
  'GitHub <notifications@github.com>',
  'X <notification@service.io>',
  'Google Business Profile <businessprofile-noreply@google.com>',
  'Google <calendar-notification@google.com>',
  'Yelp <biz@yelp.com>',
  'Yelp <no-reply@yelp.com>',
]) {
  assert.strictEqual(kind(msg(from, { id: 'n1', threadId: 'n1' })), null, from);
  assert.strictEqual(reason(msg(from, { id: 'n1', threadId: 'n1' })), 'automated', from);
}
assert.strictEqual(kind(msg('Shop <news@shop.com>', { headers: { 'list-unsubscribe': '<mailto:u@shop.com>' } })), null);
assert.strictEqual(kind(msg('Shop <news@shop.com>', { headers: { precedence: 'bulk' } })), null);
assert.strictEqual(kind(msg('Shop <news@shop.com>', { headers: { precedence: 'list' } })), null);
assert.strictEqual(kind(msg('Bot <bot@shop.com>', { headers: { 'auto-submitted': 'auto-generated' } })), null);
assert.strictEqual(kind(msg('Jane <jane@acmesigns.com>', { headers: { 'auto-submitted': 'no' } })), 'reply');
// A person named "Notifications" at a normal address isn't caught by the name.
assert.strictEqual(kind(msg('Notifications Team <jane@acmesigns.com>')), 'reply');

// Receipts label
assert.strictEqual(reason(msg('Home Depot <orders@homedepot.com>', { labelIds: ['INBOX', 'Label_77'] })), 'receipt');
// Spam/trash and missing sender
assert.strictEqual(kind(msg('Jane <jane@acmesigns.com>', { labelIds: ['SPAM'] })), null);
assert.strictEqual(reason(msg('', {})), 'no_sender');

// Signed body: ASCII-only JSON, hex HMAC matches Node's
const payload = gs.relayPayload(msg('Jöse <jose@x.com>', { headers: { subject: 'Café — sign' }, internalDate: 1759442400000 }), 'reply');
assert.deepStrictEqual(JSON.parse(JSON.stringify(payload)), {
  kind: 'reply', thread_id: 'b1', message_id: 'b2', from: 'Jöse <jose@x.com>', subject: 'Café — sign',
  at: '2025-10-02T22:00:00.000Z',
});
const body = gs.asciiJson(payload);
assert.ok(/^[\x00-\x7f]*$/.test(body), 'body is pure ASCII');
assert.deepStrictEqual(JSON.parse(body), JSON.parse(JSON.stringify(payload)));
const digest = crypto.createHmac('sha256', 'secret').update(body).digest();
const signed = Array.from(digest).map((b) => (b > 127 ? b - 256 : b)); // Apps Script returns signed bytes
assert.strictEqual(gs.bytesToHex(signed), digest.toString('hex'));

// Dedupe and marker
const list = [
  { id: 'm3', internalDate: 3000 },
  { id: 'm1', internalDate: 1000 },
  { id: 'm2', internalDate: 2000 },
  { id: 'old', internalDate: 10 },
];
const marker = 500 + gs.OVERLAP_MS; // window starts at 500: m1 in, "old" out
assert.deepStrictEqual(gs.pendingMessages(list, marker, ['m2']).map((m) => m.id), ['m1', 'm3']);
let seen = [];
for (let i = 0; i < 1005; i++) seen = gs.rememberSeen(seen, `id${i}`);
assert.strictEqual(seen.length, 1000);
assert.strictEqual(seen[0], 'id5');
seen = gs.rememberSeen(seen, 'id5');
assert.strictEqual(seen[seen.length - 1], 'id5');
assert.strictEqual(seen.length, 1000);

console.log('gmail-wake tests passed');
