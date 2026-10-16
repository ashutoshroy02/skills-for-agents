# User Guide

**Blazingly fast 3D animation engine for agents, compatible with [Manim CE's API](<https://www.manim.community>).**  
Powered by Rust and wgpu. Install with a prompt or pip. Run in the browser.

**[Documentation](</>)** · [Quickstart](</user-guide/quickstart/>) · [Examples](</gallery/>) · [API Reference](</reference/>)

**36.2 seconds of video, rendered in 3.08 seconds.** Across five scenes at 1080p60 on an Apple M4 Pro, ManimGX is **90.6× faster than ManimCE**, **11.5× faster than ManimGL**, and **18.7× faster than Blender Workbench**, from launch to finished MP4. [How it was measured](<https://github.com/academa-labs/manimgx/tree/main/benchmarks>): the scenes, the settings and every run.

<sub>All engines use the fastest encoding preset available. Lower is better.</sub>

**Compare the same scene.** Linked rings at 2.5 seconds, rendered by each engine.

| ManimGX | ManimCE | ManimGL | Blender Workbench | Blender EEVEE |
| :---: | :---: | :---: | :---: | :---: |
|  |  |  |  |  |

## Get started

**With a prompt.** Paste into Claude Code, Codex, or Cursor. Your agent handles setup:

```text
Follow https://manimgx.academa.ai/llms.txt.
Install ManimGX, make a 3D animation of the solar system, and open it.
```

**With pip.** Install on macOS, Linux or Windows with Python 3.13+:

```sh
pip install manimgx
```

Fonts, typesetting and video encoding are included. For editor setup and a guided first animation, follow the [Quickstart](</user-guide/quickstart/>).

## From Python to MP4

Save this as `scene.py`:

```python
import manimgx as m

class Hello3D(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=65 * m.DEGREES, theta=-45 * m.DEGREES)
        self.begin_ambient_camera_rotation(rate=0.5)
        cube = m.Cube(side_length=3, fill_opacity=0.3, stroke_width=2)
        self.play(m.Create(cube), run_time=2)
        self.wait(4)
```

Render it:

```sh
manimgx render scene.py
```

You get `Hello3D.mp4`, a 1080p60 video:

## Why ManimGX?

**An API for 3D video in the age of agents.** Your agent writes Python using [Manim CE's API](<https://www.manim.community>). ManimGX's Rust + wgpu engine renders the MP4, blazingly fast.

- **Fully statically typed.** Keyword arguments and `.animate` chains included.
- **2D and 3D together.** Surfaces, meshes and moving cameras alongside text, equations and plots.
- **Runs in the browser.** `npm install manimgx`. [Pyodide](<https://pyodide.org>) runs Python in a Web Worker; WebGPU renders the scene. [Embed a scene](</user-guide/rendering/#embed-in-a-web-page>) with no render server.
- **Agent feedback.** [`manimgx inspect`](</user-guide/rendering/#inspect>): storyboards and 2D layout checks, at play endings or times you choose.
- **Text and math.** Write LaTeX or Typst. No LaTeX installation needed.
- **Speech in sync.** [Match animations to spoken words](</user-guide/sound-and-voice/>) with `self.say()`.

## Documentation

**[manimgx.academa.ai](</>)** has the guides, rendered examples with source code, and API reference:

- [Quickstart](</user-guide/quickstart/>): install, set up your editor, and render your first scene.
- [User Guide](</user-guide/the-basics/>): learn scenes, animations, 3D, text and sound, one idea at a time.
- [Examples](</gallery/>): watch complete films and read the Python that makes them.
- [API Reference](</reference/>): look up classes, methods and their typed parameters.
- [Coming from Manim CE](</user-guide/coming-from-manim-ce/>): adapt existing scenes and check where behavior differs.

For agents, [llms.txt](</llms.txt>) provides setup instructions and links to the documentation as Markdown.

## On the shoulders of giants

[Grant Sanderson](<https://www.3blue1brown.com>) created [Manim](<https://github.com/3b1b/manim>). ManimGX targets the API of [Manim Community Edition](<https://www.manim.community>), the widely used community-maintained fork.

The Rust renderer uses [wgpu](<https://wgpu.rs>) for native GPU rendering and WebGPU in the browser. Its 3D lighting is adapted from Google's [Filament](<https://github.com/google/filament>): physically based materials, image-based lighting, ambient occlusion, bloom and AgX tone mapping. [Typst](<https://typst.app>) typesets text and math, with [mitex](<https://github.com/mitex-rs/mitex>) translating LaTeX input to Typst. [x264](<https://www.videolan.org/developers/x264.html>) encodes native video exports as H.264; [FFmpeg](<https://ffmpeg.org>) decodes imported audio, using [libopus](<https://opus-codec.org>) for Opus.

[Pyodide](<https://pyodide.org>) runs Python scenes in a browser worker. Linux wheels bundle [Mesa](<https://mesa3d.org>)'s lavapipe for Vulkan rendering on the CPU when no suitable GPU is available.

## Community

ManimGX is an open-source project by [Academa](<https://academa.ai>), created by [Abdullah Geduk](<https://geduk.io>) and [Sina Atalay](<https://sinaatalay.com>). We welcome contributions from the community.

Questions, bug reports and feature requests start with an [issue](<https://github.com/academa-labs/manimgx/issues/new/choose>). To contribute, read [Contributing](<https://github.com/academa-labs/manimgx/blob/main/.github/CONTRIBUTING.md>) and the [Developer Guide](</developer-guide/>).

[Changelog](</changelog/>) · [Citing ManimGX](<https://github.com/academa-labs/manimgx/blob/main/CITATION.cff>)

Everyone participating follows the [Code of Conduct](<https://github.com/academa-labs/manimgx/blob/main/.github/CODE_OF_CONDUCT.md>). Report vulnerabilities privately through the [security policy](<https://github.com/academa-labs/manimgx/blob/main/.github/SECURITY.md>).

## License

ManimGX's own code is [MIT-licensed](<https://github.com/academa-labs/manimgx/blob/main/LICENSE>). Native wheels include x264 and are GPL-3.0-or-later as a whole.

Bundled components retain their licenses: see the [third-party notices](<https://github.com/academa-labs/manimgx/blob/main/LICENSE-THIRD-PARTY>), [Linux renderer notices](<https://github.com/academa-labs/manimgx/blob/main/LICENSE-LAVAPIPE>), and the [Noto](<https://github.com/academa-labs/manimgx/blob/main/fonts/manimgx-fonts/LICENSE>) and [Noto CJK](<https://github.com/academa-labs/manimgx/blob/main/fonts/manimgx-fonts-cjk/LICENSE>) font licenses.

This software uses code of [FFmpeg](<https://ffmpeg.org>) licensed under [LGPL-2.1-or-later](<https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>). Complete source, including FFmpeg, is in `manimgx-X.Y.Z-source.tar.xz` on each [GitHub release](<https://github.com/academa-labs/manimgx/releases>).
