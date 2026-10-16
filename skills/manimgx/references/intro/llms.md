# ManimGX

> The animation engine for agents: blazingly fast math and 3D videos with Manim's Python API, on a Rust GPU core.

ManimGX is a self-contained animation engine for AI agents: it makes mathematical and 3D
videos from Python scenes. Scenes use the API of Manim Community Edition, and ManimGX
annotates all of it with types, so a type checker finds errors before a render. A Rust core
draws each frame on the GPU, typesets text and LaTeX mathematics with Typst, and encodes the
video and its sound to MP4. Animations are evaluated at each frame's time, and time-based
simulations use a fixed clock independent of the output frame rate. Per-frame callbacks
should derive state from time or other objects rather than count frames. The inspect
command runs a scene without video, prints its timeline and layout problems, for example text
over other text, and writes a storyboard. In a web browser, Pyodide runs the same scenes in a Web Worker, and a WebAssembly build of the
core draws them with WebGPU.

These are instructions for an AI agent asked to make a video with ManimGX. Follow them in order.

## 1. Install

```sh
uv tool install --python 3.14 manimgx   # puts `manimgx` on PATH
manimgx --version
```

- Keep `--python 3.14`: ManimGX needs Python 3.13 or 3.14, and uv downloads one if the machine has none. Without it, uv takes the machine's default Python (macOS's is 3.9) and finds no `manimgx`.
- No `uv`? Install it: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then `source $HOME/.local/bin/env` (or call `~/.local/bin/uv`).
- Without installing: `uvx --python 3.14 manimgx <command>` runs the same CLI.
- pip works in a virtual environment with Python 3.13 or 3.14 (older Pythons find no `manimgx`): `python3.14 -m venv .venv && .venv/bin/pip install manimgx`.
- ManimGX is not the `manim` package: do not install `manim`, ffmpeg or LaTeX, and do not `import manim`.
- It draws on the GPU: Metal on macOS, Direct3D 12 on Windows, Vulkan on Linux. With no GPU (a server, a container) it draws on the CPU, with nothing more to install: the Linux wheels bring Mesa's lavapipe.

## 2. Write a scene

Save as `scene.py`:

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

- The API is Manim CE's, and every name is on the package: `m.Circle`, `m.MathTex`, `m.Create`, `m.UP`, `m.BLUE`.
- Time passes only in `self.play(...)` (1 s unless `run_time=`) and `self.wait(seconds)`; `self.add(...)` shows a mobject without animating it.
- The frame is 14.2 × 8 units centred on the origin: keep everything within x ∈ [-7, 7], y ∈ [-4, 4].

## 3. Inspect, then render

```sh
manimgx inspect scene.py     # storyboard, timeline and 2D layout checks; exit 1 for problems
manimgx render scene.py      # writes SquareToCircle.mp4 beside scene.py and prints its path
```

- `inspect` samples play and wait endings. It lists each play with its line of code, reports 2D layout problems, and writes `<Scene>.storyboard.png` with problems outlined and numbered. Look at the pictures if you can view images. Fix problems and inspect again. 3D scenes get storyboards and timelines; layout checks are skipped.
- `manimgx inspect scene.py -t 1.5,end` inspects the frames at 1.5 s and at the end instead. Repeat `-t` or separate times with commas; `-o detail.png` names the output. Pictures are chronological, six per sheet; more go to `…-2.png`, and so on. Without `end`, inspection stops after the last requested frame's play. Only sampled moments are checked.
- `render` makes 1920×1080 at 60 fps; `-r 1280x720 --fps 30` is quicker for drafts. A file with several scenes needs the scene's name: `manimgx render scene.py MyScene`.
- An error prints the scene's line that failed and, for a wrong name, a hint (`ShowCreation is Create in ManimGX`).
- `no GPU adapter` means the command ran in a sandbox that hides the GPU: run it outside the sandbox (ask the user if your tool needs approval).

## 4. Show it

Open the video for the user, and tell them its path: `open SquareToCircle.mp4` on macOS, `xdg-open SquareToCircle.mp4` on Linux.

## 5. API cheat sheet

- Shapes: `Square`, `Circle`, `Rectangle`, `Triangle`, `Polygon([x, y, 0], ...)`, `Line`, `Arrow`, `Dot`, `Brace(mob, m.DOWN)`, `NumberPlane`. Points are `[x, y, 0]`.
- Text: `Text("plain words")`, `MathTex(r"a^2 + b^2 = c^2")` (LaTeX math), `Tex(r"words and $x^2$")`. Use raw strings.
- Animations: `Create`, `Write`, `FadeIn(mob, shift=m.UP)`, `FadeOut`, `Transform`, `ReplacementTransform`, `TransformMatchingTex`, `GrowFromCenter`, `Indicate`, `Circumscribe`, `Rotate(mob, m.PI / 2)`; combine with `AnimationGroup`, `LaggedStart`, `Succession`. `mob.animate.shift(m.RIGHT).scale(2)` animates any method call.
- Placement: `.to_edge(m.UP)`, `.next_to(other, m.RIGHT, buff=0.3)`, `.move_to([x, y, 0])`, `.shift(2 * m.LEFT)`, `.scale(k)`, `m.VGroup(a, b).arrange(m.DOWN)`.
- Style: `color=m.YELLOW`, `fill_opacity=0.5`, `stroke_width=6`, `font_size=48`. A white background: `m.config.background_color = m.WHITE` after the import.
- Graphs: `axes = m.Axes(x_range=[-3, 3], y_range=[-2, 2])`, then `axes.plot(lambda x: x**2, color=m.BLUE)`.
- Sound: `self.add_sound("click.wav")` starts a sound now; `self.play(m.FadeIn(mob), m.Sound("whoosh.mp3"))` plays one with an animation.
- Narration: `self.say("The derivative of [x squared] is [two x].", m.Indicate(a), m.Write(b))` speaks and plays each animation during its bracketed words; a scene's voice is `voice = m.voices.Fal("<model>", ...)` (fal.ai's text-to-speech, keyed by the environment variable FAL_KEY), by default ElevenLabs' Eleven v3, or any function from text to `m.Speech`.
- Slides: `self.next_section("name")` between plays; `manimgx present scene.py` opens them in the browser.

## 6. Look it up

The docs follow, each page as Markdown. The User Guide tells how a scene works. The Reference
gives each class, the keywords it takes and examples. The Gallery gives the code of thirty
films. https://manimgx.academa.ai/llms-full.txt has every page in one file.
