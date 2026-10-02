'use strict';

// Checks for netlify/functions/gmail-relay.js.
// No test framework: `node scripts/test-gmail-relay.js`

const assert = require('assert');
const relay = require('../netlify/functions/gmail-relay');
const h = require('./wake-test-helpers');

const SECRET = 'gmail-relay-secret';
const THREAD = '1a0f80bbf790c829';

function ev(kind, extra) {
  return Object.assign({
    kind,
    thread_id: THREAD,
    message_id: '1a0f80bbf790c830',
    from: 'Jane Client <jane@example.com>',
    subject: 'Re: Window graphics',
    at: '2026-10-02T22:00:00.000Z',
  }, extra || {});
}

function job(id, status, description, updated) {
  return { id, name: `HC-26-00${id} Client – Site`, status: { status }, description, date_updated: String(updated || 1), url: `https://app.clickup.com/t/${id}` };
}

async function main() {
  const logs = [];
  const origLog = console.log;
  console.log = (...args) => logs.push(args.join(' '));

  const { server, state, base } = await h.startServer();
  const saved = h.saveEnv();
  const codes = [];
  const post = async (obj, opts) => {
    const body = typeof obj === 'string' ? obj : JSON.stringify(obj);
    const headers = (opts && 'headers' in opts) ? opts.headers : { 'X-Signature': h.sign((opts && opts.secret) || SECRET, body) };
    const res = await relay.handler({ httpMethod: (opts && opts.method) || 'POST', body, isBase64Encoded: false, headers });
    codes.push(res.statusCode);
    return res;
  };
  const expectWake = async (obj, bot) => {
    h.reset(state);
    const res = await post(obj);
    assert.strictEqual(res.statusCode, 200, `status for ${bot}`);
    assert.strictEqual(state.wakes.length, 1, `one wake for ${bot}`);
    assert.strictEqual(state.wakes[0].bot, bot);
    assert.strictEqual(state.wakes[0].authorization, `Bearer key-${bot}`);
    return state.wakes[0].json;
  };
  const expectDrop = async (obj, reason, opts) => {
    h.reset(state);
    const res = await post(obj, opts);
    assert.strictEqual(res.statusCode, 200, `drop (${reason})`);
    assert.strictEqual(state.wakes.length, 0, `no wake (${reason})`);
    assert.strictEqual(JSON.parse(res.body).dropped, reason);
  };

  try {
    h.configureTargets(base);
    process.env.GMAIL_RELAY_SECRET = SECRET;

    // --- method, config, signature, pause ---
    let res = await post(ev('new_thread'), { method: 'GET' });
    assert.strictEqual(res.statusCode, 405);
    res = await post(ev('new_thread'), { headers: {} });
    assert.strictEqual(res.statusCode, 403);
    res = await post(ev('new_thread'), { secret: 'wrong' });
    assert.strictEqual(res.statusCode, 403);
    delete process.env.GMAIL_RELAY_SECRET;
    res = await post(ev('new_thread'));
    assert.strictEqual(res.statusCode, 503);
    process.env.GMAIL_RELAY_SECRET = SECRET;
    process.env.RELAY_PAUSED = 'true';
    await expectDrop(ev('new_thread'), 'paused');
    await expectDrop(ev('new_thread'), 'paused', { headers: {} });
    delete process.env.RELAY_PAUSED;
    assert.strictEqual(state.wakes.length, 0);

    // --- new_thread -> Front Desk, no ClickUp lookup ---
    let json = await expectWake(ev('new_thread'), 'front_desk');
    assert.strictEqual(state.apiCalls.length, 0);
    assert.strictEqual(json.source, 'gmail');
    assert.strictEqual(json.event, 'new_thread');
    assert.strictEqual(json.thread_id, THREAD);
    assert.strictEqual(json.message_id, '1a0f80bbf790c830');
    assert.strictEqual(json.from, 'Jane Client <jane@example.com>');
    assert.strictEqual(json.subject, 'Re: Window graphics');
    assert.strictEqual(json.at, '2026-10-02T22:00:00.000Z');
    assert.strictEqual(json.bot, 'Front Desk');

    // --- reply -> bot on duty of the matching job ---
    const duty = {
      'new': 'front_desk', 'waiting on client': 'front_desk', 'quoted': 'front_desk', 'paid': 'front_desk',
      'pricing': 'billing', 'price review': 'billing', 'estimate': 'billing', 'send estimate': 'billing',
      'deposit': 'billing', 'send deposit': 'billing', 'installed': 'billing', 'send invoice': 'billing',
      'invoiced': 'billing', 'won': 'job_coordinator', 'scheduled': 'job_coordinator',
    };
    for (const [status, bot] of Object.entries(duty)) {
      state.listPages = [[job('1', status, `Client: Jane\nThread ID: ${THREAD}\n`)]];
      json = await expectWake(ev('reply'), bot);
      assert.strictEqual(json.task_id, '1');
      assert.strictEqual(json.list, 'jobs');
      assert.strictEqual(json.new_status, status);
      assert.strictEqual(state.apiCalls.length, 1);
      assert.ok(state.apiCalls[0].path.endsWith('/list/901421592255/task'));
      assert.ok(/include_closed=true/.test(state.apiCalls[0].query));
      assert.ok(/page=0/.test(state.apiCalls[0].query));
    }
    // Closed or Lost -> Front Desk; On hold -> nobody.
    for (const status of ['Closed', 'closed', 'lost']) {
      state.listPages = [[job('1', status, `Thread ID: ${THREAD}`)]];
      await expectWake(ev('reply'), 'front_desk');
    }
    state.listPages = [[job('1', 'on hold', `Thread ID: ${THREAD}`)]];
    await expectDrop(ev('reply'), 'nobody_on_duty');
    // No matching job -> Front Desk.
    state.listPages = [[job('1', 'pricing', 'Thread ID: 19aaaaaaaaaaaaaa')]];
    json = await expectWake(ev('reply'), 'front_desk');
    assert.strictEqual(json.task_id, null);

    // Pagination, second thread id on the card, case, and no partial-id matches.
    state.listPages = [
      [job('1', 'pricing', `Thread ID: ${THREAD}0`)],
      [job('2', 'won', `Thread ID: 19bbbbbbbbbbbbbb (original thread ${THREAD.toUpperCase()})`)],
    ];
    json = await expectWake(ev('reply'), 'job_coordinator');
    assert.strictEqual(json.task_id, '2');
    assert.strictEqual(state.apiCalls.length, 2, 'one paginated read');
    // Two cards mention the thread: the most recently updated wins.
    state.listPages = [[job('1', 'pricing', `Thread ID: ${THREAD}`, 100), job('2', 'invoiced', `Thread ID: ${THREAD}`, 200)]];
    json = await expectWake(ev('reply'), 'billing');
    assert.strictEqual(json.task_id, '2');
    // text_content is searched too.
    state.listPages = [[{ id: '3', name: 'x', status: { status: 'scheduled' }, text_content: `Thread ID: ${THREAD}` }]];
    await expectWake(ev('reply'), 'job_coordinator');

    // --- alex_sent -> that job's bot on duty; no job or nobody -> drop ---
    for (const [status, bot] of Object.entries(duty)) {
      state.listPages = [[job('1', status, `Thread ID: ${THREAD}`)]];
      await expectWake(ev('alex_sent', { from: 'Alex Drew <alexdrew@highcountryfinish.com>' }), bot);
    }
    for (const status of ['closed', 'lost', 'on hold']) {
      state.listPages = [[job('1', status, `Thread ID: ${THREAD}`)]];
      await expectDrop(ev('alex_sent'), 'nobody_on_duty');
    }
    state.listPages = [[]];
    await expectDrop(ev('alex_sent'), 'no_job');

    // --- other kinds and bad input ---
    await expectDrop(ev('receipt'), 'kind_not_routed');
    await expectDrop(ev('automated'), 'kind_not_routed');
    await expectDrop({ thread_id: THREAD }, 'kind_not_routed');
    await expectDrop(ev('reply', { thread_id: 'not-hex!' }), 'bad_thread_id');
    await expectDrop('nope', 'bad_json');

    // --- missing target: drop + log ---
    delete process.env.WAKE_FRONT_DESK_AUTH;
    await expectDrop(ev('new_thread'), 'no_target');
    h.configureTargets(base);
    process.env.GMAIL_RELAY_SECRET = SECRET;

    // --- failures -> 502 so the script retries ---
    state.targetStatus = 503;
    res = await post(ev('new_thread'));
    assert.strictEqual(res.statusCode, 502);
    h.reset(state);
    state.apiStatus = 500;
    res = await post(ev('reply'));
    assert.strictEqual(res.statusCode, 502);
    h.reset(state);
    state.apiStatus = 401;
    res = await post(ev('reply'));
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(JSON.parse(res.body).dropped, 'lookup_http_401');
    assert.strictEqual(state.wakes.length, 0);
    h.reset(state);
    delete process.env.CLICKUP_API_TOKEN;
    await expectDrop(ev('reply'), 'lookup_no_token');

    for (const code of codes) {
      assert.notStrictEqual(code, 401);
      assert.notStrictEqual(code, 410);
    }
    // Logs: no secrets, keys, tokens, senders or subjects.
    for (const line of logs) {
      for (const bad of [SECRET, 'key-', 'pk_test_token', 'jane@example.com', 'Window graphics', 'Bearer']) {
        assert.ok(!line.includes(bad), `log line leaks "${bad}": ${line}`);
      }
    }
    assert.ok(logs.length > 10);
  } finally {
    console.log = origLog;
    h.restoreEnv(saved);
    server.closeAllConnections && server.closeAllConnections();
    server.close();
  }
  console.log('gmail-relay tests passed');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
