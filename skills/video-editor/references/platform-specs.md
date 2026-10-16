# Platform specs (as of late 2026; limits change, so confirm in the app when it matters)

| Preset | Platform | Frame | Max length | Notes |
|---|---|---|---|---|
| `shorts` | YouTube Shorts | 1080×1920 9:16 (square also counts) | 3 min | sweet spot 20–45 s; loops count as rewatches |
| `reels` | Instagram / Facebook Reels | 1080×1920 9:16 | 3 min in-app | the feed preview crops to 4:5 around the centre, so keep key text in the middle band |
| `tiktok` | TikTok | 1080×1920 9:16 | 10 min in-app (longer by upload) | the right-hand rail and caption block cover more than other apps |
| `youtube` | YouTube long-form | 1920×1080 16:9 | — | thumbnail 1280×720 |
| `square` | LinkedIn / X feed | 1080×1080 | — | captions matter even more (autoplay muted) |
| `preview` | review only | 540×960, crf 28 | — | fast to render and send; never publish it |

All presets give H.264 High, yuv420p, bt709, constant fps (source rate snapped, ≤60), AAC 48 kHz, −14 LUFS integrated, −1 dBTP, and `+faststart`.

## Safe zones on 1080×1920

| Zone | Covered by |
|---|---|
| y 0–220 | status bar, top tabs, "Reels"/"Shorts" label |
| y 1500–1920 | caption text, username, music ticker, buttons |
| x 960–1080 (right 120 px), lower half | like, comment and share rail |
| centre band y≈250–1450 | safe for hooks, captions (vk default centre y=1344) and graphics; keep text off the face |

## Loudness

YouTube, Instagram, TikTok and Spotify all play roughly at −14 LUFS. Louder masters get turned down and quieter ones sound weak next to other videos. `vk render` does two-pass loudnorm, then measures and reports the result. Speech-only content can sit at −14 to −16; keep the true peak at or below −1 dBTP because lossy re-encoding by the platform adds overshoot.

## Upload tips

- Upload the `exports/` file as is; platforms re-encode anyway, so a higher-quality source (crf 18) survives better.
- Upload the `.srt` from `vk captions` as a caption track on YouTube (searchable, translatable) in addition to burned-in captions.
- Leave 0.5–1 s after the last word, or loop cleanly to the first frame.
