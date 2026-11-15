# Driving Play Console in the Browser — Traps and Fixes

| Trap | Fix |
|------|-----|
| `get_page_text` returns only the side menu | Read with screenshots (scale 0.6) and `find` for refs |
| Unsaved form state lost on reload/navigation | Save after each form/page; confirm "Changes saved" toast |
| Opening a dialog shifts checkboxes under the cursor | Click one checkbox, screenshot, then the next |
| File upload tool limit (~10 MB) | AAB uploads go to the user: give the full path and say "drag it onto Upload app bundles" |
| reCAPTCHA (Google Groups, sometimes Play) | Hand to the user; continue on confirmation |
| "Do you want to restart your review?" | Cancel; explain the delay; proceed only on a new explicit yes |
| "Go to Publishing overview?" after Save | "Not now" unless you are about to submit |
| Intro carousels on first visit | Click through with Next / final button; Escape often does nothing |
| Release notes autocompletion | Select all + Delete before typing; keep the `<lang> … </lang>` tags |
| Several Google accounts in Chrome | Check the avatar/URL `/u/N/` before acting |
| Countries "select all" | Header checkbox selects every listed country; the overview also adds "rest of world" |
| Policy declarations, terms, IARC submit | The user ticks/submits these themselves |

## URL patterns

- App dashboard: `play.google.com/console/u/0/developers/<devId>/app/<appId>/app-dashboard`
- Track: `.../app/<appId>/tracks/<trackId>?tab=releases|countryAvailability|testers`
- Release prepare/review: `.../tracks/<trackId>/releases/<n>/prepare` and `/review`
- Publishing overview: `.../app/<appId>/publishing`
- App signing: `.../app/<appId>/keymanagement`

## Reporting progress

After each phase, tell the user in one line what is saved and what is not sent yet. Give the user's own action items as numbered steps with exact file paths and button names.
