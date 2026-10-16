# From Python

**The film's code**

```python
import manimgx as m

class FromPythonHero(m.Scene):
    def construct(self) -> None:
        code = m.Code(
            code_string='film = MyScene().render()\nfilm.export("video.mp4")\nprint(film.subtitles())',
            language="python",
            background="window",
        ).scale(1.1)
        self.play(m.FadeIn(code))
        self.wait()
```

A scene renders from Python as from the command line: `MyScene().render()` runs it and records its film. The film keeps the frames, the plays, the sounds, the sections and the captions, to write as a video or to read in a program. A window plays a film on the screen as it is recorded.

## render

Run the scene and record its film: `setup`, `construct` and `tear_down`, then a closing frame.

Each frame is sent as it is made: encoded into `video`, an MP4 file, and handed to `frames`, if given; each play or wait, as it ends, is handed to `plays`, if given. A frame is drawn only for the video, or when `frames` asks for its pixels: with neither, the frames are counted, not drawn, which checks a scene quickly. Frames `k = 0, 1, …` sample `k / fps` seconds, after events at the same float instant; the closing frame then shows it at its own instant: the scene's end if a frame falls there, or else the first frame time after it. So the scene's last animation is seen landing.

Either function, and a take, may raise `Cut` to end the film there: the scene stops, and the video is written up to the last frame sent. If the scene fails, the video is not written. A scene renders once: make a new one to render it again.

```python
self.render(video=None, *, preset=DEFAULT_ENCODER_PRESET, crf=DEFAULT_ENCODER_CRF, frames=None, plays=None, take=None)
```

**`video`**

The MP4 file to write, if any, at the size and frame rate of `config` (a whole number of frames a second, and an even width and height).

**`preset`**

The x264 encoding preset; faster presets make larger files.

**`crf`**

The x264 constant rate factor, from 0 to 51; lower values give higher quality.

**`frames`**

A function handed each frame as it is sent (a `FrameSink`): a `Frame`, which knows its place in the film and draws its pixels when asked.

**`plays`**

A function called as each play or wait ends (a `PlayHook`), with the `Play` and the animations it played, the world as the play left it.

**`take`**

Record the film as a take instead, for ManimGX's player to draw: a function handed its bytes as they are recorded (a `Take`). A take has no video, and no frames for `frames`.

Returns how many frames it has, its plays, sections, sounds and captions, and how its video was made.

## Film

A scene's film: its frames, as they are sent, its plays, and its sounds, sections and captions.

`Scene.render` makes one and returns it. Each frame is sent once: encoded into the video, if there is one, and handed to `frames`, if given; a frame equal to the one before is not sent again, but lengthens it. Each play, as it ends, is kept, and handed to `plays`, if given. The sounds the scene placed are mixed into the video's sound track as it is written.

A film can instead be recorded as a take: the engine's work written down — each shape once, then each frame's view and records, and at the end its sound and captions — for ManimGX's player to play, at any moment: in a `Window`, live as the scene runs (`manimgx preview`), or in the browser, where Python has no GPU (Pyodide).

```python
m.Film(video=None, *, frames=None, plays=None, take=None, preset=DEFAULT_ENCODER_PRESET, crf=DEFAULT_ENCODER_CRF)
```

**`video`**

The MP4 file the frames are encoded into as they come, if any.

**`frames`**

A function handed each frame, a `Frame` (see `FrameSink`).

**`plays`**

A function called as each play ends (see `PlayHook`).

**`take`**

A function handed the take's bytes as they are recorded, frame by frame, if the film is recorded as a take (see `Take`).

**`preset`**

The x264 preset the video is encoded with: faster presets make larger files.

**`crf`**

The video's quality, as x264's constant rate factor, from 0 to 51: lower is better, the default value is 18.

### fps

How many frames a second the film has: the configuration's when it began.

### video

The path of the video being written; None once it is written, and if there is none.

### frames

The function each drawn frame is handed to, if any.

### frame\_count

How many frames the film has so far, a hold counting every frame it lasts.

### plays

The plays and waits the scene has run, in order: each a `Play`.

### sections

The film's sections, in order: each a `Section`, lasting until the next begins. The first begins with the film.

### subcaptions

The captions the scene added (see `add_subcaption`); `captions` adds those of its speech.

### clips

The sounds the scene placed, in the order it placed them: each a `Clip`, from its start in scene time.

### export

How the video was made, once it is written: an `Export`; None until then, and with no video.

### soundtrack

