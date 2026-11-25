# Meta dashboard walkthrough (Unified login, as seen late 2026)

Exact places and labels, for driving the dashboard with a browser tool or guiding the user. Meta renames things often: if a label differs, look for the nearest match and screenshot before clicking.

## URLs

- App use cases: `https://developers.facebook.com/apps/<APP_ID>/use_cases/`
- Unified login setup: `https://developers.facebook.com/apps/<APP_ID>/use_cases/customize/Unified-Login-API-Setup/?use_case_enum=INSTAGRAM_BUSINESS`
- Roles: `https://developers.facebook.com/apps/<APP_ID>/roles/roles/`
- Basic settings (App secret): `https://developers.facebook.com/apps/<APP_ID>/settings/basic/`
- Tester invites (bot or sender account, on the web): `https://www.instagram.com/accounts/manage_access/` → tab **Tester invites**

Once the app belongs to a portfolio, Meta appends `&business_id=<PORTFOLIO_ID>` to these URLs; both forms work.

## Use cases → Customize (Instagram API)

Left panel: **Permissions and features**, **API setup with Unified login**, **API setup with Facebook login**, **Add more to this use case** (which offers only Webhooks; there is no way to add Instagram login back).

The Facebook login tab says: "API setup with Unified login is the recommended setup … API setup with Facebook login still works, but it's now legacy." It needs the Instagram account linked to a Facebook Page.

### Unified login page sections

1. **Configure your app**: "No compatible configurations found" → **Create new configuration** opens "Confirm login configuration details" (name "Instagram API (unified login)", General, System-user access token, never expire, assets Instagram accounts + Ad accounts, six permissions) → **Create from template**. Result: a row "Instagram API (unified login) · Instagram Login Compatible · Configuration ID … · Selected". Redirect URL / Login URL below are for third-party logins only.
2. **Generate access tokens**: table *Instagram account · Token · Webhook Subscription*. Tester accounts appear here automatically. **Generate token** opens a pop-up "Log in to Business Tools from Meta" with **Continue with <Facebook name>** / **Continue with Instagram**. The token is shown once. **Add account** first shows a dialog ("You can only add an Instagram professional account…", "Tokens can only be generated for public Instagram accounts") → Continue → login pop-up.
3. **Configure webhooks**: Callback URL, Verify token, "Attach a client certificate" toggle, **Remove subscription**, **Verify and save**. After saving: *Webhook fields* table (Field · Version · Test · Subscribe) with comments, live_comments, mentions, message_edit, message_reactions, **messages**, messaging_handover, messaging_postbacks, messaging_referral, messaging_seen, standby, story_insights. Each has a switch "Unsubscribed" → "Subscribed".
4. **Complete App Review**: links to review; only needed for the public.

Sections collapse ("See more" / chevron). Collapsed sections still exist in the accessibility tree but their refs report as off-screen: expand first, then `scroll_to`.

## Roles

Header shows the managing portfolio ("This app is managed by <portfolio>"). Filters: All roles, Administrators, Developers, Testers, **More → Analytics users / Instagram testers**. **Add People** dialog: Administrator, Developer, Tester, Analytics User, and under "Additional roles for this app" **Instagram Tester** → username search box (pick the exact match from the dropdown; similar names appear) → **Add**. New rows show status **Pending** until accepted on the web.

## App settings → Basic

App ID, **App secret** (masked, **Show**). Show opens "Please re-enter your password", which the user types. Same page: Display name, App domains, Contact email, Privacy policy URL, Terms URL, User data deletion, App icon, Category (all needed before Live).

## Browser-tool behaviour

- **Pop-ups opened by the page** (portfolio creation, login) appear as extra tabs. While one is open, navigation and JS in all tabs are paused. The agent can read it but not drive or close it, so ask the user to finish or close it by its title.
- **Pop-ups triggered by the agent's synthetic clicks are blocked**, so login windows need the user's own click.
- Clicking some controls (e.g. Customize, copy icons) writes to the OS clipboard. Tell the user.
- Wheel scrolling often hits the wrong container; `scroll_to` a ref works.
- The account id in a small screenshot is easy to misread. Take ids from the API (`/me/assigned_instagram_accounts`), not from pixels.
