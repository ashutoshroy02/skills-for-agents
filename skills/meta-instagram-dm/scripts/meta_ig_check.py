#!/usr/bin/env python3
"""Checks for an Instagram DM webhook on Meta's Unified login. Standard library only.

Reads secrets from a .env file and never prints them (values are shown as length + first two
characters; the token is masked in any API response).

  python meta_ig_check.py env        [--env PATH]
  python meta_ig_check.py account    [--env PATH]
  python meta_ig_check.py subscribe  [--env PATH] [--fields messages]
  python meta_ig_check.py status     [--env PATH]
  python meta_ig_check.py verify     --url https://HOST/webhooks/instagram [--url http://127.0.0.1:PORT/webhooks/instagram] [--env PATH]
  python meta_ig_check.py deliveries [--path /webhooks/instagram] [--inspect http://127.0.0.1:4040]

env         which INSTAGRAM_* settings are set
account     GET /me/assigned_instagram_accounts: the id for INSTAGRAM_ACCOUNT_ID (200 = token works)
subscribe   POST /{id}/subscribed_apps?subscribed_fields=..., then GET to confirm
status      GET /{id}/subscribed_apps only
verify      Meta's webhook handshake against each URL: expect "200 123"
deliveries  webhook calls recorded by the ngrok agent's inspector, summarised (no user text)

Env names can be changed with --token-key / --account-key / --verify-key.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v27.0"


def load_env(path: str) -> dict[str, str]:
    p = pathlib.Path(path)
    if not p.is_file():
        sys.exit(f"no env file at {p.resolve()}")
    env: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def need(env: dict[str, str], key: str) -> str:
    value = env.get(key, "")
    if not value:
        sys.exit(f"{key} is empty or missing in the env file")
    return value


def call(method: str, url: str, token: str = "", mask: tuple[str, ...] = (),
         headers: dict[str, str] | None = None) -> tuple[int | None, str]:
    req = urllib.request.Request(url, method=method, headers=dict(headers or {}))
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status, body = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        return None, f"unreachable ({getattr(exc, 'reason', exc)})"
    for secret in mask:
        if secret:
            body = body.replace(secret, "<secret>")
    return status, body


def cmd_env(a, env):
    keys = sorted(k for k in env if k.startswith("INSTAGRAM_"))
    if not keys:
        print("no INSTAGRAM_* settings in the env file")
    for key in keys:
        v = env[key]
        print(f"{key:28} " + (f"set, {len(v)} chars, starts {v[:2]!r}" if v else "EMPTY"))


def cmd_account(a, env):
    token = need(env, a.token_key)
    status, body = call("GET", f"{GRAPH}/me/assigned_instagram_accounts", token, (token,))
    print("HTTP", status)
    print(body[:1500])
    if status == 200:
        ids = [d.get("id") for d in json.loads(body).get("data", [])]
        print(f"\n{a.account_key}={ids[0]}" if len(ids) == 1 else f"\naccount ids: {ids}")


def subscribed(a, env, post: bool):
    token, account = need(env, a.token_key), need(env, a.account_key)
    url = f"{GRAPH}/{account}/subscribed_apps"
    if post:
        q = urllib.parse.urlencode({"subscribed_fields": a.fields})
        status, body = call("POST", f"{url}?{q}", token, (token,))
        print("POST", status, body[:400])
    status, body = call("GET", url, token, (token,))
    print("GET ", status, body[:800])


def cmd_verify(a, env):
    verify = need(env, a.verify_key)
    q = urllib.parse.urlencode({"hub.mode": "subscribe", "hub.verify_token": verify, "hub.challenge": "123"})
    for url in a.url:
        status, body = call("GET", f"{url}?{q}", mask=(verify,), headers={"ngrok-skip-browser-warning": "1"})
        verdict = "OK" if status == 200 and body.strip() == "123" else \
            {404: "feature off or wrong path / stale process", 403: "verify token mismatch"}.get(status, "check")
        print(f"{url} -> {status} {body[:80]!r}  [{verdict}]")


def cmd_deliveries(a, env):
    status, body = call("GET", f"{a.inspect.rstrip('/')}/api/requests/http?limit=50")
    if status != 200:
        sys.exit(f"ngrok inspector not reachable at {a.inspect} ({status}): is the tunnel running?")
    found = 0
    for item in reversed(json.loads(body).get("requests", [])):
        req, resp = item.get("request", {}), item.get("response") or {}
        if not req.get("uri", "").startswith(a.path):
            continue
        found += 1
        uri = urllib.parse.urlsplit(req.get("uri", ""))
        query = urllib.parse.urlencode([(k, "<secret>" if k == "hub.verify_token" else v)
                                        for k, v in urllib.parse.parse_qsl(uri.query)])
        shown_uri = uri.path + (f"?{query}" if query else "")
        line = f"{item.get('start')} {req.get('method')} {shown_uri[:90]} -> {resp.get('status_code')}"
        if req.get("method") != "POST":
            print(line)
            continue
        raw = base64.b64decode(req.get("raw", ""))
        payload_bytes = raw.split(b"\r\n\r\n", 1)[1] if b"\r\n\r\n" in raw else raw
        try:
            payload = json.loads(payload_bytes)
        except ValueError:
            print(line, "(body not JSON)")
            continue
        print(line, f"object={payload.get('object')}")
        for entry in payload.get("entry", []):
            for m in entry.get("messaging", []) or []:
                msg = m.get("message") or {}
                kind = "ECHO (our reply)" if msg.get("is_echo") else "incoming"
                text = msg.get("text") or ""
                shown = repr(text[:120]) if msg.get("is_echo") else f"{len(text)} chars"
                atts = [f"{x.get('type')}{sorted((x.get('payload') or {}).keys())}" for x in msg.get("attachments") or []]
                print(f"   {kind}: sender={m.get('sender', {}).get('id')} recipient={m.get('recipient', {}).get('id')}"
                      f" text={shown} attachments={atts} other_keys={sorted(set(m) - {'sender', 'recipient', 'timestamp', 'message'})}")
            for c in entry.get("changes", []) or []:
                print(f"   change field={c.get('field')} keys={sorted((c.get('value') or {}).keys())}")
    if not found:
        print(f"no requests to {a.path} recorded: Meta hasn't called the tunnel (check roles, invites, subscriptions)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["env", "account", "subscribe", "status", "verify", "deliveries"])
    p.add_argument("--env", default=".env", help="path to the backend env file (default ./.env)")
    p.add_argument("--token-key", default="INSTAGRAM_ACCESS_TOKEN")
    p.add_argument("--account-key", default="INSTAGRAM_ACCOUNT_ID")
    p.add_argument("--verify-key", default="INSTAGRAM_VERIFY_TOKEN")
    p.add_argument("--fields", default="messages", help="subscribed_fields for subscribe")
    p.add_argument("--url", action="append", default=[], help="webhook URL for verify (repeatable)")
    p.add_argument("--path", default="/webhooks/instagram", help="webhook path for deliveries")
    p.add_argument("--inspect", default="http://127.0.0.1:4040", help="ngrok inspector base URL")
    a = p.parse_args()
    env = {} if a.command == "deliveries" else load_env(a.env)
    if a.command == "verify" and not a.url:
        sys.exit("verify needs at least one --url")
    {"env": cmd_env, "account": cmd_account, "verify": cmd_verify, "deliveries": cmd_deliveries,
     "subscribe": lambda a, e: subscribed(a, e, True), "status": lambda a, e: subscribed(a, e, False)}[a.command](a, env)


if __name__ == "__main__":
    main()
