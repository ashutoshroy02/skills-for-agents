# Store Listing Assets — What We Made

| Asset | Size | How we made it |
|-------|------|----------------|
| App icon | 512×512 PNG, ≤1 MB | Rendered from the app's own icon source (the same script that makes the launcher icons) |
| Feature graphic | 1024×500 PNG/JPG, no alpha | Game art + title, text kept centered (edges may crop) |
| Phone screenshots | 6 × 900×1600 (9:16) | Captured from the release build on the emulator: title, gameplay, booster, win screen, map, profile |

- Capture: `adb exec-out screencap -p > shot.png`, then crop/resize with Pillow to 900×1600.
- Order matters: the first 2–3 screenshots show in search, so put the title screen or best gameplay first.
- Check sizes before uploading: `python -c "from PIL import Image;print(Image.open('f.png').size)"`.
- Keep a copy of everything in one folder (e.g. `Downloads/<app>-play-store/`) with the answers file.
- AI-generated content declaration on the listing: answer truthfully; let the user review it.
