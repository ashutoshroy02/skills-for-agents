---
name: video-editor
description: >
  AI video and Shorts editing: workspace rules plus the `vk` toolkit (ffmpeg, faster-whisper, OpenCV).
  Use whenever the user wants to edit, cut, trim, caption or subtitle a video, remove pauses, silences or
  retakes, reframe 16:9 to 9:16, make YouTube Shorts, Instagram Reels or TikToks, clip highlights from a long
  video or podcast, add music or a logo, fix loudness, compress or convert a video, or check a render, even if
  they only drop a file and say "make this a short". Every new edit gets its own subfolder in
  C:\Users\ashu2\Music\video-edit\videos. Routes brand talking-head reels with motion graphics to
  it-reelsmaker and programmatic animation to the Remotion skills.
domain: process
composable: true
yields_to: []
---

# Video Editor: one folder per video, edits as data, verify by looking

Edit like a careful human editor who happens to have a terminal: decide from the transcript, cut by the audio, check every result with your own eyes (contact sheets you Read) and with numbers (LUFS, duration, sync). The `vk` CLI does the deterministic work; you make the editorial calls and keep the user in the loop.

## The five rules

1. **Subfolder first.** For any new edit, the first command is `vk new "<short title>" --from <files or URL>`, then `cd` into the printed `videos/<date>-<slug>/` and keep every output inside it, because sources, intermediates and finals of different videos then never mix, `vk clean` can free space safely, and the folder is the video's whole history.
   - User drops `D:\clips\IMG_4012.MOV` with "make a short" → `vk new "gym tip short" --from "D:\clips\IMG_4012.MOV"`.
   - Files in the workspace `inbox/` are moved (not copied) into `source/`, which saves disk.
   - A revision of the same video goes in the same folder; a different video gets a new folder. Several Shorts mined from one long source share that source's folder (`exports/clip-01-…`), so the big file is stored once.
2. **Sources are read-only.** Derived files go to `work/` (regenerable) or `exports/` (deliverables), because the original is the only thing that cannot be recreated.
3. **Plan → "yes" → cut.** Show the edit plan and wait for approval before cutting or the full render, because renders are slow on this machine and the user's taste decides. The plan covers the hook, kept ranges with source timecodes, what was dropped and why, pacing, speed, captions style, reframe, music, and the final length.
4. **Verify by looking and measuring.** After every cut and render, run `vk sheet <file>` and Read the PNG; `vk render` verifies size, fps, codec, −14 LUFS, true peak, A/V sync and faststart by itself. Report the numbers, because "looks good" hides defects.
5. **Respect the machine.** It has an i3-1115G4 (2 cores/4 threads), 8 GB RAM, Intel UHD graphics with no NVIDIA/CUDA, and about 7 GB free on C:. Render `--preset preview` (540×960) for review before the full render, use `--hw` (Quick Sync) when speed matters, check `vk status` before big jobs, and after the user approves the final, offer `vk clean <video> --yes`.

## Workspace

```
C:\Users\ashu2\Music\video-edit\        ← workspace (marker: .vk-workspace; CLAUDE.md has the house rules)
├── inbox\                              ← user drops raw files here; vk new moves them out
├── library\                            ← shared across videos: brands\ fonts\ music\ sfx\ luts\ overlays\
└── videos\<YYYY-MM-DD>-<slug>\         ← ONE folder per video (a motion-graphics video adds remotion\ here)
    ├── project.md   brief · plan · decisions log · outputs · open items (keep it current)
    ├── vk.json      machine state (sources with probe info, outputs with verify results)
    ├── source\      originals, never modified
    ├── work\        transcripts, EDLs, cut.mp4, captions.ass, sheets, frames (regenerable media)
    ├── assets\      this video's own logo, music, overlays, B-roll
    └── exports\     finals: <slug>-<preset>.mp4 (never overwritten: -2, -3 …)
```

## Routing: which tool does what

