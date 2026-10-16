# Command line

The animation engine for agents: blazingly fast math and 3D videos with Manim's Python API, on a Rust GPU core.

A scene file is Manim CE code: `import manimgx as m`, a class deriving m.Scene, its `construct`. Work in a loop:

 manimgx inspect scene.py timeline, storyboard, layout problems manimgx inspect scene.py -t 1.5,end inspect specific moments manimgx render scene.py the video (MP4), with the same report

Files are written beside the scene file; each command prints what it wrote.

**Usage**:

```console
$ manimgx [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--version`: Show the version and exit.
- `--help`: Show this message and exit.

**Commands**:

- `render`: Render a scene to an MP4 video, with its...
- `inspect`: Inspect a scene: annotated PNGs, timeline...
- `preview`: Preview a scene live: in a window, made...
- `present`: Present a scene: its sections are the slides.

## `manimgx render`

Render a scene to an MP4 video, with its sound.

Also writes a storyboard beside the video (the frame at each play's end, layout problems outlined and numbered) and lists those problems — see `manimgx inspect` — and, if the scene speaks or has subcaptions, its subtitles (.srt).

**Usage**:

```console
$ manimgx render [OPTIONS] {FILE} [SCENE]
```

**Arguments**:

- `FILE`: The scene file: a Python file defining ManimGX scenes. \[required\]
- `SCENE`: The scene (a class in the file); needed only if the file defines several.

**Options**:

- `-o, --output <path>`: The video (.mp4). \[default: .mp4 beside the file\]
- `-r, --resolution WxH`: Pixels, e.g. 1280x720. \[default: the scene's config, 1920x1080 unless set\]
- `--fps <int range>`: Frames per second. \[default: the scene's config, 60 unless set\] \[x\>=1\]
- `--preset <ultrafast|superfast|veryfast|faster|fast|medium|slow|slower|veryslow|placebo>`: Encoding speed: faster presets encode sooner but produce larger files. \[default: medium\]
- `--crf <float range>`: Video quality: lower values give higher quality and larger files. \[default: 23.0; 0\<=x\<=51\]
- `--help`: Show this message and exit.

## `manimgx inspect`

Inspect a scene: annotated PNGs, timeline and 2D layout checks, without video.

Samples play and wait endings by default. With -t, inspects the frames a video player shows at those times; 'end' is the last frame. Checks for clipped content, overlapping text, lines or fills over text, and small labels. 3D scenes get pictures and a timeline; layout checks are skipped. Only sampled moments are checked.

Pictures are chronological, captioned \#play t=… file:line, with problems outlined and numbered. Six fit on each sheet (more go on `<name>-2.png`, …). Default sampling omits consecutive identical pictures. With -t, only the requested frames are drawn, and the scene stops after the last requested frame's play unless 'end' is included.

Exits 1 for layout problems; notes, such as a graph leaving the frame, do not count.

**Usage**:

```console
$ manimgx inspect [OPTIONS] {FILE} [SCENE]
```

**Arguments**:

- `FILE`: The scene file: a Python file defining ManimGX scenes. \[required\]
- `SCENE`: The scene (a class in the file); needed only if the file defines several.

**Options**:

- `-t, --time TIME`: Seconds from the start, or 'end'; several: repeat -t or separate with commas.
- `-o, --output <path>`: The storyboard (.png). \[default: .storyboard.png beside the file\]
- `--help`: Show this message and exit.

## `manimgx preview`

Preview a scene live: in a window, made again each time its code is saved.

The window plays the scene as it is made. Saving the file, or a module it imports from beside it, runs the scene again, and the window keeps its place; an error shows over the last good picture. A file of several scenes plays the one named, or its first; N and P go to the others. Keys: Space play/pause, ← → 5 s, , . a frame, Option (or Ctrl) with ← → a play, ? all of them. Closing the window, or Ctrl+C, stops.

**Usage**:

```console
$ manimgx preview [OPTIONS] {FILE} [SCENE]
```

**Arguments**:

- `FILE`: The scene file: a Python file defining ManimGX scenes. \[required\]
- `SCENE`: The scene (a class in the file); needed only if the file defines several.

**Options**:

- `-t, --time <float range>`: Where the playhead starts, in seconds. \[default: 0.0; x\>=0\]
- `-r, --resolution WxH`: Pixels, e.g. 1280x720. \[default: the scene's config, 1920x1080 unless set\]
- `--fps <int range>`: Frames per second. \[default: the scene's config, 60 unless set\] \[x\>=1\]
- `--help`: Show this message and exit.

## `manimgx present`

Present a scene: its sections are the slides.

Renders the video, writes a page that plays it (it stops at the end of each section, until you go on), and opens it. Keys: → or Space next, ← back, F full screen, B black, Shift+P presenter view (notes, the next slide, a timer), C captions, ? help. A clicker works: it sends the same keys. Begin a section with `self.next_section(...)` in the scene.

**Usage**:

```console
$ manimgx present [OPTIONS] {FILE} [SCENE]
```

**Arguments**:

- `FILE`: The scene file: a Python file defining ManimGX scenes. \[required\]
- `SCENE`: The scene (a class in the file); needed only if the file defines several.

**Options**:

- `-o, --output <path>`: The video (.mp4); the page is written beside it (.html). \[default: .mp4 beside the file\]
- `-r, --resolution WxH`: Pixels, e.g. 1280x720. \[default: the scene's config, 1920x1080 unless set\]
- `--fps <int range>`: Frames per second. \[default: the scene's config, 60 unless set\] \[x\>=1\]
- `--pdf / --no-pdf`: Also write a PDF: the picture each slide ends on, a page each. \[default: no-pdf\]
- `--open / --no-open`: Open the page in the browser. \[default: open\]
- `--help`: Show this message and exit.
