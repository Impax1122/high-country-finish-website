'use strict';

// Checks for netlify/functions/clickup-relay.js and netlify/lib/wake.js.
// No test framework: `node scripts/test-clickup-relay.js`

const assert = require('assert');
const wake = require('../netlify/lib/wake');
const relay = require('../netlify/functions/clickup-relay');
const h = require('./wake-test-helpers');

const JOBS = '901421592255';
const HQ = '901421591928';
const SECRET = 'hq-webhook-secret';
const SECRET_JOBS = 'jobs-webhook-secret';

function statusEvent(taskId, listId, before, after) {
  return {
    event: 'taskStatusUpdated',
    task_id: taskId,
    webhook_id: 'wh',
    history_items: [{
      id: '1', type: 1, date: '1759441200000', field: 'status', parent_id: listId,
      user: { username: 'Alex Drew' },
      before: before == null ? null : { status: before, type: 'custom' },
      after: { status: after, type: 'custom' },
    }],
  };
}

function commentEvent(taskId, listId, text, opts) {
  const comment = (opts && opts.legacy)
    ? { id: 'c1', comment: [{ text }], user: { username: 'Alex Drew' } }
    : { id: 'c1', text_content: text, comment: [{ text }], user: { username: 'Alex Drew' } };
  return {
    event: 'taskCommentPosted',
    task_id: taskId,
    webhook_id: 'wh',
    history_items: [{ id: '2', type: 1, date: '1759441200000', field: 'comment', parent_id: listId, comment }],
  };
}

