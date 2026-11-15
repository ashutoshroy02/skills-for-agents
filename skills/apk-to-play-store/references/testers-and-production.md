# Testers and Production Access

## The rule

Personal developer accounts created after 13 November 2023 must run a closed test with **at least 12 testers opted in for the last 14 consecutive days** before they can apply for production. Organization accounts (D-U-N-S number) are exempt. Google does not supply testers.

## Google Group setup (preferred over email lists)

groups.google.com → Create group:
- Name `<App> Testers`, email `<app>-testers@googlegroups.com`
- Who can search: Anyone on the web
- Who can join: Anyone can join
- Who can view members: Group managers (testers cannot see each other's emails)
- Creation often shows a reCAPTCHA → hand to the user

Then in the closed track → Testers → Google Groups → add the group address → Save. This replaces any email list on that track.

## What testers do

1. Join the group with the Google account signed in on their Android phone's Play Store.
2. Open the opt-in link (`https://play.google.com/apps/testing/<package>`) → Become a tester. The link appears only after the closed test is approved.
3. Tap "Download it on Google Play" and install. The listing can take minutes to hours to appear after opting in.
4. Keep it installed for 14 days. Opening it a few times and sending feedback helps the production application.

If a tester installed a website APK earlier, they uninstall it and install from Play so the install counts (local progress is lost).

## Message the user can send to testers

> Hi! I'm testing my new game on Google Play and need your help for 14 days.
> 1. Join: https://groups.google.com/g/<app>-testers (use the Gmail on your phone)
> 2. Opt in: <opt-in link>
> 3. Install from the Play page that opens, and keep it installed for 14 days.
> Feedback welcome at <email>. Thank you!

## Sourcing testers

- Friends, family, colleagues: most reliable
- Tester-exchange communities (r/AndroidClosedTesting, "12 testers" Discord/Telegram groups): free, reciprocal, higher drop-out; aim for 15–20
- Paid tester gigs: discourage. Low-quality or fake accounts can get the production application rejected.

## Applying for production

After 14 days with ≥12 opted-in testers, Dashboard shows "Apply for production". Google asks about: how testers were recruited, how many engaged, feedback received and changes made, why the app is ready. Answer factually. Review takes about 7 days. If rejected, the usual fix is a longer test with more engaged testers.

## Timeline to give the user

| Day | Event |
|-----|-------|
| 0 | Closed test submitted |
| ~1–3 (up to 7+) | Approved; opt-in link appears |
| +14 | ≥12 testers kept it installed → Apply for production |
| +~7 | Production approved; publish (staged rollout recommended) |
