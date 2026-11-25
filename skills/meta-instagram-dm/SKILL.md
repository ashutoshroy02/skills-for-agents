---
name: meta-instagram-dm
description: >
  Connects an app's backend to Instagram DMs through Meta (Facebook) for Developers, so a bot
  account can receive DMs by webhook and reply: a "send us a reel/post to save it" door,
  a support inbox or any Instagram DM bot. Follows the Unified login setup Meta gives new apps
  (Instagram login is gone for them): business portfolio, login configuration, Instagram
  Tester roles, the never-expiring system-user token, account id, App secret, webhook verify,
  the messages field and the per-account subscribed_apps call, then testing in Development
  mode and going Live. Use whenever the user says "Instagram DM", "Instagram webhook",
  "Meta app setup", "Instagram Graph API messaging", "connect Instagram to my backend",
  "Unified login", "instagram_manage_messages", "Instagram tester", "subscribed_apps",
  "API setup with Instagram login is not available", or is stuck in the Meta developer
  dashboard on any Instagram messaging step.
domain: process
composable: true
yields_to: []
---

# Meta Instagram DM

You wire an Instagram professional account to a backend webhook the way that works for Meta apps created from late 2026 on, and you get it to a real DM round-trip (message in, reply out) before calling it done. Most tutorials online describe the retired Instagram login setup; following them wastes hours.

## Rules learned the hard way

1. **New Meta apps get Unified login, not Instagram login.** The dashboard shows a banner, "API setup with Instagram login is not available for newer apps". Because of that, ignore guides that use `graph.instagram.com`, `instagram_business_*` permissions, an "Instagram app secret" or a 60-day token refresh. Unified login uses `graph.facebook.com`, `instagram_basic` + `instagram_manage_messages`, the Meta **App secret**, and a system-user token that never expires.
2. **Replies go to `/{ig-user-id}/messages`, never `/me/messages`.** Because with a system-user token `/me` is the system user, not the Instagram account, so Meta rejects the send. Get the id from `GET /me/assigned_instagram_accounts`.
3. **Three separate subscriptions, all required:** the `messages` webhook field, the per-account "Webhook Subscription" switch, and `POST /{ig-user-id}/subscribed_apps?subscribed_fields=messages`. Because each one alone looks "done" in the dashboard while no DM arrives.
4. **Prove every step with a check before moving on** (table below). Because the dashboard rarely shows errors; a 200 from the API or the challenge echo is the only real signal.
5. **The user does the steps that need their identity:** typing passwords, finishing Meta/Instagram login windows, the password prompt behind "Show" on the App secret, accepting tester invites, and pasting the verify token into Meta's form. Give the exact page and button, wait for "done", then continue. Because an agent must not type credentials or tokens into web forms, and Meta opens these as pop-ups that browser automation can't drive.
6. **Ask before each outward or account-changing action:** creating the app or portfolio, creating the configuration, adding roles, subscribing, submitting App Review, switching to Live. Approval for one doesn't cover the next.
7. **Secrets go only into the backend env file, never into chat or logs.** When checking the env, print each value's length and first two characters, not the value; mask the token in any API response you print. Use `scripts/meta_ig_check.py`, which already does this.

## When to Use

- Building or fixing an Instagram DM bot, DM-to-save door, or Instagram inbox in any backend
- The Meta dashboard shows only "API setup with Unified login" / "with Facebook login"
- Webhook verified but no DMs arrive, or DMs arrive but replies fail
- Choosing permissions for App Review, or taking the app Live
- The user says "do it yourself" in the Meta dashboard: drive the browser, hand over the identity steps

## The setup, in order

Each step ends in a check. Don't start the next step until its check passes.

