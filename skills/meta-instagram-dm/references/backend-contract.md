# Backend contract for an Instagram DM webhook (Unified login)

What the backend must do so Meta's checks pass and replies go out. Adapt names to the project; keep the behaviour.

## Env

| Name | Value | Notes |
|---|---|---|
| `INSTAGRAM_APP_SECRET` | Meta **App secret** (App settings → Basic) | Verifies `X-Hub-Signature-256` |
| `INSTAGRAM_VERIFY_TOKEN` | random string you make | Same string typed in Meta's webhook form |
| `INSTAGRAM_ACCESS_TOKEN` | system-user token from "Generate access tokens" | Starts `EA`, never expires; only used to send |
| `INSTAGRAM_ACCOUNT_ID` | `id` from `GET /me/assigned_instagram_accounts` | Send path, and to ignore events for other accounts |
| `INSTAGRAM_HANDLE` | bot username, no `@` | Shown to users ("DM @handle") |
| `INSTAGRAM_GRAPH_BASE_URL` | `https://graph.facebook.com/v27.0` | Version bumps over time |

Treat the feature as off (webhook 404) until secret, verify token, access token and handle are all set. Because a half-configured bot that receives but can't verify or reply confuses users and Meta's checks.

## Endpoints

1. `GET /webhooks/instagram`: if `hub.mode == "subscribe"` and `hub.verify_token` equals the env value (constant-time compare), return `hub.challenge` as **plain text**, else 403.
2. `POST /webhooks/instagram`:
   - Read the **raw bytes** first; the signature covers exactly those bytes.
   - `expected = "sha256=" + hex(HMAC_SHA256(app_secret, raw))`; constant-time compare with the header; 401 on mismatch.
   - Parse JSON; ignore anything where `object != "instagram"`.
   - For each `entry[].messaging[]` (and `entry[].changes[]` with `field == "messages"`, which older payloads use): skip `message.is_echo`, skip events whose recipient isn't your account id, skip deleted/unsupported messages, de-duplicate by `message.mid` (Meta redelivers).
   - Answer **200 for every correctly signed POST**, even if handling one message failed (log it). Because a non-200 makes Meta retry the same payload, and repeated failures can disable the subscription.
   - Send replies **after** answering (background task / queue).
3. Send: `POST {GRAPH}/{INSTAGRAM_ACCOUNT_ID}/messages`, header `Authorization: Bearer <token>`, body `{"recipient": {"id": sender_igsid}, "message": {"text": text}}`. Keep text ≤ 1000 bytes. Never raise from the background sender: log status and Meta's `error.code`/`error_subcode`/`message`, never the token or user text.

## FastAPI sketch

```python
import hashlib, hmac, json
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
import httpx

router = APIRouter()

@router.get("/webhooks/instagram", response_class=PlainTextResponse)
async def verify(mode: str = Query("", alias="hub.mode"),
                 token: str = Query("", alias="hub.verify_token"),
                 challenge: str = Query("", alias="hub.challenge")):
    s = settings()
    if not s.instagram_enabled:
        raise HTTPException(404)
    if mode != "subscribe" or not hmac.compare_digest(token.encode(), s.instagram_verify_token.encode()):
        raise HTTPException(403)
    return PlainTextResponse(challenge)

def signature_ok(secret: str, header: str | None, raw: bytes) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    want = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(want, header[7:])

@router.post("/webhooks/instagram")
async def receive(request: Request, background: BackgroundTasks):
    s = settings()
    if not s.instagram_enabled:
        raise HTTPException(404)
    raw = await request.body()
    if not signature_ok(s.instagram_app_secret, request.headers.get("x-hub-signature-256"), raw):
        raise HTTPException(401)
    payload = json.loads(raw)
    for msg in message_events(payload, s.instagram_account_id):  # skips echoes, dedupes by mid
        reply = await handle(msg)                                 # your product logic
        if reply:
            background.add_task(send_reply, msg.sender, reply)
    return {"status": "ok"}

async def send_reply(recipient: str, text: str) -> None:
    s = settings()
    account = s.instagram_account_id.strip() or "me"   # "me" only works for Instagram-login tokens
    url = f"{s.instagram_graph_base_url.rstrip('/')}/{account}/messages"
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(url, json={"recipient": {"id": recipient}, "message": {"text": text}},
                             headers={"Authorization": f"Bearer {s.instagram_access_token}"})
        if r.is_error:
            log.warning("instagram reply not sent: HTTP %s %s", r.status_code, r.text[:200])
    except Exception as exc:
        log.warning("instagram reply not sent: %s", type(exc).__name__)
```

## Express sketch

```js
app.get('/webhooks/instagram', (req, res) => {
  const ok = req.query['hub.mode'] === 'subscribe' &&
    safeEqual(req.query['hub.verify_token'] ?? '', process.env.INSTAGRAM_VERIFY_TOKEN);
  return ok ? res.type('text/plain').send(req.query['hub.challenge']) : res.sendStatus(403);
});

app.post('/webhooks/instagram', express.raw({ type: '*/*' }), async (req, res) => {
  const want = 'sha256=' + crypto.createHmac('sha256', process.env.INSTAGRAM_APP_SECRET)
    .update(req.body).digest('hex');
  if (!safeEqual(req.get('x-hub-signature-256') ?? '', want)) return res.sendStatus(401);
  res.sendStatus(200);                       // answer first, work after
  const payload = JSON.parse(req.body.toString('utf8'));
  for (const msg of messageEvents(payload)) handle(msg).then(r => r && sendReply(msg.sender, r));
});

async function sendReply(recipient, text) {
  const url = `https://graph.facebook.com/v27.0/${process.env.INSTAGRAM_ACCOUNT_ID}/messages`;
  const r = await fetch(url, { method: 'POST',
    headers: { Authorization: `Bearer ${process.env.INSTAGRAM_ACCESS_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient: { id: recipient }, message: { text } }) });
  if (!r.ok) console.warn('instagram reply not sent', r.status, (await r.text()).slice(0, 200));
}
```

`safeEqual` = length check + `crypto.timingSafeEqual`.

## Tests worth having

- Verify GET: right token → challenge as plain text; wrong token → 403; feature off → 404.
- POST: bad/missing signature → 401; signed body → 200; signature computed over the raw bytes (re-serialised JSON must fail).
- Echo messages and other accounts' events are ignored; a repeated `mid` is handled once.
- Send path is `/{account id}/messages` when the id is set (a unit test with a mock transport).
- One failing message doesn't fail the delivery (still 200).
- Logs never contain the token, app secret or message text.

## Linking DMs to app users (common pattern)

The sender arrives as an Instagram-scoped id (IGSID), not your user. A one-time code is the simplest bridge: the app shows a short code (e.g. `LINK-` + 6 chars, 15-minute expiry, rate-limited); the user DMs it to the bot; the webhook maps IGSID → user and deletes the code; later DMs from that IGSID act for that user. Reply to unlinked senders at most once an hour, so the bot doesn't spam.
