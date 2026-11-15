---
name: apk-to-play-store
description: >
  Ships a Capacitor Android app (a web game wrapped as an APK) from a working build to a Google
  Play closed test sent for review, following the exact workflow used for Castle Cascade:
  release ad and purchase config with a test-build switch, a release keystore, GitHub Actions
  that build/sign/release the APK and AAB and update the website download, emulator testing,
  creating the Play app, every App content form, store listing and screenshots, Play App
  Signing with your own key via PEPK, RevenueCat Play key, closed testing (countries, Google
  Group testers, release notes) and submitting for review, then the 12-testers-for-14-days
  rule. Use whenever the user says "apk to play store", "publish my game on Google Play",
  "put this on the Play Store", "Play Console forms", "data safety", "app signing", "PEPK",
  "closed testing", "12 testers", "upload the AAB", or has a new Play developer account and
  an APK ready.
domain: process
composable: true
yields_to: []
---

# APK to Play Store

You repeat the release path Castle Cascade took: one signing key protected forever, a CI pipeline that makes every release the same way, honest form answers taken from the SDKs in the build, and nothing sent to Google until the user says yes.

## Rules learned the hard way

1. **One signing key, created once, backed up twice.** The website APK, the GitHub Release and the Play upload are all signed with it, so every install can update every other. Because a lost or changed key means existing installs can never update. Keep it in a folder outside the repo, in CI secrets, and in a backup the user confirms.
2. **Release builds carry real IDs; test builds are forced to test IDs at build time.** Because test ad units earn nothing, the RevenueCat Test Store breaks real purchases, and a developer tapping real ads in a test build risks an AdMob ban. CI fails the release if test values are inside the APK.
3. **Write every Play answer into an answers file first.** Show it, then fill the forms from it. Because forms lose drafts, dialogs shift, and the user wants one place to check later ("do all forms, I check it later").
4. **The user does what only the user can or should do:** ticking legal declarations and terms, the content-rating submit, CAPTCHAs, identity checks, payments, passwords, and uploading files over the browser tool's ~10 MB limit (the AAB is ~22 MB). Give the exact path and button, wait for "done", then continue.
5. **Ask before anything goes to Google or is permanent:** creating the app, sending for review, restarting a review, deleting anything, downloading files. Approval for one action does not cover the next.

## When to Use

- An APK (or a web game with a Capacitor `android/` folder) exists and the user wants it on Google Play
- The user just got a Play developer account and asks "what now?"
- Any single step: signing key, CI release pipeline, website APK download, App content forms, store graphics, PEPK, closed test, testers

## The Workflow

| # | Step | Done when |
|---|------|-----------|
| 1 | Release config | Real AdMob + RevenueCat values in `src/config.js`; `TEST_BUILD` forces test values; test APK and release APK both build |
| 2 | Signing key | `.jks` + `keystore.properties` in a signing folder outside the repo; 4 GitHub secrets set; SHA-256 noted |
| 3 | CI pipeline | Push → test APK artifact; tag `vX.Y.Z` → signed APK + AAB, GitHub Release, website updated; `-rcN` tag → pre-release only |
| 4 | Website download | Download button serves the APK instantly with the right headers and shows version and size |
| 5 | Emulator test | APK installed on an emulator (MuMu/Android Studio) via adb, opened, ads load as test ads in the test build |
| 6 | Play app created | App exists with the exact package name; user ticked the declarations |
| 7 | App content + listing | Every "Finish setting up your app" item is ticked |
| 8 | Play App Signing | Own key uploaded via PEPK; Play shows the same SHA-256 as step 2 |
| 9 | Play billing key build | RevenueCat Play app → `goog_` key in config → new tag built with `BILLING` and `AD_ID` |
| 10 | Closed test | User uploaded the AAB; notes, countries, Google Group testers, feedback email saved |
| 11 | Submit | User said yes; Publishing overview shows "Changes in review" |
| 12 | After approval | Opt-in link shared; 12+ testers for 14 days; Play products + RevenueCat service account; apply for production |

### 1 — Release config

All store IDs live in one file; the test switch lives in the bundle step.

```js
// src/config.js
export default {
  testAds: false,
  admob: { android: { appId: 'ca-app-pub-XXXX~YYYY', interstitial: 'ca-app-pub-XXXX/1111', rewarded: 'ca-app-pub-XXXX/2222' } },
  revenuecat: { useTestStore: false, testStore: 'test_…', android: 'goog_…' },
  entitlement: '<app>_pro',
};
// src/native.js — esbuild: define { __TEST_BUILD__: process.env.TEST_BUILD === '1' }
if (__TEST_BUILD__) { CONFIG.testAds = true; CONFIG.revenuecat.useTestStore = true; }
```

