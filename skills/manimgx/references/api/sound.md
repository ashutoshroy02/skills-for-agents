# Sound

**The film's code**

```python
import manimgx as m
import numpy as np

class SoundHero(m.Scene):
    def construct(self) -> None:
        def tone(t: np.ndarray) -> np.ndarray:
            return 0.3 * np.sin(2 * np.pi * 440 * t) * np.exp(-3 * t)

        dots = m.VGroup(
            *[m.Dot(radius=0.25, color=m.YELLOW) for _ in range(4)]
        ).arrange(buff=1)
        for dot in dots:
            self.play(
                m.FadeIn(dot, scale=2), m.Sound.of(tone, duration=0.5), run_time=0.5
            )
        self.wait()
```

A sound is read from a file (WAV, MP3, AAC, FLAC and the other usual kinds), or made by a function of time. ManimGX places each sound at its moment in the video, and mixes them into one sound track.

Give a sound to `play` with animations, and it starts with them. To start one at any moment, add it: the scene goes on while it plays. A sound plays to its end, or until you stop the clip that adding it gives back.

A sound's methods make a changed sound: quieter or louder, faded in or out, trimmed, looped, faster, panned, or ducked under a voice.

## Sound

A sound a film plays.

Make one from a file, the bytes of one, or samples; edit it (each edit makes a new sound); place it in a scene: `add_sound` starts it now and takes no time, while `play` plays it as a part of the play, which then lasts at least as long as the sound. In a composition it starts when its window opens: `LaggedStart(*(AnimationGroup(FadeIn(d), click) for d in dots))` clicks as each dot appears. It changes nothing on screen, and a play's `run_time` does not change it: a sound lasts its `duration`.

```python
m.Sound(source, *, rate=None)
```

**`source`**

A file's path, a file's bytes, or samples: floats from -1 to 1, one column per channel (a 1-D array is mono), copied as they are given.

**`rate`**

The samples' rate, in samples a second; only for samples.

### samples

Its samples at `RATE`: floats, one column per channel (1 or 2).

```python
sound.samples
```

### duration

How long it lasts, in seconds (inf for a sound looped until stopped).

```python
sound.duration
```

### run\_time

Its duration: a sound plays for as long as it lasts. An endless one (`loop()`) cannot be played: add it (`add_sound`), and stop it.

```python
sound.run_time
```

### gain

This sound louder by `decibels` (quieter if negative: -6 halves it).

```python
sound.gain(decibels)
```

### fade\_in

This sound fading in from silence over its first `seconds`.

```python
sound.fade_in(seconds)
```

### fade\_out

This sound fading out to silence over its last `seconds`.

```python
sound.fade_out(seconds)
```

### trim

The part of this sound from `start` to `end` seconds (None: its end).

```python
sound.trim(start=0.0, end=None)
```

### loop

This sound repeated to last `duration` seconds; None: until the film ends, or until its clip is stopped.

```python
sound.loop(duration=None)
```

### speed

This sound played `factor` times as fast, as a tape is: higher and shorter.

The resulting speed must be finite and positive.

```python
sound.speed(factor)
```

### pan

This sound placed from -1 (left) through 0 (center) to 1 (right).

```python
sound.pan(position)
```

### duck

This sound dipping by `decibels` while anything speaks (while a `Speech` plays): music under a narration. It eases down `DUCK_ATTACK` seconds before the speech and back up over `DUCK_RELEASE` after.

```python
sound.duck(decibels=12)
```

### of

`Sound.of(lambda t: 0.3 * np.sin(2 * np.pi * 440 * t), 1)`: a second of A.

A sound made by a function of time: `function(t)`, given the times of its samples (seconds, an array), returns their values (-1 to 1).

```python
Sound.of(function, duration)
```

## add\_sound

Start a sound: now, or `time_offset` seconds from now; it takes no time.

The scene goes on at once, and the sound plays over whatever follows, until it ends (or the film does, or its clip is stopped). Called by an updater, it starts at the instant the updater runs for: a bounce sounds exactly at the bounce. To wait for a sound, `play` it instead.

```python
self.add_sound(sound, time_offset=0, gain=None)
```

**`sound`**

The sound, or its file.

**`time_offset`**

How long after now it starts, in seconds.

**`gain`**

How much louder it plays, in decibels (negative: quieter).

Returns `stop` it to end it early.

## Clip

A sound as a film plays it: from `start`, in seconds of scene time, until it ends or is stopped. `add_sound` returns it.

### stop

Stop the sound: it fades out from now (the instant the scene is computing) over `fade` seconds, and is silent after.

```python
clip.stop(fade=0.05)
```