async function main() {
  const logs = [];
  const origLog = console.log;
  console.log = (...args) => logs.push(args.join(' '));

  // --- signature helper (unchanged from PR #3) ---
  const payload = Buffer.from('{"event":"taskCreated","text":"café — 壁"}', 'utf8');
  const goodSig = h.sign(SECRET, payload);
  assert.strictEqual(wake.verifySignature(SECRET, goodSig, payload), true);
  assert.strictEqual(wake.verifySignature(SECRET, goodSig.toUpperCase(), payload), true);
  assert.strictEqual(wake.verifySignature(SECRET, `  ${goodSig}  `, payload), true);
  assert.strictEqual(wake.verifySignature(SECRET, '', payload), false);
  assert.strictEqual(wake.verifySignature(SECRET, undefined, payload), false);
  assert.strictEqual(wake.verifySignature(SECRET, goodSig.slice(0, -1), payload), false);
  assert.strictEqual(wake.verifySignature(SECRET, 'g'.repeat(64), payload), false);
  assert.strictEqual(wake.verifySignature('other', goodSig, payload), false);
  assert.strictEqual(wake.verifySignature('', goodSig, payload), false);
  const b64 = payload.toString('base64');
  assert.deepStrictEqual(wake.rawBody({ body: b64, isBase64Encoded: true }), payload);
  assert.deepStrictEqual(wake.rawBody({ body: null }), Buffer.alloc(0));

  // --- routing table: every status ---
  const duty = {
    'new': 'front_desk', 'waiting on client': 'front_desk', 'quoted': 'front_desk', 'paid': 'front_desk',
    'pricing': 'billing', 'price review': 'billing', 'estimate': 'billing', 'send estimate': 'billing',
    'deposit': 'billing', 'send deposit': 'billing', 'installed': 'billing', 'send invoice': 'billing',
    'invoiced': 'billing', 'won': 'job_coordinator', 'scheduled': 'job_coordinator',
    'closed': null, 'Closed': null, 'lost': null, 'on hold': null,
  };
  for (const [status, bot] of Object.entries(duty)) {
    assert.strictEqual(wake.botForStatus(status), bot, status);
    assert.strictEqual(wake.botForStatus(status.toUpperCase()), bot, `${status} upper`);
  }
  assert.strictEqual(wake.botForStatus('to do'), null);
  assert.strictEqual(wake.isKnownStatus('to do'), false);
  assert.strictEqual(wake.botForHqTitle('[Front Desk] x'), 'front_desk');
  assert.strictEqual(wake.botForHqTitle('[Billing] x'), 'billing');
  assert.strictEqual(wake.botForHqTitle('[Estimator] old card'), 'billing');
  assert.strictEqual(wake.botForHqTitle('[Job Coordinator] x'), 'job_coordinator');
  assert.strictEqual(wake.botForHqTitle('[Chief of Staff] x'), 'chief_of_staff');
  assert.strictEqual(wake.botForHqTitle('[Web Presence] x'), 'web_presence');
  assert.strictEqual(wake.botForHqTitle('[web presence] x'), 'web_presence');
  assert.strictEqual(wake.botForHqTitle('[Growth] retired'), null);
  assert.strictEqual(wake.botForHqTitle('[Bookkeeper] retired'), null);
  assert.strictEqual(wake.botForHqTitle('No prefix'), null);
  assert.strictEqual(wake.isBotComment('[Front Desk] did a thing'), true);
  assert.strictEqual(wake.isBotComment('  [COO] note'), true);
  assert.strictEqual(wake.isBotComment('Alex (via CoS): please revise'), false);
  assert.strictEqual(wake.isBotComment('Looks good, send it'), false);

  const { server, state, base } = await h.startServer();
  const saved = h.saveEnv();
  const codes = [];
  const post = async (obj, opts) => {
    const body = typeof obj === 'string' ? obj : JSON.stringify(obj);
    const secret = (opts && opts.secret) || SECRET;
    const headers = (opts && 'headers' in opts) ? opts.headers : { 'X-Signature': h.sign(secret, body) };
    const res = await relay.handler({ httpMethod: (opts && opts.method) || 'POST', body, isBase64Encoded: false, headers });
    codes.push(res.statusCode);
    return res;
  };
  const expectWake = async (obj, bot, opts) => {
    h.reset(state);
    const res = await post(obj, opts);
    assert.strictEqual(res.statusCode, 200, `status for ${bot}`);
    assert.strictEqual(state.wakes.length, 1, `one wake for ${bot}`);
    assert.strictEqual(state.wakes[0].bot, bot);
    assert.strictEqual(state.wakes[0].authorization, `Bearer key-${bot}`);
    assert.strictEqual(state.wakes[0].contentType, 'application/json');
    return state.wakes[0].json;
  };
  const expectDrop = async (obj, reason, opts) => {
    h.reset(state);
    const res = await post(obj, opts);
    assert.strictEqual(res.statusCode, 200, `drop status (${reason})`);
    assert.strictEqual(state.wakes.length, 0, `no wake (${reason})`);
    if (reason) assert.strictEqual(JSON.parse(res.body).dropped, reason);
    return res;
  };

  try {
    h.configureTargets(base);
    process.env.CLICKUP_WEBHOOK_SECRET = SECRET;
    process.env.CLICKUP_WEBHOOK_SECRET_JOBS = SECRET_JOBS;

    // --- method, config, signatures ---
    let res = await post({}, { method: 'GET' });
    assert.strictEqual(res.statusCode, 405);
    assert.strictEqual(res.headers.Allow, 'POST');

    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'), { headers: {} });
    assert.strictEqual(res.statusCode, 403);
    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'), { secret: 'wrong' });
    assert.strictEqual(res.statusCode, 403);
    assert.strictEqual(state.wakes.length, 0);

    // Either secret is accepted (HQ webhook and Jobs webhook).
    await expectWake(statusEvent('t1', JOBS, 'new', 'pricing'), 'billing', { secret: SECRET });
    await expectWake(statusEvent('t1', JOBS, 'new', 'pricing'), 'billing', { secret: SECRET_JOBS });
    delete process.env.CLICKUP_WEBHOOK_SECRET;
    await expectWake(statusEvent('t1', JOBS, 'new', 'pricing'), 'billing', { secret: SECRET_JOBS });
    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'), { secret: SECRET });
    assert.strictEqual(res.statusCode, 403);
    delete process.env.CLICKUP_WEBHOOK_SECRET_JOBS;
    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'));
    assert.strictEqual(res.statusCode, 503, 'no secret at all is 503');
    process.env.CLICKUP_WEBHOOK_SECRET = SECRET;
    process.env.CLICKUP_WEBHOOK_SECRET_JOBS = SECRET_JOBS;

    // Base64 bodies are verified over the decoded bytes.
    {
      h.reset(state);
      const body = JSON.stringify(statusEvent('t1', JOBS, 'new', 'won'));
      const r = await relay.handler({
        httpMethod: 'POST', body: Buffer.from(body).toString('base64'), isBase64Encoded: true,
        headers: { 'x-signature': h.sign(SECRET, body) },
      });
      assert.strictEqual(r.statusCode, 200);
      assert.strictEqual(state.wakes[0].bot, 'job_coordinator');
    }

    // --- pause ---
    process.env.RELAY_PAUSED = 'true';
    await expectDrop(statusEvent('t1', JOBS, 'new', 'pricing'), 'paused');
    await expectDrop(statusEvent('t1', JOBS, 'new', 'pricing'), 'paused', { headers: {} });
    process.env.RELAY_PAUSED = 'TRUE';
    await expectDrop(statusEvent('t1', JOBS, 'new', 'pricing'), 'paused');
    process.env.RELAY_PAUSED = 'false';
    await expectWake(statusEvent('t1', JOBS, 'new', 'pricing'), 'billing');
    delete process.env.RELAY_PAUSED;

    // --- Jobs status changes: bot on duty for the NEW status, no ClickUp call ---
    for (const [status, bot] of Object.entries(duty)) {
      if (bot) {
        const json = await expectWake(statusEvent('job1', JOBS, 'previous', status), bot);
        assert.strictEqual(json.new_status, status);
        assert.strictEqual(json.previous_status, 'previous');
        assert.strictEqual(json.list, 'jobs');
        assert.strictEqual(json.source, 'clickup');
        assert.strictEqual(json.event, 'taskStatusUpdated');
        assert.strictEqual(json.task_id, 'job1');
        assert.strictEqual(json.task_url, 'https://app.clickup.com/t/job1');
        assert.strictEqual(json.at, '2025-10-02T21:40:00.000Z');
      } else {
        await expectDrop(statusEvent('job1', JOBS, 'invoiced', status), 'nobody_on_duty');
      }
      assert.strictEqual(state.apiCalls.length, 0, 'Jobs status change needs no lookup');
    }
    await expectDrop(statusEvent('job1', JOBS, 'new', 'to do'), 'unknown_status');

    // Missing parent_id: one GET finds the list.
    state.tasks.job2 = { id: 'job2', name: 'HC-26-0050 Acme – Main St', list: { id: JOBS }, status: { status: 'won' } };
    {
      const ev = statusEvent('job2', undefined, 'quoted', 'won');
      delete ev.history_items[0].parent_id;
      const json = await expectWake(ev, 'job_coordinator');
      assert.strictEqual(state.apiCalls.length, 1);
      assert.strictEqual(state.apiCalls[0].authorization, 'pk_test_token');
      assert.strictEqual(json.task_name, 'HC-26-0050 Acme – Main St');
    }

    // --- Jobs comments by Alex: bot on duty for the CURRENT status (one GET) ---
    for (const [status, bot] of Object.entries(duty)) {
      state.tasks.job3 = { id: 'job3', name: 'HC-26-0051 Beta – Elm', list: { id: JOBS }, status: { status } };
      if (bot) {
        const json = await expectWake(commentEvent('job3', JOBS, 'Change line 2 to $45'), bot);
        assert.strictEqual(json.comment_text, 'Change line 2 to $45');
        assert.strictEqual(json.new_status, status);
        assert.strictEqual(json.task_name, 'HC-26-0051 Beta – Elm');
        assert.strictEqual(state.apiCalls.length, 1);
        assert.ok(state.apiCalls[0].path.endsWith('/task/job3'));
      } else {
        await expectDrop(commentEvent('job3', JOBS, 'note'), 'nobody_on_duty');
      }
    }
    state.tasks.job3.status = { status: 'price review' };
    await expectWake(commentEvent('job3', JOBS, 'Alex (via CoS): drop the travel fee'), 'billing');
    await expectWake(commentEvent('job3', JOBS, 'legacy shape', { legacy: true }), 'billing');
    {
      const long = 'x'.repeat(800);
      const json = await expectWake(commentEvent('job3', JOBS, long), 'billing');
      assert.strictEqual(json.comment_text.length, 500);
    }

    // Bot comments: dropped before any ClickUp call.
    await expectDrop(commentEvent('job3', JOBS, '[Billing] Priced: $1,200'), 'bot_comment');
    await expectDrop(commentEvent('job3', JOBS, '[Front Desk] Intake done'), 'bot_comment');
    await expectDrop(commentEvent('hq1', HQ, '[Chief of Staff] brief'), 'bot_comment');
    assert.strictEqual(state.apiCalls.length, 0);

    // --- HQ list: bot named in the card title ---
    const hqTitles = {
      '[Front Desk] Not a job: vendor question': 'front_desk',
      '[Billing] Receipts to categorize': 'billing',
      '[Estimator] Old pricing card': 'billing',
      '[Job Coordinator] Photos with no match': 'job_coordinator',
      '[Chief of Staff] Weekly audit': 'chief_of_staff',
      '[Web Presence] Approve PR #9': 'web_presence',
    };
    for (const [title, bot] of Object.entries(hqTitles)) {
      state.tasks.hq1 = { id: 'hq1', name: title, list: { id: HQ }, status: { status: 'needs review' } };
      let json = await expectWake(statusEvent('hq1', HQ, 'needs review', 'approved'), bot);
      assert.strictEqual(json.list, 'hq');
      assert.strictEqual(json.task_name, title);
      assert.strictEqual(json.new_status, 'approved');
      json = await expectWake(commentEvent('hq1', HQ, 'Yes, do it'), bot);
      assert.strictEqual(json.new_status, 'needs review');
    }
    for (const title of ['[Growth] retired bot', '[Bookkeeper] retired', '[Follow-Up] x', 'No prefix at all']) {
      state.tasks.hq1 = { id: 'hq1', name: title, list: { id: HQ }, status: { status: 'open' } };
      await expectDrop(statusEvent('hq1', HQ, 'open', 'done'), 'no_bot_in_title');
      await expectDrop(commentEvent('hq1', HQ, 'ok'), 'no_bot_in_title');
    }

    // --- dropped events ---
    await expectDrop({ event: 'taskCreated', task_id: 'x', history_items: [] }, 'event_not_routed');
    await expectDrop({ event: 'taskUpdated', task_id: 'x', history_items: [{ field: 'name', parent_id: JOBS }] }, 'event_not_routed');
    await expectDrop({ event: 'taskAssigneeUpdated', task_id: 'x', history_items: [] }, 'event_not_routed');
    await expectDrop({ event: 'taskDueDateUpdated', task_id: 'x', history_items: [] }, 'event_not_routed');
    await expectDrop(statusEvent('o1', '123456', 'a', 'pricing'), 'other_list');
    await expectDrop(commentEvent('o1', '123456', 'hi'), 'other_list');
    await expectDrop('not json', 'bad_json');
    assert.strictEqual(state.apiCalls.length, 0);

    // --- missing target: drop + log, never 5xx ---
    delete process.env.WAKE_BILLING_URL;
    await expectDrop(statusEvent('t1', JOBS, 'new', 'pricing'), 'no_target');
    process.env.WAKE_BILLING_URL = `${base}/wake/billing`;
    process.env.WAKE_BILLING_AUTH = 'Bearer x\r\nEvil: 1';
    await expectDrop(statusEvent('t1', JOBS, 'new', 'pricing'), 'no_target');
    process.env.WAKE_BILLING_AUTH = 'Bearer key-billing';

    // --- Chief of Staff falls back to the original relay target ---
    delete process.env.WAKE_CHIEF_OF_STAFF_URL;
    delete process.env.WAKE_CHIEF_OF_STAFF_AUTH;
    process.env.RELAY_TARGET_URL = `${base}/wake/chief_of_staff`;
    process.env.RELAY_TARGET_AUTHORIZATION = 'Bearer key-chief_of_staff';
    state.tasks.hq1 = { id: 'hq1', name: '[Chief of Staff] x', list: { id: HQ }, status: { status: 'open' } };
    await expectWake(statusEvent('hq1', HQ, 'open', 'done'), 'chief_of_staff');
    delete process.env.RELAY_TARGET_AUTHORIZATION;
    await expectDrop(statusEvent('hq1', HQ, 'open', 'done'), 'no_target');
    delete process.env.RELAY_TARGET_URL;
    process.env.RELAY_TARGET_AUTHORIZATION = 'Bearer key';
    assert.strictEqual(wake.targetFor('chief_of_staff').url, wake.DEFAULT_COS_TARGET);
    assert.strictEqual(
      wake.DEFAULT_COS_TARGET,
      'https://api2.cursor.sh/automations/webhook/6d7dec1b-159d-5f4d-a8a5-1beb74206318'
    );
    process.env.WAKE_CHIEF_OF_STAFF_URL = 'https://example.test/cos';
    process.env.WAKE_CHIEF_OF_STAFF_AUTH = 'Bearer new';
    assert.deepStrictEqual(wake.targetFor('chief_of_staff'), { url: 'https://example.test/cos', authorization: 'Bearer new' });
    assert.strictEqual(wake.targetFor('front_desk').url, `${base}/wake/front_desk`);
    delete process.env.WAKE_FRONT_DESK_URL;
    assert.strictEqual(wake.targetFor('front_desk'), null, 'only CoS has a fallback');
    h.configureTargets(base);
    process.env.CLICKUP_WEBHOOK_SECRET = SECRET;

    // --- upstream failures: 502 so ClickUp retries ---
    state.targetStatus = 500;
    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'));
    assert.strictEqual(res.statusCode, 502);
    state.targetStatus = 302;
    res = await post(statusEvent('t1', JOBS, 'new', 'pricing'));
    assert.strictEqual(res.statusCode, 502, 'redirects are not followed');
    state.targetStatus = 200;

    // --- ClickUp lookup failures ---
    state.tasks.job3 = { id: 'job3', name: 'n', list: { id: JOBS }, status: { status: 'pricing' } };
    h.reset(state);
    state.apiStatus = 500;
    res = await post(commentEvent('job3', JOBS, 'hi'));
    assert.strictEqual(res.statusCode, 502, 'transient ClickUp error -> retry');
    h.reset(state);
    state.apiStatus = 401;
    res = await post(commentEvent('job3', JOBS, 'hi'));
    assert.strictEqual(res.statusCode, 200, 'bad ClickUp token -> drop, not a retry loop');
    assert.strictEqual(state.wakes.length, 0);
    h.reset(state);
    await expectDrop(commentEvent('missing', JOBS, 'hi'), 'lookup_http_404');
    delete process.env.CLICKUP_API_TOKEN;
    await expectDrop(commentEvent('job3', JOBS, 'hi'), 'lookup_no_token');
    process.env.CLICKUP_API_TOKEN = 'pk_test_token';

    // Upstream timeout.
    {
      const http = require('http');
      const hanging = http.createServer(() => {});
      await new Promise((r) => hanging.listen(0, '127.0.0.1', r));
      try {
        await wake.forward(`http://127.0.0.1:${hanging.address().port}/x`, Buffer.from('{}'), 'Bearer k', 150);
        assert.fail('forward should time out');
      } catch (err) {
        assert.strictEqual(err.code, 'TIMEOUT');
      } finally {
        hanging.closeAllConnections && hanging.closeAllConnections();
        hanging.close();
      }
    }

    // --- normalized body carries no raw ClickUp payload ---
    {
      const json = await expectWake(statusEvent('t9', JOBS, 'quoted', 'won'), 'job_coordinator');
      assert.deepStrictEqual(Object.keys(json).sort(), [
        'at', 'bot', 'comment_text', 'event', 'from', 'list', 'message_id', 'new_status', 'previous_status',
        'source', 'subject', 'task_id', 'task_name', 'task_url', 'thread_id',
      ]);
      assert.strictEqual(json.bot, 'Job Coordinator');
    }

    for (const code of codes) {
      assert.notStrictEqual(code, 401);
      assert.notStrictEqual(code, 410);
    }
    // Logs: no secrets, keys, tokens, task names or comment text.
    for (const line of logs) {
      for (const bad of [SECRET, SECRET_JOBS, 'key-', 'pk_test_token', 'Bearer', 'Change line 2', 'Acme', 'Receipts to categorize']) {
        assert.ok(!line.includes(bad), `log line leaks "${bad}": ${line}`);
      }
    }
    assert.ok(logs.length > 50);
  } finally {
    console.log = origLog;
    h.restoreEnv(saved);
    server.closeAllConnections && server.closeAllConnections();
    server.close();
  }
  console.log('clickup-relay tests passed');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