- A sync script writes the AdMob app ID into `AndroidManifest.xml` meta-data. Normalize CRLF before regex-editing the manifest on Windows, because a `\n`-only regex silently matches nothing.
- Until the Play app exists in RevenueCat there is no `goog_` key: ship with purchases hidden (Pro offered only when the offering has products) and add the key in step 9.
- Explain to the user: a "debug" APK is the test build; the public APK is the signed release.

### 2 — Signing key

```bash
keytool -genkeypair -v -keystore <app>-release.jks -alias <alias> -keyalg RSA -keysize 4096 -validity 10000 \
  -storepass "$SP" -keypass "$KP" -dname "CN=<Developer>, O=<Brand>, C=<CC>"
keytool -list -v -keystore <app>-release.jks -alias <alias> -storepass "$SP" | grep SHA256
```

- Generate passwords as `cc` + 32 hex chars. Because a password starting with `-` is read as an option by keytool and PEPK (this broke once).
- Signing folder (e.g. `~/<app>-signing/`): `.jks`, `keystore.properties`, later `pepk.jar`, the `.pem`, a portable JDK if needed.
- Ask "upload the signing secrets to GitHub?" then set `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_PASSWORD`, `KEY_ALIAS` by piping from files, never on the command line. With several `gh` accounts, use `GH_TOKEN=$(gh auth token --user <owner>)`.
- Gitignore `android/keystore.properties`.

### 3 — CI pipeline

Copy `templates/android-release.yml` and `templates/publish-website-apk.sh`. Behavior:
- Push / PR → test APK (`TEST_BUILD=1`) as a run artifact
- Tag `v1.2.3` → versionCode `10203`, signed `assembleRelease bundleRelease`, `apksigner verify`, `jarsigner -verify` on the AAB, fail if test values are in the bundled JS, GitHub Release with APK + AAB, then the website script commits the APK and pushes `main`
- Tag `v1.2.3-rc1` → pre-release only (dry run, website untouched)
- Release published by hand → its APK goes to the website

Gradle reads signing from `KEYSTORE_PROPERTIES` env or `../keystore.properties`, version from `-PappVersionName/-PappVersionCode` (snippet: `references/signing-and-ci.md`). If the website job's push is rejected because the bot already pushed, fetch and merge, then push again.

### 4 — Website download

- APK at `docs/download/<app>.apk` (served by GitHub Pages and Vercel), `.gitignore` exception `!docs/download/*.apk`.
- `vercel.json` header block for the **exact path** (a `(.*)` source pattern failed the deploy): `Content-Type: application/vnd.android.package-archive`, `Content-Disposition: attachment`, `Cache-Control: max-age=0, must-revalidate`.
- Link with `download="<app>.apk"` so it starts at once; show "Version x · Android 7.0 or newer · about N MB" with **decimal MB** (what phones show).
- If the user wants no GitHub exposure, remove every GitHub link from the site.

### 5 — Emulator test

Connect adb to the running emulator (MuMu Player or Android Studio), `adb install -r` the test APK, open it, check the screens and that ads are test ads. On Windows, copy the APK to a short path first (long paths break adb). Never tap the emulator home screen blindly: a misclick can open a store page; verify nothing was installed.

### 6 — Create the Play app

Explain the account first: one-time $25 fee, personal account, one account can hold many apps, identity verification can take days. Then in the user's Chrome: Create app → name, language, Game/App, Free (cannot later become paid). The user ticks the policy and export declarations.

### 7 — App content forms and store listing

Fill `templates/play-console-answers.md` from `references/play-console-forms.md` (SDK → data map for AdMob and RevenueCat), save it next to the store graphics, then enter it in this order: privacy policy → app access → ads → content rating (user submits) → target audience 13+ → Data safety → advertising ID → government/financial/health/news → store settings → store listing.

Graphics (`references/store-assets.md`): icon 512×512, feature graphic 1024×500, 6 phone screenshots 900×1600 captured from the emulator, title screen first. Mark "Ready to send for review" on the listing. AI-content declaration: let the user review it.

Save after every form and check its tick. Because a reload lost the Data safety draft once.

### 8 — Play App Signing with your own key