| # | Step | Who | Check that proves it |
|---|------|-----|----------------------|
| 0 | Backend has the webhook (verify GET, signed POST, send function) and an `https://` tunnel or deploy | agent | `GET <url>?hub.mode=subscribe&hub.verify_token=X&hub.challenge=123` → 404 while unconfigured (endpoint exists) |
| 1 | Bot Instagram account: professional, **public**, "Allow access to messages" on | user | Account shows as Business/Creator; not private |
| 2 | Meta app with use case **Manage messaging & content on Instagram**; connect a business portfolio | agent asks, user approves | Use cases → Customize → **API setup with Unified login** opens without the "portfolio is mandatory" warning |
| 3 | **1. Configure your app** → Create new configuration → **Create from template** | agent | Config shows "Instagram Login Compatible", "Selected" |
| 4 | App roles → Roles → **Add People** → **Instagram Tester**: the bot account and a separate sender account | agent | Both listed as Instagram Tester, status Pending |
| 5 | Accept each invite at `instagram.com/accounts/manage_access/` → **Tester invites**, logged in as that account | user | "Pending" disappears in Roles |
| 6 | **2. Generate access tokens** → **Generate token** next to the bot account → login window → **Continue with Instagram** as the bot | user (pop-up) | Token (starts `EA`, ~250 chars) pasted into env as `INSTAGRAM_ACCESS_TOKEN` |
| 7 | Account id from the API | agent | `meta_ig_check.py account` → HTTP 200 with one `id` → `INSTAGRAM_ACCOUNT_ID` |
| 8 | App settings → Basic → **App secret** → Show (password prompt) | user types password; value into env | `meta_ig_check.py env` shows `INSTAGRAM_APP_SECRET` set, 32 chars |
| 9 | Verify token: random string in env (`python -c "import secrets; print(secrets.token_urlsafe(32))"`) | agent | set in env |
| 10 | Restart the backend; confirm the **old process is gone** | agent/user | `meta_ig_check.py verify --url https://<host>/webhooks/instagram` → `200 123` locally and via the tunnel |
| 11 | **3. Configure webhooks**: Callback URL (agent types), Verify token (user pastes), **Verify and save** | both | Section 3 gets a green check |
| 12 | Webhook fields → `messages` → Subscribed | agent | Toast "Successfully subscribed to the messages … webhook field" |
| 13 | Section 2 → **Webhook Subscription** switch On for the bot account | agent | Toast "Webhooks turned on" |
| 14 | `meta_ig_check.py subscribe` | agent | `{"success":true}`, then `subscribed_fields: ["messages"]` |
| 15 | Real DM from the tester sender account to the bot | user | `meta_ig_check.py deliveries` shows the POST (200) **and** an echo with `is_echo: true` = your reply was sent |

Skip "Redirect URL" and "Login URL" in step 3 unless other businesses will log in to your app; a single bot account doesn't need them.

## Facts about the Unified login setup

- **Template configuration can't be edited in the dialog.** Next to `instagram_basic` and `instagram_manage_messages` it adds `ads_management`, `ads_read`, `instagram_content_publish`, `instagram_manage_comments` and ad-account access. Tell the user, then use it: it's the one the page accepts as "compatible". Trimming is possible later under Facebook Login for Business → Configurations.
- **Instagram Tester** is under "Additional roles for this app" in the Add People dialog. To list testers: Roles → More → Instagram testers.
- **Tester invites only show on the website**, not in the Instagram phone app.
- **Accounts with the tester role appear in "Generate access tokens" automatically**; "Add account" is only for accounts not yet listed. Meta: "Tokens can only be generated for public Instagram accounts."
- **Development mode delivers DMs from accounts with a role on the app.** Strangers' DMs need Advanced Access through App Review.
- **The dashboard's per-account switch subscribes ~17 fields**; the `subscribed_apps` call with `subscribed_fields=messages` narrows it to the one you handle.
- **`Authorization: Bearer <token>` works on `graph.facebook.com`.** The account-id call returning 200 proves it for your token.

## What arrives (observed payloads)

```json
{"object": "instagram", "entry": [{"id": "<bot ig id>", "time": 0, "messaging": [{
  "sender": {"id": "<user IGSID>"}, "recipient": {"id": "<bot ig id>"}, "timestamp": 0,
  "message": {"mid": "...", "text": "LINK-ABC123"}}]}]}
```

- **Reel shared into the chat:** `message.attachments[0]` = `{"type": "ig_reel", "payload": {"reel_video_id", "title", "url"}}`, and `url` is the public `https://www.instagram.com/reel/<code>/…` link.
- **Your own reply comes back as an echo:** sender = bot id, `message.is_echo: true`. Skip echoes in the handler. In debugging they confirm the send worked.
- **Signature:** header `X-Hub-Signature-256: sha256=<hex>` = HMAC-SHA256 of the **raw** body with the Meta App secret. Answer 200 fast and do work after, because Meta retries slow or failed deliveries.

Send a reply:

```http
POST https://graph.facebook.com/v27.0/{INSTAGRAM_ACCOUNT_ID}/messages
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
Content-Type: application/json

{"recipient": {"id": "<sender IGSID>"}, "message": {"text": "Saved."}}
```

Full handler code (FastAPI and Express), env layout and tests: `references/backend-contract.md`.