| Task | Use |
|---|---|
| Cuts, pause/retake removal, captions, 9:16 reframe, music, loudness, export, compress, convert, clip mining | `vk` (this skill) |
| Talking-head brand reel with motion graphics, designed scenes, face-aware layout, brand profiles | the **it-reelsmaker** skill, with the video subfolder as its PROJECT_ROOT and `<workspace>\remotion` as its Remotion project |
| Math/science explainers, animated equations, graphs, charts, counters, 3D, narrated Manim-style scenes | the **manimgx** skill: scene in `videos\<slug>\manim\scene.py`, `manimgx render` → `work\`, finished by `vk render … --preset reels --reframe none --fps 30`. Reference build: `videos\2026-10-16-manimgx-demo` |
| Animated titles, explainers, data-driven or programmatic motion graphics | the **remotion:*** skills, with the Remotion project inside the video folder (`videos\<slug>\remotion\`, scaffolded by `npx create-video@latest --yes --blank --no-tailwind remotion`) and renders into the video's `exports\`. Reference build: `videos\2026-10-11-strongest-currencies\remotion` (voice → whisper word times → cue words → frames, synthesised music/SFX, −14 LUFS mix) |
| An ffmpeg operation `vk` lacks (GIF, stabilise, PiP, split screen, xfade, compress to size…) | `references/ffmpeg-cookbook.md`; output still goes inside the video folder |

## vk cheat sheet

`vk` runs from PowerShell (`vk.ps1`), cmd (`vk.cmd`) or Git Bash. Each command has `-h`. Paths are relative to the video folder you are in.

| Command | What it does |
|---|---|
| `vk new "title" --from f1 f2 URL [--brief "…"]` | create the video folder, ingest sources (URLs via yt-dlp), probe them, write `project.md` |
| `vk ingest <video> files…` | add sources later |
| `vk probe f [--loudness]` | display size after rotation, fps, HDR, VFR, audio offset, LUFS |
| `vk sheet f [-n 12] [--from s --to s]` | contact sheet PNG with timestamps; **Read it** |
| `vk frames f --at 1.5,8,12.3` | full stills; Read them to check faces, text and framing |
| `vk transcribe f [--lang hi] [--prompt "names"]` | word timings → `work/<stem>.transcript.{json,txt,srt}`, cached; flags stretched words (hidden retakes) and unsure words |
| `vk transcribe f --from s --to e` | re-transcribe a ≤10 s window to expose a merged retake |
| `vk words t.json --find "phrase"` / `--from s --to e` | locate a phrase or list word times |
| `vk edl t.json --keep "12.3-25.1, 1:02-1:15"` | EDL from your transcript picks; edges snapped to words, then to real silence |
| `vk silence f\|edl.json [--pause 0.3 --keep 0.12]` | shorten dead air in a file or inside an EDL's ranges → `edl.json` / `*-tight.json` |
| `vk cut edl.json [--speed 1.1] [--punch 1.12]` | frame-accurate cut with audio micro-fades → `work/cut.mp4` + `cut.map.json`; checks for repeated phrases at cuts |
| `vk captions t.json [--style bold\|clean\|box\|minimal] [--fix "jeeny=Jinny"]` | word-highlight `.ass` + `.srt`, auto-remapped onto the cut timeline |
| `vk track f` | face-tracking analysis for a vertical crop (render does it on demand) |
| `vk render f --preset shorts\|reels\|tiktok\|youtube\|square\|preview\|source [--ass …] [--reframe auto\|face\|blur\|center\|none] [--music m --duck] [--logo png] [--lut cube] [--hw]` | one-encode final with two-pass loudness, then auto-verify |
| `vk verify f --preset shorts` | platform checks on any file |
| `vk status [video]` · `vk clean video [--yes]` · `vk doctor` | free disk and inventory · delete regenerable work media · environment check |

## Playbook A: talking head → Short (the common case)

1. `vk new "<title>" --from <file>` → `cd` into the folder. Ask only what the prompt leaves open: platform, target length, captions on (default yes), music (default none).
2. `vk probe source\<f>` and `vk sheet source\<f>`, then Read the sheet: framing, light, whether a face is present, vertical or wide.
3. `vk transcribe source\<f>` (medium model, about 2× realtime on this CPU; `--lang hi` for Hindi, `--prompt` for names). Read `work\<stem>.transcript.txt`.
4. Hunt retakes before planning: a stretched word (>1 s) flagged by transcribe, a repeated phrase (`vk words … --find`), restart words ("sorry", "let me start again", "matlab"), a long pause mid-thought. Re-check suspicious spots with `vk transcribe <f> --from s --to e`. By default keep the last clean take, and keep a take the speaker approved out loud.
5. **Plan → yes.** Pick the hook (strongest line first, even if it comes later in the recording), the kept ranges, pacing and speed. Write the plan into `project.md` and show it as a short table.
6. `vk edl work\<stem>.transcript.json --keep "…"` → `vk silence work\edl.json` (tightens pauses inside the kept ranges) → `vk cut work\edl-tight.json --speed 1.1 --punch 1.12`. Read the warnings: an "edge inside continuous speech" or a repeat warning means listen at that spot and fix the range.
7. `vk captions work\<stem>.transcript.json --style bold` → `vk render work\cut.mp4 --preset preview --ass work\captions.ass` → `vk sheet` the preview and Read it, then send the preview to the user.
8. After the user's notes: edit the EDL JSON or rerun steps 6–7, then `vk render work\cut.mp4 --preset shorts --ass work\captions.ass` (add `--hw` for speed). Update `project.md` (decisions, outputs) and report.

## Playbook B: long video or podcast → several Shorts

1. One folder for the long source: `vk new "<show> ep12 clips" --from <file-or-URL>`.
2. Transcribe it once (longer than 10 min uses the `small` model automatically; a one-time ~460 MB download).
3. Read the transcript and propose 3–6 candidates in a table: source range, length (20–60 s), the hook line, why it stands alone, score. Each clip must make sense with zero context.
4. After the user picks, each clip gets `work\clip-NN.edl.json` (`vk edl … -o work\clip-01.edl.json`), its own cut (`vk cut … -o work\clip-01.mp4`), captions (`--map work\clip-01.map.json -o work\clip-01.ass`) and render (`-o exports\clip-01-<hook-slug>.mp4`). Wide footage reframes with `--reframe auto` (face-tracked when faces show in ≥30% of frames, otherwise a blurred-background fit).

## Playbook C: quick utility jobs

A trim, compress, convert, audio extract or GIF still starts with `vk new` (rule 1), then a single command. Use `vk render <f> --preset source --from s --to e --no-norm` for a re-encoded trim, `--preset youtube|square` to resize, or `references/ffmpeg-cookbook.md` for everything else. Keep the result in `exports\`.

## Editing judgment for Shorts

- **Hook in the first 1–2 s:** open on the most surprising or useful line, not "hi guys". A teaser works well: put a strong later line first, then start the story (reorder ranges in the EDL).
- **Pacing:** defaults `--pause 0.3 --keep 0.12` give a tight cut. For a calm or emotional delivery use `--pause 0.5 --keep 0.25`. Keep meaningful silence such as a beat before a punchline by adding it back in the EDL.
- **Speed:** ×1.1 for slow talkers, ×1.15–1.2 for monologue insights; above ×1.25 it sounds rushed. Leave footage the creator already sped up at ×1.0.
- **Visual change every 2–4 s:** `--punch 1.1–1.15` alternates zoom on jump cuts (1080p sources; keep ≤1.06 below 720p).
- **Length:** 20–45 s is the sweet spot; one idea per Short. Hard limits: `references/platform-specs.md`.
- **Captions:** on by default because most viewers watch muted. Use `bold` (2–3 words, highlighted word) for energy and `clean` or `box` for calm or premium. Keep them centred at y≈0.70, away from the top 220 px, bottom 420 px and right 120 px UI zones of a 1080×1920 frame, and off the face (check with `vk frames`). Fix misheard names with `--fix`.
- **Ending:** a payoff line, a loop back to the hook, or one clear CTA, with nothing after the last word.
- **Audio:** −14 LUFS and −1 dBTP (render does both). Use `--denoise` only for audible hiss. Music sits at about −20 dB with `--duck`, and only with a commercial licence; otherwise render without music and let the user add a track in the app.
- **On-screen facts** (numbers, names, prices) come from the speaker or the user; list anything else under open items in `project.md`.

## EDL format (edit it by hand freely)

```json
{"sources": {"A": "source/IMG_4012.MOV", "B": "assets/broll-gym.mp4"},
 "ranges": [
   {"src": "A", "start": 41.20, "end": 44.90, "note": "teaser hook"},
   {"src": "A", "start": 3.10, "end": 12.75, "zoom": 1.12},
   {"src": "B", "start": 0.0, "end": 2.5, "note": "b-roll over the list"},
   {"src": "A", "start": 13.05, "end": 27.40, "speed": 1.15}]}
