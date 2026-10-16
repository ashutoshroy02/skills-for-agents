---
name: manimgx
description: >
  ManimGX, the GPU animation engine with Manim Community Edition's Python API (Rust core, Typst
  math, MP4 with sound), installed in the video-edit workspace with a free local Kokoro voice.
  Use to make animated Reels, Shorts, TikToks or YouTube videos from code: math and science
  explainers, equations that write and rearrange (MathTex, TransformMatchingTex), graphs and
  plots, bar charts and counting numbers, 3D surfaces, kinetic text, narrated scenes with
  self.say, slides. Trigger on "manimgx", "manim", "3blue1brown style", "animate this
  equation/proof/graph", "explainer animation", "math reel", or any request for a video made
  from Python scenes. Not for editing camera footage (video-editor / vk) or React/brand motion
  graphics (remotion:*).
domain: content
composable: true
yields_to: [process, craft]
---

# ManimGX: animated reels and videos from Python scenes

ManimGX turns a Python scene (Manim CE's API, `import manimgx as m`) into an MP4 on the GPU: no LaTeX, no ffmpeg, no `manim` package. In this workspace a scene lives inside its video folder, is narrated by the local Kokoro voice, and is finished by `vk render` for loudness and platform checks.

## Installed here

| What | Where |
|---|---|
| Engine (ManimGX 0.1.1, Python 3.14 venv) | `C:\Users\ashu2\Music\video-edit\tools\manimgx\.venv` |
| `manimgx` command (cmd, PowerShell, Git Bash) | launchers in `~/.local/bin` → the venv's `manimgx.exe` |
| `mgxkit` (import in any scene) | `tools\manimgx\mgxkit.py`: `tall()`, `SAFE`, `Kokoro` voice |
| Kokoro bridge | `tools\manimgx\kokoro_say.py`, run by `~/.video-tools/venv` with the reels engine's model and pacing |
| Reel template | `templates/reel_scene.py` in this skill |

`import mgxkit` works because `.venv\Lib\site-packages\mgxkit.pth` holds the path `C:\Users\ashu2\Music\video-edit\tools\manimgx`. Upgrade: `uv pip install --python "C:\Users\ashu2\Music\video-edit\tools\manimgx\.venv\Scripts\python.exe" -U manimgx` (ask first: it downloads). Rebuild from scratch: `uv venv tools/manimgx/.venv --python 3.14`, the same `uv pip install`, then write the `.pth` file again. Never `pip install manim`, LaTeX or ffmpeg for it.

## Rules

1. **One video folder.** Start with `vk new "<title>" --brief "<goal>"` (no `--from` needed), then work from `videos/<date>-<slug>/`: scene in `manim/scene.py`, drafts and storyboards in `work/`, finals in `exports/` (via `vk render`). Several reels from one idea may share a folder as separate scene classes. The workspace CLAUDE.md rules apply.
2. **Script and beats approved before rendering.** Show the spoken lines, what appears on each, and the length; wait for "yes". Then inspect → preview → final.
3. **Look before you report.** `manimgx inspect` exits 1 on layout problems (clipped, overlapping or tiny text): Read its storyboard PNG, fix, inspect again. After the final, Read a `vk sheet` and report duration, LUFS and the verify result.
4. **A reel never opens on an empty frame.** `self.add(hook)` before the first `say`/`play`, then animate it while it is spoken. An animation inside brackets starts only at its words, so the frames before them are black.
5. **Stay in the safe zone.** Tall frame: x ∈ [-4, 4], y ∈ [-7.1, 7.1], 1 unit = 135 px. Keep text and key visuals in `mgxkit.SAFE` (x ±3.5, y −4.0…5.2): platforms cover the bottom ~420 px and top ~250 px.
6. **Always finish with vk.** ManimGX writes variable-frame-rate MP4s with raw voice loudness (≈ −23 LUFS). `vk render work/<Scene>.mp4 --preset reels --reframe none --fps 30` gives constant 30 fps, −14 LUFS, faststart and a verify report. Without `--fps 30` vk snaps to 23.976.
7. **Free voice by default.** `voice = mgxkit.Kokoro(...)`. ManimGX's default voice (fal.ai / ElevenLabs) needs a paid `FAL_KEY`: use it only if the user asks and has set the key.
8. **Licences.** Music or SFX via `m.Sound` / `vk render --music` only when the user confirms the licence; fonts from `library/fonts` likewise.

## Workflow: narrated reel

```powershell
vk new "pythagoras reel" --brief "20 s math reel: why a²+b²=c²"
cd videos\2026-10-16-pythagoras-reel
mkdir manim; copy "$env:USERPROFILE\.claude\skills\manimgx\templates\reel_scene.py" manim\scene.py
```

1. **Script**: 3–6 short spoken lines (hook, steps, payoff, loop/CTA), one `self.say` each, with brackets around the words each animation belongs to. Get approval.
2. **Inspect**: `manimgx inspect manim/scene.py -o work/Reel.storyboard.png` → Read it. The first run voices each new line (≈ 4–20 s per line); later runs use `manim/voice/`. `-t 1.5,end` inspects exact moments.
3. **Preview**: `manimgx render manim/scene.py -r 540x960 -o work/Reel-preview.mp4`, then `vk sheet work/Reel-preview.mp4` → Read it, show the user. `manimgx preview manim/scene.py` opens a live window that replays on save.
4. **Final**: `manimgx render manim/scene.py -o work/Reel.mp4` (1080×1920 from `tall()`), then `vk render work/Reel.mp4 --preset reels --reframe none --fps 30` → `exports/<slug>-reels.mp4`. Add `--music library\music\x.mp3 --duck` for a licensed bed. Use `--preset shorts` or `tiktok` for other platforms.
5. **Captions**: `render` writes `work/Reel.srt` from the voice, ready to upload as subtitles. For burned-in word captions run the vk path instead: `vk transcribe work/Reel.mp4` → `vk captions work/Reel.transcript.json --style bold -o work/Reel.ass` → `vk render … --ass work/Reel.ass`. vk centres captions at 70 % of the height (scene y ≈ −2.8): keep that band free of scene text, or move them with `--y`.
6. **Log** script, decisions and outputs in `project.md`.

Speed on this machine (i3, Intel UHD, Direct3D 12): a 16 s 1080×1920 30 fps reel renders in about 14 s; `vk render` adds about 7 s. Wide video: skip `tall()` and finish with `--preset youtube`.

Reference build: `videos/2026-10-16-manimgx-demo/` (“0.999… = 1”, 16 s, Kokoro voice, verify PASS).

## Workspace helpers (mgxkit)

```python
import manimgx as m
import mgxkit

mgxkit.tall()  # m.config.pixel_width, pixel_height = 1080, 1920; frame_rate = 30


class Reel(m.Scene):
    voice = mgxkit.Kokoro("am_michael", 0.95)  # or af_heart, af_bella, bm_george …

    def construct(self) -> None:
        hook = m.Text("Is 0.999… = 1?", font_size=72)
        self.add(hook)
        self.say("Is zero point nine repeating [really equal to one?]", m.Indicate(hook))
```

- Voices: `~/.video-tools/venv/Scripts/python.exe tools/manimgx/kokoro_say.py --list` (am_* / af_* US male / female, bm_* / bf_* British).
- Write numbers and symbols in the spoken text as words ("zero point nine", "x squared"). The bridge also turns small numbers and 2–3 letter acronyms into speech, and puts a 0.45 s pause between sentences, as the Facebook reels engine does.
- `Kokoro` is a frozen dataclass, so `manim/voice/` re-voices a line only when its text, voice or speed changes. Drop a recording with the same file name there to replace a line.

## Quick reference (from the docs)

**The smallest scene**: time passes only in `play` (1 s unless `run_time=`) and `wait`:
```python
import manimgx as m


class SquareToCircle(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(radius=1.6, color=m.PINK, fill_opacity=0.5)
        self.play(m.Create(square))
        self.play(m.Transform(square, circle))
        self.wait()
```

**Tall video** without mgxkit (Reels, Shorts, TikTok), or `manimgx render scene.py -r 1080x1920`:
```py
m.config.pixel_width, m.config.pixel_height = 1080, 1920
```

**Place things**: `to_edge`/`to_corner` keep a 0.5 margin and work in tall frames; `next_to` gaps 0.25 unless `buff=`:
```python
import manimgx as m

class Edges(m.Scene):
    def construct(self) -> None:
        title = m.Text("A title")
        title.to_edge(m.UP)
        note = m.Text("a note", font_size=32)
        note.to_corner(m.DR)
        self.add(title, note)
```
Also `m.VGroup(a, b, c).arrange(m.DOWN, buff=0.7)`, `.move_to([x, y, 0])`, `.shift(2 * m.LEFT)`, `.scale(k)`.

**Styled text**: weight, slant, font, per-word colour, staggered entrance:
```python
        styles = m.VGroup(
            m.Text("bold", weight=m.BOLD, font_size=40),
            m.Text("italic", slant=m.ITALIC, font_size=40),
            m.Text("monospace", font="monospace", font_size=40),
            m.Text("red and blue", t2c={"red": m.RED, "blue": m.BLUE}, font_size=40),
        ).arrange(buff=0.6)
```
```python
        self.play(m.LaggedStart(*[m.FadeIn(style) for style in styles], lag_ratio=0.2))
```

**Rearrange a formula**: parts with the same LaTeX glide to their new places:
```python
import manimgx as m

class Rearrange(m.Scene):
    def construct(self) -> None:
        before = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=96)
        after = m.MathTex("a^2", "=", "c^2", "-", "b^2", font_size=96)
        before[2].set_color(m.YELLOW)
        after[4].set_color(m.YELLOW)
        self.play(m.Write(before))
        self.play(m.TransformMatchingTex(before, after))
        self.wait()
```

**Narrate**: each animation plays during its bracketed words; the scene waits for the line:
```python
import manimgx as m

class Derivative(m.Scene):
    def construct(self) -> None:
        square = m.MathTex("x^2", font_size=96).shift(2 * m.LEFT)
        derivative = m.MathTex("2x", font_size=96).shift(2 * m.RIGHT)
        self.add(square)
        self.say(
            "The derivative of [x squared] is [two x].",
            m.Indicate(square),
            m.Write(derivative),
        )
```

**Count up a number**: stats and "how much" reels:
```python
import manimgx as m

class Counter(m.Scene):
    def construct(self) -> None:
        x = m.ValueTracker(0)
        number = m.DecimalNumber(0, font_size=96)

        def show_x(mobject: m.DecimalNumber) -> None:
            mobject.set_value(x.get_value())

        number.add_updater(show_x)
        self.add(number)
        self.play(x.animate.set_value(10), run_time=3)
```

**Bar chart that changes**: data reels:
```python
import manimgx as m

class ChartsHero(m.Scene):
    def construct(self) -> None:
        chart = m.BarChart(
            [3, 5, 2, 6, 4], bar_names=["A", "B", "C", "D", "E"], y_range=[0, 8, 2]
        )
        self.play(m.Create(chart))
        self.play(chart.animate.change_bar_values([5, 2, 6, 3, 7]), run_time=2)
        self.wait()
```

**A dot rides a graph**: `always_redraw` rebuilds a mobject every frame:
```python
import manimgx as m

def curve(x: float) -> float:
    return x**2 / 4

class Ride(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 5, 1], y_range=[0, 7, 1], x_length=8, y_length=5)
        graph = axes.plot(curve, color=m.BLUE)
        x = m.ValueTracker(1)

        def make_dot() -> m.Dot:
            point = axes.c2p(x.get_value(), curve(x.get_value()))
            return m.Dot(point, color=m.YELLOW)

        dot = m.always_redraw(make_dot)
        self.add(axes, graph, dot)
        self.play(x.animate.set_value(4.5), run_time=3)
```
In a tall frame give `Axes` `x_length` ≤ 7.

**Zoom and pan**: `self.camera.frame` is a mobject:
```python
        frame = self.camera.frame
        self.play(frame.animate.scale(0.25).move_to(3 * m.UP), run_time=2)
```

**Sound**: a sound with an animation, or a music bed that loops (licensed files only):
```py
self.play(m.FadeIn(dot), m.Sound("click.wav"))
```
```py
music = self.add_sound(m.Sound("theme.mp3").gain(-18).fade_in(2).loop())
```

## Key concepts

- **Scene**: one video; the class name names the MP4. `construct` runs top to bottom. `m.ThreeDScene` for 3D.
- **Mobject**: anything drawn (shapes, `Text`, `MathTex`, `Axes`, `ImageMobject("file.png")`, `SVGMobject`). Making one does not show it: `self.add` shows it at once, `self.play(...)` animates it in.
- **`.animate`**: animates any method call (`mob.animate.shift(m.RIGHT).scale(2)`); several `.animate`s of one mobject at the same time add up.
- **Frame units**: the short side is 8 units in every aspect ratio. Points are `[x, y, 0]`; `m.UP`, `m.DR`, `m.ORIGIN`… are points.
- **`m.config`**: `pixel_width`, `pixel_height`, `frame_rate`, `background_color`, set after the import; `-r`/`--fps` override.
- **Text and math**: set by Typst with bundled fonts (New Computer Modern default; `"sans-serif"` = Noto Sans; CJK, Indic and emoji included). `MathTex` converts LaTeX math; LaTeX packages and `\def` do not convert. `m.Typst` / `m.MathTypst` take Typst directly. `font_paths=[...]` adds font folders.
- **Updaters / ValueTracker**: per-frame rules; derive state from time or trackers, never from frame counts.
- **Sections**: `self.next_section("name")` → `manimgx present` slides (`--pdf` handout).

## Errors and fixes

| Symptom | Fix |
|---|---|
| `ShowCreation`, `ApplyMethod`, `MovingCameraScene` … not found or deprecated | ManimGX keeps one name: `Create`, `.animate`, `Scene` (the error prints a hint) |
| `import manim` / LaTeX package errors | use `import manimgx as m`; rewrite the formula without packages or use `m.MathTypst` |
| `no GPU adapter` | the command ran in a sandbox that hides the GPU → run it outside the sandbox |
| `Kokoro failed for …` | `vk doctor`; check `~/.video-tools/venv` has kokoro-onnx and `facebook-pages/_engine/models/` has the model files |
| `inspect` exit 1 | Read the storyboard: red numbered boxes name the clipped/overlapping mobjects by variable name |
| vk verify `fps 14` / `23.976` | the raw ManimGX file is VFR → finish with `vk render … --fps 30` |
| loudness warn ≈ −15 LUFS after vk | speech-only mix with linear loudnorm; PASS is fine, or add `--lufs -13` |
| text cut off in a tall frame | reflow to fit x ±3.5: smaller `font_size`, `\n` line breaks, `arrange(m.DOWN)` |

## Reference files

`references/index.md` lists every page and the classes each API page documents. Search by name: `grep -rn "^### TransformMatchingTex" references/api/`.

| Folder | Holds | Open when |
|---|---|---|
| `intro/llms.md` | the agent instructions and API cheat sheet from llms.txt | refreshing the basics |
| `guide/` (13 pages) | the basics, positions, animations, text and math, graphs, updaters, camera and 3D, sound and voice, rendering, coming from Manim CE | a new kind of task: read the guide page first |
| `api/` (55 pages) | every class: signature, each keyword with its default, a runnable example | exact keywords, an unfamiliar class, an error about a name |
| `gallery/` (48 films) | full code of finished films: Fourier π, Galton board, Lorenz, Pythagoras, quadratic formula, Riemann sums, Taylor series, 3D surfaces … | a whole-film pattern to adapt; `gallery/index.md` lists them |

Start with the template and the Quick reference. For a specific animation look in `api/appear-and-disappear.md`, `emphasis.md`, `transforms.md`, `move-and-deform.md`, `together-and-in-turn.md` and `rate-functions.md`. For advanced work (3D, lights, vector fields, simulations) read `guide/camera-and-3d.md`, then the matching gallery film.

## Composability: working with other skills

> See `PROTOCOL.md` (SIP) at the skills root for the full interop contract.

```yaml
domain: content
composable: true
yields_to: [process, craft]
```

manimgx owns the **content** of a scene: what is drawn, how it moves, what the voice says, and the ManimGX API.

**Leads** when a video is made from Python scenes: math or science explainers, animated equations, graphs, charts, counters, 3D, kinetic text.

| Other skill's domain | What manimgx does |
|---|---|
| **Process** (video-editor) | defers on the folder rule, plan approval, `vk render`/verify, captions, music and cleanup; manimgx supplies `work/<Scene>.mp4` |
| **Process** (Facebook reels engine, `facebook-pages/fb`) | can render an animated scene as a clip asset for a reel; the reel's own pipeline still voices, captions and renders it |
| **Craft** (remotion:*, painter, it-reelsmaker) | they own React/brand motion graphics and visual design; manimgx is for code-drawn math and diagrams. One video can use both, with each render as a clip finished by `vk` |

Conflict signal: `⚠️ Process conflict: <skill> wants <X>; manimgx keeps <scene content>. <What was preserved>.`