## Driving the dashboard with a browser tool

- **Page-opened pop-ups freeze navigation.** A leftover "Meta Business Suite" or login pop-up tab blocks every page load until it closes, and the agent can't close it. Ask the user to close that tab in the browser pane by name. In-page clicks and dialogs still work meanwhile.
- **Pop-ups the agent's click opens are blocked.** "Generate token", "Add account" and "Continue with …" windows open only from the user's own click, so hand those to the user.
- **The pages scroll inside a container.** Use `find` + `scroll_to` on a ref, not wheel scrolling. Collapsed sections ("See more") hide their switches: expand first.
- **Set a 1280×900 viewport** (the narrow pane collapses the tables), and reset it when done.
- **Clicking some dashboard controls writes to the clipboard.** Warn the user before they paste.
- Details and selectors: `references/dashboard-walkthrough.md`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Only "Unified login" and "Facebook login" tabs | New app; Instagram login retired | Use Unified login (this skill) |
| Unified page: "Business portfolio selection is mandatory" | App has no portfolio | Connect or create one (step 2) |
| Verify GET still 404 after "restarting" | Old backend process still holds the port with old env | Find the listener's start time (`Get-NetTCPConnection -LocalPort <port>` / `lsof -i :<port>`), stop that tree, start again |
| Verify and save fails | Backend not reachable over https, wrong path, or verify token mismatch | Run `verify` via the tunnel URL; 403 = token mismatch |
| POSTs arrive with 401 | Wrong secret in env | Use the Meta **App secret** (App settings → Basic) |
| No POST at all when DMing | Sender has no role, invite not accepted, a subscription missing, or "Allow access to messages" off | Check steps 1, 4–5, 12–14 |
| POST arrives, no reply, no echo | Send failed: `/me/messages`, missing account id, wrong host | Send to `graph.facebook.com/v27.0/{account id}/messages` |
| Reply error code 190 | Token revoked or wrong | Generate a new token (step 6) |
| "Invalid code" / blank page in the login window | Known Meta glitch adding accounts to portfolios | Close the window, retry; or add the account in Business settings → Accounts → Instagram accounts |

Debug order: tunnel inspector first (`meta_ig_check.py deliveries` reads ngrok's `127.0.0.1:4040`), then the backend log. The inspector shows whether Meta called at all, the status your backend returned, and the payload shape.

## Going public

1. **App settings → Basic:** app icon (1024×1024), category, Privacy policy URL, Data deletion URL.
2. **Business verification** of the portfolio (Security Centre). It needs official documents in the business's name, so start early.
3. **App Review:** Advanced Access for `instagram_basic` and `instagram_manage_messages`, with a screencast of the real flow (link, DM, reply, result in app). Rejections are common; fix the stated reason and resubmit.
4. **Switch the app to Live.**
5. **Privacy:** the bot stores sender IGSIDs and message ids. Disclose it in the privacy policy and store data-safety forms.

## Boundaries

- Covers Instagram messaging webhooks and replies. Publishing posts, comments moderation, ads and the Facebook Page Messenger platform are out of scope.
- Doesn't choose the product flow (linking codes, what replies say). It gives the plumbing and the checks.
- Doesn't handle credentials: the user types passwords, completes logins and pastes tokens into web forms.

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

Meta Instagram DM owns **process**: the order of setup steps, who does each one, and the check that closes it.

### When Meta Instagram DM Leads

- Any Meta dashboard or Instagram Graph API messaging setup or debugging
- Turning "Instagram DMs → my backend" into a working round-trip

### When Meta Instagram DM Defers

| Other Skill's Domain | What Meta Instagram DM Does |
|---------------------|-----------------------------|
| **Density** (caveman, compress) | Keeps the step table, the checks and every command intact; prose around them may shrink. |
| **Voice** (blogger, humanize) | Keeps exact button names, URLs and field names verbatim; tone may change. |
| **Craft** (harden, refactor) | Supplies the webhook contract; code-quality skills shape the handler's implementation. |
| **Content** (documenter) | Hands over the verified facts and payloads for setup docs. |

### Conflict Signal

> `⚠️ Process conflict: [skill] wants to [shorten/reorder] the setup steps. Kept every step and its check, because a skipped subscription or check fails silently in Meta.`

---

**Remember:** Unified login, `graph.facebook.com`, replies to `/{ig-user-id}/messages`, three subscriptions, a check after every step, and the user handles every password, login window and token paste.