Dashboard asks which key signs the app. Recommend **our own key** because the website APK is signed with it, so Play and website installs stay one app. Play App signing → "Use a different key" → "Export and upload a key from Java keystore":
1. User downloads `encryption_public_key.pem`; download `pepk.jar` after asking.
2. Run PEPK with passwords piped from `keystore.properties`:
   ```bash
   java -jar pepk.jar --keystore=<app>-release.jks --alias=<alias> --output=<app>-play-signing.zip \
     --include-cert --rsa-aes-encryption --encryption-key-path=encryption_public_key.pem
   ```
3. Upload the ZIP (small enough for the browser tool), Save, and check Play's app signing SHA-256 equals the keystore's.

Do this before the first AAB upload.

### 9 — RevenueCat Play key and the upload build

RevenueCat → project → Apps → add Google Play app with the package name → copy the public `goog_` key into config (`useTestStore: false`). Make sure the manifest has `com.android.vending.BILLING` and `com.google.android.gms.permission.AD_ID`. Bump and tag (e.g. `v1.0.2`), wait for CI, download the AAB, copy it to the user's Downloads. A RevenueCat → Integrations → AdMob link is fine; it only imports ad revenue into RevenueCat charts.

### 10 — Closed testing track

Test and release → Closed testing → the track (e.g. "Closed testing - Alpha") → Create release:
1. The user drags the AAB into "Upload app bundles"; wait for `10002 (1.0.2)`.
2. Release notes inside the tags: select all + delete first, then type `<en-GB>…</en-GB>`. Only claim what you verified (no level counts you did not check). Save as draft.
3. Countries/regions → Add → header checkbox (all, ~178) → Save.
4. Testers → Google Groups → `<app>-testers@googlegroups.com` (create it at groups.google.com: anyone can find, anyone can join, members visible to managers only; the user solves the CAPTCHA). Lists and Groups are exclusive; the group replaces the list.
5. Feedback URL or email → ask which address.
6. Preview: "no deobfuscation file" and "no native debug symbols" warnings are fine. Save → "Not now".

Set testers **before** submitting. Because changing them during review forces a restart.

### 11 — Submit

Publishing overview → read the change list to the user → ask "Send N changes for review?" → on yes click Submit → confirm in the dialog → wait for "Changes in review". If the dialog says **"Do you want to restart your review?"**, cancel and ask again with the cost spelled out.

### 12 — After approval

Tell the user (details: `references/testers-and-production.md`):
- Review usually takes 1–3 days, up to 7+. Then the opt-in link appears on the Testers tab.
- Testers join the group, opt in, install from the hidden Play page with the same Google account, and keep it 14 days. Website-APK installs should be replaced by the Play install.
- Personal accounts need 12+ testers for 14 straight days before "Apply for production". Google does not provide them; recruit 15–20.
- Then: Play products (`lifetime` one-time, `yearly`/`monthly` subscriptions), Google service account JSON in RevenueCat, attach to the entitlement and `default` offering, publish a paywall with subscription terms (`references/monetization.md`).

## Browser notes

Play Console's `get_page_text` returns only the menu; read with screenshots (scale 0.6) and `find`. Full trap list: `references/browser-automation.md`. After each step, tell the user in one line what is saved and what is not yet sent.

## Boundaries

- Ships the app that exists; does not redesign it.
- Does not solve CAPTCHAs, type passwords, pay, or tick legal declarations.
- Does not answer forms untruthfully or buy testers.
- Does not tap real ads, or delete repos/apps/data; the user does deletions.

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

apk-to-play-store owns **process** — the order of release steps, the checks between them, and the answers file given to Google.

### When apk-to-play-store Leads

- First Play Store publication, signing, CI release pipeline, App content, closed testing

### When apk-to-play-store Defers

| Other Skill's Domain | What apk-to-play-store Does |
|---------------------|------------------------|
| **Craft** (painter, logo-favicon) | Gives exact asset sizes; the craft skill designs icon, feature graphic, site. |
| **Voice/Content** (humanize, blogger) | Gives the facts and character limits for store text; the voice skill writes it. Claims stay verifiable. |
| **Density** (caveman, compress) | Status lines may be compressed; package names, IDs, paths and form answers stay exact. |

### Conflict Signal

> `⚠️ Process conflict: [skill] wants [X] but Play requires [Y]. Kept [Y]; [X] applied where allowed.`

---

**Remember:** one key backed up twice, real IDs only in release, answers file before forms, the user ticks declarations and solves CAPTCHAs, and nothing goes to Google without a fresh yes.
