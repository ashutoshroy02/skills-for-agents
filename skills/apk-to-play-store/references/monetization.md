# Ads and Pro Purchase

## AdMob

1. Create the app in AdMob (Android), then two ad units: Interstitial and Rewarded.
2. App ID (`~`) → `src/config.js` and the manifest meta-data (written by the sync script); unit IDs (`/`) → config; `testAds: false`.
3. Publish a GDPR message in AdMob → Privacy & messaging; without it EU users get no consent form and no ads.
4. Later, when the developer website is listed on Play, host `app-ads.txt` at its root as AdMob instructs.
5. Tell the user: never tap their own real ads, on any phone or emulator. Friends tapping normally is fine; a pattern of self-clicks is what gets accounts banned.

Ad rules we used: rewarded ads always optional (extra moves, lives, double coins); interstitials from level 15, at most every 3 levels, never twice within 2 minutes, never for Pro players.

## RevenueCat Pro

Entitlement `<app>_pro`, three products: `lifetime` (one-time), `yearly`, `monthly` (subscriptions), all in the `default` offering.

- **Testing first:** Test Store key + the three products created under the Test Store app; a test build simulates purchases. Debug APK name: `<app>-pro-test-debug.apk`.
- **Capacitor:** `@revenuecat/purchases-capacitor` + `@revenuecat/purchases-capacitor-ui`; `presentPaywallIfNeeded` for the paywall (fallback: buy the lifetime package directly), `presentCustomerCenter` for Manage Pro, and a Restore purchases button.
- **Play:** add the Google Play app in RevenueCat → `goog_` key into config → build with `BILLING`.
- **After the first AAB upload:** create the three Play products with the same IDs → Google Cloud service account JSON with Play Console financial/orders access into RevenueCat → import products → attach to entitlement and offering → publish a paywall that shows price, period and auto-renewal terms.
- RevenueCat → Integrations → AdMob only imports ad revenue into charts.

## Honest answers to give the user

- Ads in a website-installed APK still earn through AdMob even before Play; Pro cannot be bought until the Play products exist.
- Purchases are tied to the Google account: uninstall + reinstall, then Restore purchases, brings Pro back. Game progress stored on the phone does not come back.
