'use strict';

// Signature and relay checks for netlify/functions/clickup-relay.js.
// No test framework: `node scripts/test-clickup-relay.js`

const assert = require('assert');
const crypto = require('crypto');
const http = require('http');
const relay = require('../netlify/functions/clickup-relay');

function sign(secret, body) {
  return crypto.createHmac('sha256', secret).update(body).digest('hex');
}

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

async function main() {
  const secret = 'test-webhook-secret';
  const payload = Buffer.from('{"event":"taskCreated","text":"café — 壁"}', 'utf8');
  const goodSig = sign(secret, payload);

  assert.strictEqual(relay.verifySignature(secret, goodSig, payload), true);
  assert.strictEqual(relay.verifySignature(secret, goodSig.toUpperCase(), payload), true);
  assert.strictEqual(relay.verifySignature(secret, `  ${goodSig}  `, payload), true);
  assert.strictEqual(relay.verifySignature(secret, '', payload), false);
  assert.strictEqual(relay.verifySignature(secret, undefined, payload), false);
  assert.strictEqual(relay.verifySignature(secret, goodSig.slice(0, -1), payload), false);
  assert.strictEqual(relay.verifySignature(secret, 'g'.repeat(64), payload), false);
  assert.strictEqual(relay.verifySignature(secret, '0'.repeat(64), payload), false);
  assert.strictEqual(relay.verifySignature('other-secret', goodSig, payload), false);
  assert.strictEqual(relay.verifySignature('', goodSig, payload), false);

  const flipped = Buffer.from(payload);
  flipped[0] = flipped[0] ^ 0x01;
  assert.strictEqual(relay.verifySignature(secret, goodSig, flipped), false);

  const b64 = payload.toString('base64');
  assert.deepStrictEqual(relay.rawBody({ body: b64, isBase64Encoded: true }), payload);
  assert.deepStrictEqual(relay.rawBody({ body: payload.toString('utf8'), isBase64Encoded: false }), payload);
  assert.deepStrictEqual(relay.rawBody({ body: null }), Buffer.alloc(0));
  assert.strictEqual(relay.FORWARD_TIMEOUT_MS, 5000);
  assert.strictEqual(
    relay.DEFAULT_TARGET,
    'https://api2.cursor.sh/automations/webhook/6d7dec1b-159d-5f4d-a8a5-1beb74206318'
  );

  const seen = [];
  let upstreamStatus = 204;
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      seen.push({
        method: req.method,
        url: req.url,
        authorization: req.headers.authorization,
        contentType: req.headers['content-type'],
        body: Buffer.concat(chunks),
      });
      res.writeHead(upstreamStatus, { 'Content-Type': 'text/plain' });
      res.end('ok');
    });
  });
  const port = await listen(server);
  const target = `http://127.0.0.1:${port}/hook`;

  const statuses = [];
  const prevHandler = relay.handler;
  relay.handler = async (event) => {
    const res = await prevHandler(event);
    statuses.push(res.statusCode);
    return res;
  };

  const prev = {
    secret: process.env.CLICKUP_WEBHOOK_SECRET,
    auth: process.env.RELAY_TARGET_AUTHORIZATION,
    url: process.env.RELAY_TARGET_URL,
  };
  process.env.CLICKUP_WEBHOOK_SECRET = secret;
  process.env.RELAY_TARGET_AUTHORIZATION = 'Bearer cursor-token';
  process.env.RELAY_TARGET_URL = target;

  const post = (overrides) => relay.handler(Object.assign({
    httpMethod: 'POST',
    body: payload.toString('utf8'),
    isBase64Encoded: false,
    headers: { 'X-Signature': goodSig },
  }, overrides));

  try {
    let res = await relay.handler({ httpMethod: 'GET', body: payload.toString('utf8') });
    assert.strictEqual(res.statusCode, 405);
    assert.strictEqual(res.headers.Allow, 'POST');
    assert.strictEqual(seen.length, 0);

    delete process.env.CLICKUP_WEBHOOK_SECRET;
    res = await post();
    assert.strictEqual(res.statusCode, 503);
    assert.strictEqual(seen.length, 0);
    process.env.CLICKUP_WEBHOOK_SECRET = secret;

    delete process.env.RELAY_TARGET_AUTHORIZATION;
    res = await post();
    assert.strictEqual(res.statusCode, 503);
    assert.strictEqual(seen.length, 0);
    process.env.RELAY_TARGET_AUTHORIZATION = 'Bearer cursor-token\nEvil: yes';
    res = await post();
    assert.strictEqual(res.statusCode, 503);
    assert.strictEqual(seen.length, 0);
    process.env.RELAY_TARGET_AUTHORIZATION = 'raw-token-no-prefix';

    res = await post({ headers: {} });
    assert.strictEqual(res.statusCode, 403);
    res = await post({ headers: { 'x-signature': sign(secret, b64) }, body: b64, isBase64Encoded: true });
    assert.strictEqual(res.statusCode, 403, 'signature over the base64 text must not pass');
    assert.strictEqual(seen.length, 0);

    res = await post({ body: b64, isBase64Encoded: true, headers: { 'x-signature': goodSig } });
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(seen.length, 1);
    assert.strictEqual(seen[0].method, 'POST');
    assert.strictEqual(seen[0].url, '/hook');
    assert.strictEqual(seen[0].authorization, 'raw-token-no-prefix');
    assert.strictEqual(seen[0].contentType, 'application/json');
    assert.deepStrictEqual(seen[0].body, payload);

    upstreamStatus = 201;
    res = await post();
    assert.strictEqual(res.statusCode, 200);

    upstreamStatus = 302;
    res = await post();
    assert.strictEqual(res.statusCode, 502);
    assert.strictEqual(seen.length, 3, 'redirects are not followed');

    upstreamStatus = 500;
    res = await post();
    assert.strictEqual(res.statusCode, 502);

    process.env.RELAY_TARGET_URL = 'ftp://example.test/hook';
    res = await post();
    assert.strictEqual(res.statusCode, 502);
    assert.strictEqual(seen.length, 4);

    delete process.env.RELAY_TARGET_URL;
    const hanging = http.createServer(() => {});
    const hangPort = await listen(hanging);
    try {
      await relay.forward(`http://127.0.0.1:${hangPort}/hang`, payload, 'raw-token-no-prefix', 200);
      assert.fail('forward should time out');
    } catch (err) {
      assert.strictEqual(err.code, 'TIMEOUT');
    } finally {
      hanging.close();
    }

    assert.ok(statuses.length > 0);
    for (const code of statuses) {
      assert.notStrictEqual(code, 401);
      assert.notStrictEqual(code, 410);
    }
  } finally {
    relay.handler = prevHandler;
    server.close();
    if (prev.secret === undefined) delete process.env.CLICKUP_WEBHOOK_SECRET;
    else process.env.CLICKUP_WEBHOOK_SECRET = prev.secret;
    if (prev.auth === undefined) delete process.env.RELAY_TARGET_AUTHORIZATION;
    else process.env.RELAY_TARGET_AUTHORIZATION = prev.auth;
    if (prev.url === undefined) delete process.env.RELAY_TARGET_URL;
    else process.env.RELAY_TARGET_URL = prev.url;
  }

  console.log('clickup-relay tests passed');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
