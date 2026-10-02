# Gmail wake script (Google Apps Script)

Wakes the High Country bots on new email, per the Bot Rulebook's "How you get
woken" table. It runs inside Google as **alexdrew@highcountryfinish.com**, checks
Gmail every 5 minutes, and POSTs one small signed event per new message to
`https://highcountryfinish.com/.netlify/functions/gmail-relay`. The relay decides
which bot to wake (see the repo README).

It only reads mail (`gmail.readonly`). It never sends, labels, moves or deletes
anything.

## What it sends

| Message | Kind sent |
|---|---|
| Alex sent it (Sent label, from alexdrew@highcountryfinish.com) | `alex_sent` |
| First message of a thread, from someone else, not automated | `new_thread` |
| Later message on a thread, from someone else, not automated | `reply` |
| Automated: no-reply / noreply / do-not-reply / mailer-daemon / postmaster / notifications / bounces senders, `List-Unsubscribe` or `List-Id`, `Precedence: bulk/list/junk`, `Auto-Submitted`, Google or Yelp system mail | nothing |
| Yelp lead messages from `messaging.yelp.com` | treated as client mail (`new_thread` / `reply`) |
| Labeled `Receipts` (or `Receipts/...`), unsent drafts, spam, trash, mail from Alex that isn't in Sent | nothing |

Each event is `{kind, thread_id, message_id, from, subject, at}`, signed with
`X-Signature` = hex HMAC-SHA256 of the body keyed with `GMAIL_RELAY_SECRET`.

## Set up (once)

1. Signed in as **alexdrew@highcountryfinish.com**, open https://script.google.com
   and click **New project**. Name it `HC Gmail wake`.
2. **Project Settings** (gear) → tick **Show "appsscript.json" manifest file in editor**.
3. In the editor, replace `Code.gs` with this folder's `Code.gs`, and
   `appsscript.json` with this folder's `appsscript.json`. Save. (The manifest turns
   on the Gmail advanced service and limits the script to three permissions.)
4. **Project Settings** → **Script Properties** → add:
   - `RELAY_URL` = `https://highcountryfinish.com/.netlify/functions/gmail-relay`
   - `GMAIL_RELAY_SECRET` = the same long random string as Netlify's `GMAIL_RELAY_SECRET`
5. Back in the editor, pick `install` in the function menu and click **Run**.
   Approve the access prompt (read Gmail, connect to an external service, manage
   its own triggers). If Google warns the app isn't verified, click **Advanced** →
   **Go to HC Gmail wake**; it's your own script.
6. **Triggers** (clock icon) should now show one `checkMail` trigger, every 5 minutes.

`install` starts the marker at "now", so old mail is not replayed.

## Pause and resume

- **Pause:** Triggers → delete the `checkMail` trigger (or run `uninstall`). Also set
  `RELAY_PAUSED=true` in Netlify for a full pause.
- **Resume:** run `install` again. The script keeps its `LAST_CHECK_MS` marker and
  picks up mail from its last check. After a long pause, delete `LAST_CHECK_MS`
  first if you don't want the backlog to wake the bots.

## How it keeps its place

- `LAST_CHECK_MS`: time of the newest message handled. Each run looks back 2 minutes
  further to catch late-indexed mail; `SEEN_IDS` (last 1,000 ids) stops repeats.
- If the relay doesn't answer `2xx`, the run stops at that message and retries it
  next run. After 6 failed tries (~30 minutes) that message is skipped and logged
  in **Executions**, so one bad message can't block the inbox.
- Up to 50 messages are handled per run; the rest wait for the next run.
