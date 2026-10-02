# High Country Finish and Repair CO — website

Static marketing site for a Denver / Front Range commercial sign and vinyl graphics installer.
Plain HTML, CSS and JavaScript — no build step. Deployed to Netlify from the repository root.

## Layout

```
index.html            Homepage (source of truth for shared CSS, nav and footer — see docs/BRAND.md)
services.html         Services hub
services/*.html       One page per service
portfolio.html        Full portfolio grid
about-us.html, our-process.html, service-area.html, get-a-quote.html, blog.html, privacy.html
blog/*.html           Articles
404.html              Custom not-found page
images/               Photos, logo, share card (og-home.jpg), favicons
sitemap.xml, feed.xml, robots.txt, netlify.toml, favicon.ico
partials/             nav.html and footer.html — the single source for the shared nav/footer
build.js              Copies the partials into every page, regenerates sitemap.xml and feed.xml (node build.js; --check on deploy)
netlify/              Bot wake-up relays: functions/ (clickup-relay, gmail-relay) and lib/ (server-side only; not pages)
automation/gmail-wake/ Google Apps Script that wakes the bots on new Gmail (source only; not served)
docs/                 Brand guide, launch guide, SEO audit/work log, e-commerce roadmap, image credits and build logs (not served)
scripts/              Historical one-off build/patch scripts, plus the relay tests (not served)
```

## Editing

* The site nav and footer live in `partials/nav.html` and `partials/footer.html`. Edit the partial,
  then run `node build.js` to copy it into every page (each page holds the block between
  `<!-- build:nav -->` / `<!-- build:footer -->` markers). `node build.js --check` reports stale
  pages and is what Netlify runs on deploy, so a forgotten build fails loudly instead of shipping.
* The shared CSS is still duplicated per page; when you change it, apply the change to every page (run `node build.js --check` to list them).
* Save files as UTF-8 without a byte-order mark.
* Blog posts carry `BlogPosting` JSON-LD; `build.js` reads it to build `feed.xml` and the sitemap's
  image entries, so keep the schema block on every new post (copy an existing post as the template).
* Third-party photos must be public domain or CC0 and listed in `docs/IMAGE_CREDITS.md`.
* The quote forms post to Formspree (`https://formspree.io/f/mqeydnkg`) and include a `_gotcha`
  honeypot field for spam.
* `netlify.toml` blocks `/docs/*`, `/scripts/*` and `/README.md` from being served and sets the
  security headers. If you add a third-party script or embed, extend the Content-Security-Policy there.

## Deploying

Push to `master`; Netlify publishes the repository root.

## Bot wake-up relays (ClickUp and Gmail)

Two Netlify Functions wake the High Country bots when something happens. Visitors
never see them. The routing follows the "How you get woken" table in the High
Country Bot Rulebook (Oct 2, 2026); any event not on it is dropped with `200`.

| Endpoint | Called by | Signature |
|---|---|---|
| `https://highcountryfinish.com/.netlify/functions/clickup-relay` | ClickUp webhooks (HQ list and Jobs list) | `X-Signature`: hex HMAC-SHA256 of the raw body with `CLICKUP_WEBHOOK_SECRET` or `CLICKUP_WEBHOOK_SECRET_JOBS` |
| `https://highcountryfinish.com/.netlify/functions/gmail-relay` | The Gmail wake script (`automation/gmail-wake/`) | `X-Signature`: hex HMAC-SHA256 of the raw body with `GMAIL_RELAY_SECRET` |

### Routing

Bot on duty by Jobs status (case-insensitive):

| Status | Bot on duty |
|---|---|
| New, Waiting on client, Quoted, Paid | Front Desk |
| Pricing, Price review, Estimate, Send estimate, Deposit, Send deposit, Installed, Send invoice, Invoiced | Billing |
| Won, Scheduled | Job Coordinator |
| Closed, Lost, On hold | nobody |

| Event | Who is woken |
|---|---|
| Jobs card moves to a new status | Bot on duty for the new status (no ClickUp lookup) |
| Alex comments on a Jobs card | Bot on duty for the card's current status (one ClickUp GET) |
| HQ card status change, or Alex comments on an HQ card | Bot named in the title prefix: `[Front Desk]`, `[Billing]` (old `[Estimator]` too), `[Job Coordinator]`, `[Chief of Staff]`, `[Web Presence]`. Other or retired names: nobody |
| A comment starting with `[Name]` (bot comment; all bots post with Alex's ClickUp token), a new card, a field change, other lists, other events | nobody |
| Gmail `new_thread` (not from Alex, not automated, not a receipt) | Front Desk |
| Gmail `reply` on a thread | Bot on duty for the Jobs card whose description holds the thread id; Front Desk if that job is Closed or Lost; **Front Desk if no job card matches**; nobody if On hold |
| Gmail `alex_sent` (Alex sent a draft) | That job's bot on duty; no matching job: nobody |

`Alex (via CoS): ...` comments have no bracket prefix, so they count as Alex.
Thread lookups read the Jobs list once (paginated, closed cards included).

Each wake is a POST of a small normalized JSON (not the raw ClickUp body):
`source, event, list, task_id, task_name, task_url, new_status, previous_status,
comment_text (first 500 chars), thread_id, message_id, from, subject, at, bot`.

### Status codes

Never `401` or `410` (ClickUp suspends a webhook immediately on either). Bad or
missing signature `403`. No secret configured `503`. Failed forward, or a
transient ClickUp lookup failure, `502` so the sender retries. A bot with no wake
target, a bad ClickUp token, or a dropped event is `200` and logged. Logs hold
status codes, event kinds, task ids and reasons only: never bodies, names,
comment text, signatures or env values.

### Environment variables

Set these in **Netlify → Site configuration → Environment variables**, then
redeploy. They are not committed.

| Variable | Purpose |
|---|---|
| `CLICKUP_WEBHOOK_SECRET` | Secret of the HQ list ClickUp webhook (existing). |
| `CLICKUP_WEBHOOK_SECRET_JOBS` | Secret of the Jobs list ClickUp webhook (optional second secret). |
| `CLICKUP_API_TOKEN` | ClickUp personal token, for card lookups. |
| `GMAIL_RELAY_SECRET` | Shared with the Gmail script's Script Property of the same name. |
| `WAKE_FRONT_DESK_URL` / `WAKE_FRONT_DESK_AUTH` | Front Desk's wake webhook URL and full `Authorization` header value (sent verbatim). |
| `WAKE_BILLING_URL` / `WAKE_BILLING_AUTH` | Billing's. |
| `WAKE_JOB_COORDINATOR_URL` / `WAKE_JOB_COORDINATOR_AUTH` | Job Coordinator's. |
| `WAKE_WEB_PRESENCE_URL` / `WAKE_WEB_PRESENCE_AUTH` | Web Presence's. |
| `WAKE_CHIEF_OF_STAFF_URL` / `WAKE_CHIEF_OF_STAFF_AUTH` | Optional. If unset, Chief of Staff keeps the original relay target: `RELAY_TARGET_URL` (default `https://api2.cursor.sh/automations/webhook/6d7dec1b-159d-5f4d-a8a5-1beb74206318`) with `RELAY_TARGET_AUTHORIZATION`. |
| `RELAY_PAUSED` | `true` makes both endpoints drop everything with `200` (the pause switch). |

### Tests

`node scripts/test-clickup-relay.js`, `node scripts/test-gmail-relay.js` and
`node scripts/test-gmail-wake.js` cover every routing row, signatures, the pause
switch, missing targets and the Gmail classification. Netlify runs them on every
deploy after `node build.js --check`.

