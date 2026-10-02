'use strict';

// Shared fixtures for the relay tests: one local HTTP server that plays every
// bot's wake target (/wake/<bot>) and the ClickUp API (/api/v2/...).

const crypto = require('crypto');
const http = require('http');

const BOT_ENV = {
  front_desk: 'WAKE_FRONT_DESK',
  billing: 'WAKE_BILLING',
  job_coordinator: 'WAKE_JOB_COORDINATOR',
  chief_of_staff: 'WAKE_CHIEF_OF_STAFF',
  web_presence: 'WAKE_WEB_PRESENCE',
};

const MANAGED_ENV = [
  'CLICKUP_WEBHOOK_SECRET', 'CLICKUP_WEBHOOK_SECRET_JOBS', 'CLICKUP_API_TOKEN', 'CLICKUP_API_BASE',
  'GMAIL_RELAY_SECRET', 'RELAY_PAUSED', 'RELAY_TARGET_URL', 'RELAY_TARGET_AUTHORIZATION',
].concat(...Object.values(BOT_ENV).map((p) => [`${p}_URL`, `${p}_AUTH`]));

function sign(secret, body) {
  return crypto.createHmac('sha256', secret).update(body).digest('hex');
}

async function startServer() {
  const state = {
    wakes: [],
    apiCalls: [],
    tasks: {},
    listPages: [],
    targetStatus: 200,
    apiStatus: 200,
    hangApi: false,
  };
  const server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      const body = Buffer.concat(chunks).toString('utf8');
      const url = new URL(req.url, 'http://x');
      if (url.pathname.startsWith('/wake/')) {
        state.wakes.push({
          bot: url.pathname.slice(6),
          authorization: req.headers.authorization,
          contentType: req.headers['content-type'],
          json: JSON.parse(body),
        });
        res.writeHead(state.targetStatus);
        res.end('ok');
        return;
      }
      if (url.pathname.startsWith('/api/v2/')) {
        state.apiCalls.push({ path: url.pathname, query: url.search, authorization: req.headers.authorization });
        if (state.hangApi) return; // never answers
        if (state.apiStatus !== 200) {
          res.writeHead(state.apiStatus);
          res.end('{}');
          return;
        }
        let m = /^\/api\/v2\/task\/([^/]+)$/.exec(url.pathname);
        if (m) {
          const task = state.tasks[decodeURIComponent(m[1])];
          res.writeHead(task ? 200 : 404, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(task || { err: 'not found' }));
          return;
        }
        m = /^\/api\/v2\/list\/([^/]+)\/task$/.exec(url.pathname);
        if (m) {
          const page = Number(url.searchParams.get('page') || 0);
          const tasks = state.listPages[page] || [];
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ tasks, last_page: page >= state.listPages.length - 1 }));
          return;
        }
      }
      res.writeHead(404);
      res.end();
    });
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  return { server, state, base };
}

function saveEnv() {
  const saved = {};
  for (const k of MANAGED_ENV) saved[k] = process.env[k];
  return saved;
}

function restoreEnv(saved) {
  for (const k of MANAGED_ENV) {
    if (saved[k] === undefined) delete process.env[k];
    else process.env[k] = saved[k];
  }
}

// Point every bot at /wake/<bot> with its own Authorization value.
function configureTargets(base) {
  for (const k of MANAGED_ENV) delete process.env[k];
  for (const [bot, prefix] of Object.entries(BOT_ENV)) {
    process.env[`${prefix}_URL`] = `${base}/wake/${bot}`;
    process.env[`${prefix}_AUTH`] = `Bearer key-${bot}`;
  }
  process.env.CLICKUP_API_BASE = `${base}/api/v2`;
  process.env.CLICKUP_API_TOKEN = 'pk_test_token';
}

function reset(state) {
  state.wakes.length = 0;
  state.apiCalls.length = 0;
  state.targetStatus = 200;
  state.apiStatus = 200;
  state.hangApi = false;
}

module.exports = { BOT_ENV, sign, startServer, saveEnv, restoreEnv, configureTargets, reset };
