# vk environment: what is installed where, and how to repair it

Installed on 2026-10-11 for Windows 11 (i3-1115G4, 8 GB RAM, Intel UHD, no CUDA).

| Piece | Location | Notes |
|---|---|---|
| Toolkit code | `~/.claude/skills/video-editor/scripts/` (`vk.py` + `vk_*.py`) | stdlib + numpy/Pillow/OpenCV/faster-whisper, imported lazily |
| Python env | `~/.video-tools/venv` (CPython 3.12.7 via uv) | 3.14 lacks wheels for some deps, so it stays on 3.12 |
| Packages | faster-whisper 1.2.x, opencv-python-headless **<5** (4.x keeps the Haar fallback), numpy, Pillow | PyAV ≥19 broke faster-whisper's file decoding; vk passes a numpy array instead |
| Launchers | `~/.local/bin/vk.ps1` (PowerShell), `vk.cmd` (cmd), `vk` (Git Bash) | `~/.local/bin` is on PATH |
| Config | `~/.video-tools/config.json` → `{"workspace": "C:\\Users\\ashu2\\Music\\video-edit"}` | env `VK_WORKSPACE` overrides; the `.vk-workspace` marker is found by walking up from the cwd |
| Face model | `~/.video-tools/models/face_detection_yunet_2023mar.onnx` (opencv_zoo) | missing → Haar cascade fallback |
| Whisper models | `~/.cache/huggingface/hub/models--Systran--faster-whisper-*` | medium (~1.5 GB) cached; small downloads on first long video; env `VK_WHISPER_MODEL` forces one |
| ffmpeg | winget `Gyan.FFmpeg` 8.1 full build | needs libass, libzimg, libvpl (QSV); `vk doctor` checks |
| yt-dlp | `uv tool install yt-dlp` | update with `uv tool upgrade yt-dlp` when sites break |
| Node | system Node.js | for Remotion (`npx create-video` via the remotion skills) |

## Repair commands

```
vk doctor
uv venv "$HOME/.video-tools/venv" --python 3.12                                      # recreate the env
uv pip install --python "$HOME/.video-tools/venv/Scripts/python.exe" faster-whisper "opencv-python-headless<5" numpy Pillow
uv tool upgrade yt-dlp
winget upgrade Gyan.FFmpeg
```

Re-download the face model:
```
curl -sSL -o "$HOME/.video-tools/models/face_detection_yunet_2023mar.onnx" https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
```

## Measured speeds on this machine (for estimates)

| Job | Speed |
|---|---|
| `vk transcribe` medium int8 | ~2.2× realtime (27 s of audio → 59 s) |
| `vk cut` (per-segment libx264 veryfast, 1080p) | ~1× realtime (9 segments, 14.7 s output → 16 s) |
| `vk render --preset shorts` (x264 medium, two-pass loudness) | ~2.4 s per output second (9.7 s → 23 s; a 45 s Short ≈ 2 min) |
| `vk render --hw` (Quick Sync) | ~1.4 s per output second (9.7 s → 14 s), similar file size |
| `vk render --preset preview` | fastest option (540×960, x264 veryfast); use it for every review round |

## Extending vk

Add a module `scripts/vk_<area>.py` with `register(sub)` and wire it into `vk.py`. Put shared helpers in `vk_common.py`: `probe`, `run`, `fpath` (filter-safe paths, run ffmpeg with `cwd=` the video folder), `audio16k`, `measure_loudness`, `std_fps`, `tonemap_chain`. Keep outputs inside the video folder (`work_dir()`, `require_video_dir()`).