The film's sound: its clips mixed over its length, at `RATE` samples a second, one column per channel; None if the scene placed no sound.

```python
film.soundtrack()
```

### cut

The sounds the film's end cuts short: each clip, with the seconds it loses.

```python
film.cut()
```

### subtitles

The film's `captions` as subtitles, in SubRip (`.srt`) form: what players, editors and video sites read beside a video.

```python
film.subtitles()
```

### captions

The film's captions, in order of their start: those the scene added, and its speech's, a line of a few words at a time as they are said.

```python
film.captions()
```

## Window

ManimGX's player in a window on this machine's screen, which plays the takes it is sent.

A window is a `Take`: hand it to `Scene.render` as `take`, and it plays the film as it is recorded. Once it is closed, a film sent to it is cut (see `Cut`).

Its viewer can ask for another of the file's scenes (N and P).

```python
m.Window(title='ManimGX', *, time=0.0)
```

**`title`**

The window's title.

**`time`**

Where its playhead starts, in seconds.

### failure

Why the window failed, if it did (no screen to open on, no GPU): it is closed.

### open

Whether the window is open: until its viewer closes it, or it is closed.

```python
window.open
```

### wait

Wait until the window is closed, at most `timeout` seconds; whether it was.

```python
window.wait(timeout=None)
```

### close

Close the window.

```python
window.close()
```

## What a film holds

### Frame

A frame of a film, as the film sends it: shown as frames `index` to `index + repeat - 1` of the video.

A frame the world holds still for is sent once, shown `repeat` times. Its pixels are drawn only when asked for, by `pixels`.

**`index`**

Where it is in the film: the number of the first frame it is shown as.

**`repeat`**

How many frames it is shown for.

**`draw`**

The function that draws its pixels.

**`key`**

Whether it begins a section of the film.

#### index

Where it is in the film: the number of the first frame it is shown as, from 0.

#### repeat

How many frames it is shown for: more than 1 for a hold.

#### key

Whether it begins a section of the film: the picture the section before it ends on.

#### pixels

Draw the frame, now.

Drawing is what a frame costs: ask only for the frames you keep, and before the film sends its next frame.

```python
frame.pixels()
```

Returns RGBA, a byte a channel, row after row from the top.

### Play

One play, or wait, of a scene, as its film keeps it: its number, when it began and ended, and where the scene's code played it.

#### index

Its number, from 0: plays and waits are counted together.

#### start

When it began, in seconds of scene time, exactly.

#### end

When it ended, in seconds of scene time, exactly.

#### where

Where the scene's code played it: the file and line of the innermost call outside manimgx; None if there is none.

### Section

A section of a film, as `next_section` begins one: it lasts until the next section begins, or the film ends.

#### name

Its name.

#### start

When it begins, in seconds of scene time: a frame's time, exactly.

#### frame

Its first frame's number: a keyframe of the video, where a player can start.

#### type

How a presentation plays it.

#### notes

What the presenter reads during it.

### Export

How a film's video was made: what `Film.export` holds once the video is written.

#### seconds

How long the video took, in seconds: from its start, as the scene began rendering, to its file written.

#### x264

Of those, the seconds spent in x264, the H.264 encoder (on a thread of its own).

#### converted

The share of the video's 16 × 16 pixel blocks converted for the encoder, from 0 to 1: the others had not changed since the frame before, and were skipped.

#### bytes

The size of the file, in bytes.

### Cut

An early end to a film: raised by a frame sink, a play hook or a take, it stops the scene there.

The film closes as it is: its video, if any, is written up to the last frame sent.

### Take

```python
Take = Callable[[bytes], object]
```

A function handed a film's take as it is recorded (see `Film`): bytes of the stream manimgx's player reads — uploads, frames and notes, then the film's sound and captions — in order, frame by frame; what it returns is ignored. It may raise `Cut` to end the film there: it is then sent nothing more (a `Window` closed by its viewer does).

### FrameSink

```python
FrameSink = Callable[[Frame], object]
```

A function handed each frame of a film as the film sends it, a `Frame` (see `Scene.render`); what it returns is ignored. It may raise `Cut` to end the film there.

### PlayHook

```python
PlayHook = Callable[[Play, tuple[Animation, ...]], object]
```

A function called as each play or wait of a film ends (see `Scene.render`), with the `Play` and the animations it played, the world as the play left it; what it returns is ignored. It may raise `Cut` to end the film there.

### manimgx.audio.sound.RATE

The soundtrack's sample rate: 48,000 samples a second, as video's sound has.
