# ffmpeg cookbook: jobs `vk` does not wrap

Run these from inside the video folder (`videos/<slug>/`), reading from `source/` or `work/` and writing to `work/` or `exports/`. Add `-hide_banner -y` to taste. For speed on this machine, swap `-c:v libx264 -crf 18 -preset medium` for `-c:v h264_qsv -global_quality 21`.

Prefer `vk` when it covers the job: `vk cut` (any multi-clip assembly, B-roll inserts, intros/outros via a multi-source EDL), `vk render` (resize, reframe, captions, music, loudness, LUT, logo), `vk verify`.

## Trim without re-encoding (instant, cuts on keyframes)
```
ffmpeg -ss 00:01:05 -to 00:02:10 -i source/in.mp4 -c copy -avoid_negative_ts make_zero work/trim.mp4
```
Use this to carve a manageable chunk out of a huge recording before `vk transcribe`. The edges may be off by up to a GOP (group of pictures, the run of frames between keyframes); for frame-accurate trims use `vk render --from --to` or `vk cut`.

## Compress to a target size (two-pass)
Use video bitrate (kbps) = target_MB × 8192 / seconds − audio kbps. For example, 25 MB for 60 s with 128k audio gives 25×8192/60 − 128 ≈ 3285k.
```
ffmpeg -i in.mp4 -c:v libx264 -b:v 3285k -preset medium -pass 1 -an -f null NUL
ffmpeg -i in.mp4 -c:v libx264 -b:v 3285k -preset medium -pass 2 -c:a aac -b:a 128k -movflags +faststart exports/small.mp4
```
(`NUL` in PowerShell/cmd, `/dev/null` in Git Bash.) Delete the `ffmpeg2pass-0.log*` files afterwards.

## Extract audio
```
ffmpeg -i in.mp4 -vn -c:a libmp3lame -q:a 2 exports/audio.mp3      # mp3 ~190 kbps
ffmpeg -i in.mp4 -vn -c:a pcm_s16le -ar 48000 exports/audio.wav     # lossless
```

## GIF (good palette, small)
```
ffmpeg -ss 3 -t 4 -i in.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" exports/clip.gif
```

## Thumbnail / cover frame
Pick the frame with `vk sheet` then `vk frames --at <t> --width 1280`. Make a YouTube thumbnail at 1280×720 (keep text big, 3–5 words). For Shorts the cover is chosen in the app.

## Speed ramp (slow-mo section)
Split the section into its own EDL range with `"speed": 0.5` (vk keeps pitch with atempo). Smooth slow-mo needs high-fps footage. Otherwise interpolate (slow on this CPU):
```
ffmpeg -i in.mp4 -vf "minterpolate=fps=60:mi_mode=mci" work/smooth.mp4
```

## Freeze frame at t=5 s for 1.5 s
Extract a still (`vk frames --at 5`), make a 1.5 s clip `ffmpeg -loop 1 -t 1.5 -i still.png -f lavfi -t 1.5 -i anullsrc=r=48000:cl=stereo -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -shortest work/freeze.mp4`, then splice it in as an EDL source.

## Reverse a short clip (≤10 s; it buffers everything in RAM)
```
ffmpeg -i clip.mp4 -vf reverse -af areverse work/rev.mp4
```

## Stabilise shaky handheld (two passes, vidstab)
```
ffmpeg -i in.mp4 -vf vidstabdetect=shakiness=6:result=work/transforms.trf -f null NUL
ffmpeg -i in.mp4 -vf "vidstabtransform=input=work/transforms.trf:smoothing=20:zoom=4,unsharp=5:5:0.6" -c:a copy work/stable.mp4
```
The filter path is relative to the cwd (the video folder). Avoid drive letters inside filter options.

## Denoise video (grainy low light)
`-vf hqdn3d=3:3:6:6` (light) to `hqdn3d=6:5:9:8` (strong). Apply it before scaling.

## Colour fixes
- Brightness, contrast and saturation: `eq=brightness=0.03:contrast=1.07:saturation=1.08`
- A gentle S-curve: `curves=master='0/0 0.25/0.22 0.5/0.5 0.8/0.83 1/1'`
- White balance (warm→neutral): `colorbalance=rs=-0.05:bs=0.05` (shadows); `colortemperature=temperature=5600`
- A LUT: `vk render … --lut library/luts/x.cube --lut-mix 0.7`

## Picture-in-picture (face cam over screen recording)
```
ffmpeg -i screen.mp4 -i face.mp4 -filter_complex "[1:v]scale=360:-2,format=yuva420p[pip];[0:v][pip]overlay=W-w-40:H-h-40:shortest=1" -map 0:a -c:a copy work/pip.mp4
```

## Split screen (stack two clips vertically for 9:16)
```
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex "[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[a];[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[b];[a][b]vstack[v]" -map "[v]" -map 0:a -shortest work/split.mp4
```

## Crossfade between two clips (xfade)
```
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.4:offset=<lenA-0.4>[v];[0:a][1:a]acrossfade=d=0.4[a]" -map "[v]" -map "[a]" work/xf.mp4
```
Both inputs need the same size, fps and timebase (run them through `vk cut` first). For Shorts, hard cuts usually beat fades.

## Text overlay (title card, label)
Prefer ASS for styled text (put a `Dialogue` line in a small `.ass` and pass `--ass`). Quick drawtext:
```
-vf "drawtext=fontfile=C\\:/Windows/Fonts/arialbd.ttf:text='3 TIPS':fontsize=96:fontcolor=white:borderw=6:x=(w-tw)/2:y=h*0.18:enable='between(t,0,2.5)'"
```

## Burn an existing .srt
`vk render f --ass work/x.ass` is the styled route. For a plain `.srt`: `-vf "subtitles=work/x.srt:force_style='Fontname=Arial Black,Fontsize=18,Outline=2'"`.

## Replace or mix audio
- Replace: `ffmpeg -i video.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest work/out.mp4`
- Music bed with ducking: `vk render f --music library/music/x.mp3 --music-db -20 --duck`

## Fade in from and out to black
`-vf "fade=t=in:st=0:d=0.4,fade=t=out:st=<len-0.5>:d=0.5" -af "afade=t=in:d=0.3,afade=t=out:st=<len-0.5>:d=0.5"`

## Rotate / flip (when the metadata is wrong)
`-vf transpose=1` (90° clockwise), `transpose=2` (90° counter-clockwise), `hflip`, `vflip`. To fix only the rotation flag without re-encoding: `ffmpeg -display_rotation:v:0 0 -i in.mov -c copy work/fixed.mov`.

## Concatenate many same-format clips fast (no re-encode)
Write `list.txt` with `file 'a.mp4'` lines, then run `ffmpeg -f concat -safe 0 -i list.txt -c copy work/joined.mp4`. This needs identical codecs, size and fps; otherwise use `vk cut` with a multi-source EDL.