```

Times are in source seconds, paths are relative to the video folder, and `zoom`/`speed` per range are optional. The output of `vk cut` follows range order. The map file records where each range landed, which captions use.

## Report format (end of every delivery)

```
exports\<file>.mp4 · 1080×1920 · 34.2 s · −14.1 LUFS · peak −1.0 dBTP · verify PASS
cut: 27 → 9 ranges, 18.6 s of pauses removed, 1 retake dropped (02:14 "so the thing is…")
captions: bold, 41 cues · reframe: face (92% coverage) · music: none
open: confirm the "₹499" price shown at 00:21
```

## Pitfalls → fix

| Symptom | Cause → fix |
|---|---|
| A word is clipped or doubled at a cut | Whisper word times drift 0.1–0.5 s → keep edges from `vk edl`/`vk silence` (audio-snapped); for a warned edge, check `vk words` around it and move the range to the next silence |
| A phrase repeats in the output | a merged retake → `vk transcribe --from --to` on that spot, then drop one take in the EDL |
| Washed-out grey phone footage | HDR (HLG/PQ) → vk tone-maps automatically; check `vk probe` shows HDR |
| Captions show boxes instead of Hindi | the font lacks Devanagari → vk switches to Nirmala UI automatically, or pass `--font` |
| `vk` prints nothing, or a stray file appears | `>`/`&` reached cmd.exe → call `vk` from PowerShell or Git Bash, or quote the argument |
| A cut or render stops halfway, exit −1 | its output was piped into `Select-Object -First`/`head`, which kills the process → filter with `Select-String -NotMatch '^frame='` or read the full output |
| The face-track crop drifts or jitters | check with `vk track` (coverage); if it is low or there are two speakers, use `--reframe blur` or `center`, or set per-range `zoom` |
| The render is too slow | review with `--preset preview`, add `--hw`, render `--from/--to` for a spot check |
| Low disk warning | `vk clean <video> --yes` after approval, ingest with `--move`, empty the Recycle Bin |
| `npx remotion add …` fails with "--allow-scripts is not allowed" | npm 12 → `npm i --save-exact @remotion/<pkg>@<remotion version>` instead |
| Remotion captions lose the space between words | leading spaces inside `inline-block` word spans collapse → trim the token and add `marginLeft: 0.3em` |
| A Remotion render probes as `yuvj420p` (full range, even with `--pixel-format=yuv420p`) | JPEG frames → finish with `vk render <file> --preset youtube --reframe none --no-norm`, which outputs standard yuv420p and verifies |
| The mix stops short of −14 LUFS | linear loudnorm can't add gain past the peaks → make-up gain + `alimiter`, re-measure and iterate; upmix mono with `pan=stereo\|c0=c0\|c1=c0` (`-ac 2` costs 3 dB) |
| Something else breaks | `vk doctor`; setup and repair steps are in `references/setup.md` |

## Boundaries

- Publishing or uploading is the user's job; this skill prepares files and captions (`.srt`) for them.
- yt-dlp downloads only content the user owns or is licensed to edit; ask before any download.
- `vk clean` touches only regenerable media in `work\`; deleting sources or exports needs an explicit request.
- Music, stock footage and fonts are burned in only with a licence the user confirms.

## Composability: working with other skills

> **See `PROTOCOL.md` (SIP) at the skills root for the full interop contract.**

```yaml
domain: process
composable: true
yields_to: []
```

video-editor owns **process**: the folder discipline, step order, plan-before-cut and verification for video work.

**Leads** whenever video files are edited, rendered or checked, and when video work is routed to it-reelsmaker or Remotion. Its folder rule still applies in those cases (they run inside the video subfolder).

**Defers:**

| Other skill's domain | What video-editor does |
|---|---|
| **Process** (it-reelsmaker for brand reels) | hands over the reel workflow (brief, styles, scenes) and keeps rule 1: its PROJECT_ROOT is the video subfolder |
| **Craft** (remotion:*, painter) | they own motion-graphics code and visual design; video-editor supplies the timeline (cut, map, captions) and the render target |
| **Voice** (blogger, humanize) | they own the wording of captions, hooks and post copy; video-editor keeps timing and length limits |
| **Density** (caveman, compress) | chat may be compressed; plans, EDLs, `project.md` and reports keep their full structure |

Conflict signal: `⚠️ Process conflict: <what>. Kept: one subfolder per video and plan-before-cut; deferred: <what>.`

---

**Remember: `vk new` before anything else, plan before cutting, Read the sheet before reporting, numbers in every report.**
