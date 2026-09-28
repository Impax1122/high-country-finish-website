'use strict';

// Relays ClickUp webhook deliveries to an endpoint that requires an
// Authorization header. ClickUp signs the raw body but cannot set custom headers.
//
// ClickUp suspends a webhook immediately if the endpoint returns 401 or 410.
// This function must never use those status codes: bad signatures are 403,
// missing configuration is 503, and a failed forward is 502 (so ClickUp retries).

const crypto = require('crypto');
const http = require('http');
const https = require('https');

const DEFAULT_TARGET = 'https://api2.cursor.sh/automations/webhook/6d7dec1b-159d-5f4d-a8a5-1beb74206318';
const FORWARD_TIMEOUT_MS = 5000;

function rawBody(event) {
  const body = event && event.body != null ? event.body : '';
  if (typeof body !== 'string') return Buffer.alloc(0);
  // Netlify/Lambda base64-encodes the body for some content types. The HMAC
  // has to cover the exact bytes ClickUp sent, not the base64 text.
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

// Hex HMAC-SHA256 of the raw body, compared in constant time.
// Returns false (never throws) when the header is missing or malformed.
function verifySignature(secret, signature, body) {
  if (typeof secret !== 'string' || secret.length === 0) return false;
  if (typeof signature !== 'string') return false;
  const provided = signature.trim().toLowerCase();
  if (provided.length !== 64 || !/^[0-9a-f]{64}$/.test(provided)) return false;
  const expected = crypto.createHmac('sha256', secret).update(body).digest();
  const actual = Buffer.from(provided, 'hex');
  return crypto.timingSafeEqual(expected, actual);
}

function configured(secret, authorization) {
  if (typeof secret !== 'string' || secret.length === 0) return false;
  if (typeof authorization !== 'string' || authorization.length === 0) return false;
  // A newline in the header value would split the outbound request. Treat that
  // as "not configured" and refuse to forward.
  if (/[\r\n\0]/.test(authorization)) return false;
  return true;
}

function forward(targetUrl, body, authorization, timeoutMs) {
  return new Promise((resolve, reject) => {
    let settled = false;
    let url;
    try {
      url = new URL(targetUrl);
    } catch (err) {
      reject(Object.assign(new Error('forward failed'), { code: 'BAD_URL' }));
      return;
    }
    if (url.protocol !== 'https:' && url.protocol !== 'http:') {
      reject(Object.assign(new Error('forward failed'), { code: 'BAD_URL' }));
      return;
    }

    const lib = url.protocol === 'https:' ? https : http;
    const req = lib.request(
      {
        hostname: url.hostname,
        port: url.port || undefined,
        path: `${url.pathname}${url.search}`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': body.length,
          Authorization: authorization,
        },
      },
      (res) => {
        res.resume();
        done(null, { statusCode: res.statusCode || 0 });
      }
    );

    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      req.destroy();
      done(Object.assign(new Error('forward timeout'), { code: 'TIMEOUT' }));
    }, timeoutMs);

    req.on('error', (err) => {
      if (timedOut) done(Object.assign(new Error('forward timeout'), { code: 'TIMEOUT' }));
      else done(Object.assign(new Error('forward failed'), { code: (err && err.code) || 'ERROR' }));
    });
    req.end(body);

    function done(err, result) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (err) reject(err);
      else resolve(result);
    }
  });
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

function log(method, statusCode, detail) {
  // Status codes and a short reason only. Never the body, signature, or env values.
  if (detail) console.log(`clickup-relay method=${method} status=${statusCode} ${detail}`);
  else console.log(`clickup-relay method=${method} status=${statusCode}`);
}

async function handle(event) {
  const method = String((event && event.httpMethod) || '').toUpperCase();
  if (method !== 'POST') {
    log(method || 'UNKNOWN', 405);
    return respond(405, { error: 'method not allowed' }, { Allow: 'POST' });
  }

  const secret = process.env.CLICKUP_WEBHOOK_SECRET;
  const authorization = process.env.RELAY_TARGET_AUTHORIZATION;
  if (!configured(secret, authorization)) {
    log(method, 503, 'not_configured');
    return respond(503, { error: 'relay not configured' });
  }

  const body = rawBody(event);
  const signature = headerValue(event, 'x-signature');
  if (!verifySignature(secret, signature, body)) {
    log(method, 403);
    return respond(403, { error: 'forbidden' });
  }

  const target = process.env.RELAY_TARGET_URL || DEFAULT_TARGET;
  try {
    const upstream = await forward(target, body, authorization, FORWARD_TIMEOUT_MS);
    if (upstream.statusCode >= 200 && upstream.statusCode < 300) {
      log(method, 200, `upstream=${upstream.statusCode}`);
      return respond(200, { ok: true });
    }
    log(method, 502, `upstream=${upstream.statusCode}`);
    return respond(502, { error: 'upstream rejected' });
  } catch (err) {
    const reason = err && err.code === 'TIMEOUT' ? 'timeout' : 'forward_failed';
    log(method, 502, reason);
    return respond(502, { error: reason === 'timeout' ? 'upstream timeout' : 'upstream error' });
  }
}

exports.handler = async function handler(event) {
  try {
    return await handle(event);
  } catch (err) {
    log('POST', 502, 'internal');
    return respond(502, { error: 'relay failed' });
  }
};

exports.rawBody = rawBody;
exports.verifySignature = verifySignature;
exports.forward = forward;
exports.DEFAULT_TARGET = DEFAULT_TARGET;
exports.FORWARD_TIMEOUT_MS = FORWARD_TIMEOUT_MS;
