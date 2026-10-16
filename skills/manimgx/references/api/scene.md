# Scene

**The film's code**

```python
import manimgx as m

class SceneHero(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        self.add(square)
        self.wait(0.5)
        self.play(square.animate.shift(2 * m.RIGHT), run_time=1)
        self.next_section("turn")
        self.play(square.animate.rotate(m.PI / 4))
        self.remove(square)
        self.wait(0.5)
```

A scene runs its `construct` method once, from top to bottom, to make its video. Nothing in `construct` shows until a play or an add puts it in the scene, and the scene's time moves only in a play or a wait: each frame of the video shows the scene at its own exact time.

A scene also speaks and plays sounds: see [Sound](<https://manimgx.academa.ai/reference/sound/index.md>) and [Voice](<https://manimgx.academa.ai/reference/sound/voice/index.md>).

## Scene

**Code**

```python
import manimgx as m

class SceneExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        self.play(m.Create(square))  # from 0 s to 1 s
        self.wait()  # from 1 s to 2 s
        self.play(square.animate.rotate(m.PI / 4))  # from 2 s to 3 s
```

A scene: one video, and what happens in it.

Make a class from it, and write what happens in its `construct` method: ManimGX runs it once, from top to bottom, and `render` records the video. A mobject shows from the moment the scene holds it (`add` puts one in). Time passes only in `play` and `wait`: whatever `construct` does between them happens at one moment.

Each frame shows the scene at its own exact time, so a scene is the same at every frame rate: a second of animation is 60 frames at 60 frames a second, and 30 at 30. When `construct` ends, a last frame shows the scene as it ends, so that its last animation is seen landing. The methods that change a scene give it back, so that their calls chain.

```python
class MyScene(m.Scene):
```

## What happens

### construct

Describe the scene, what happens and when: override it.

`render` runs it once, from top to bottom, and the film is what it leaves behind. It is ordinary Python: loops, functions and variables work as they do anywhere.

```python
self.construct()
```

### setup

Prepare the scene: `render` calls it before `construct`.

It does nothing unless overridden: override it for what several scenes share, in a class they derive from.

```python
self.setup()
```

### tear\_down

Finish the scene: `render` calls it after `construct`, before the closing frame.

It does nothing unless overridden.

```python
self.tear_down()
```

## Time

### play

**Code**

```python
import manimgx as m

class ScenePlayExample(m.Scene):
    def construct(self) -> None:
        colors = (m.BLUE, m.YELLOW, m.GREEN)
        dots = m.VGroup(*(m.Dot(radius=0.3, color=c) for c in colors))
        dots.arrange(m.DOWN, buff=1.5).shift(5 * m.LEFT)
        self.add(dots)
        self.play(  # all three begin now; the play lasts 3 s
            dots[0].animate(run_time=1).shift(10 * m.RIGHT),
            dots[1].animate(run_time=2).shift(10 * m.RIGHT),
            dots[2].animate(run_time=3).shift(10 * m.RIGHT),
            rate_func=m.linear,  # for each of the three
        )
```

Play animations, together, from the scene's present time.

Each animation starts now and lasts its own run time, and ends when its time is up, whatever else still plays: the play lasts as long as the longest one. Then `construct` goes on, at the time the play ended. To play animations one after another, or each a little after the one before it, play a `Succession` or a `LaggedStart`.

A play brings into the scene what its animations change, if the scene doesn't hold it yet, in the order given. An animation that brings its mobject in (`Create`, `FadeIn`, …) adds it as it starts, and a replacement adds the mobject it turns into as it ends. One that takes its mobject out (`FadeOut`, …) removes it as it ends. A `Wait` played alone is a `wait`.

```python
self.play(*animations, **options)
```

**`*animations`**

The animations, or iterables of them; at least one.

**`run_time`**

How long the animation plays, in seconds (default 1).

**`lag_ratio`**

How the parts of the mobject are staggered: each begins this fraction of its run after the one before it begins (default 0: all together; 1: one after another).

**`rate_func`**

How the animation's progress runs with time: a function from \[0, 1\] to \[0, 1\] (default `smooth`; see rate functions).

**`reverse_rate_function`**

Whether to run the animation backward (default False).

**`name`**

A name for the animation.

**`remover`**

Whether the mobject leaves the scene when the animation finishes (default False).

**`suspend_mobject_updating`**

Whether the mobject's updaters run beneath the animation (default True): they keep acting on the mobject, and each frame shows the animation applied to the result. If False, they act on the animated mobject itself.

**`introducer`**

Whether the mobject joins the scene when the animation begins (default False); otherwise the play brings it in when the play begins, if the scene lacks it.

**`use_override`**

Whether a mobject whose class plays another animation in place of this one does so (default True).

It also takes the transform keywords.

        import manimgx as m

        class ScenePlayExample(m.Scene):
            def construct(self) -> None:
                colors = (m.BLUE, m.YELLOW, m.GREEN)
                dots = m.VGroup(*(m.Dot(radius=0.3, color=c) for c in colors))
                dots.arrange(m.DOWN, buff=1.5).shift(5 * m.LEFT)
                self.add(dots)
                self.play(  # all three begin now; the play lasts 3 s
                    dots[0].animate(run_time=1).shift(10 * m.RIGHT),
                    dots[1].animate(run_time=2).shift(10 * m.RIGHT),
                    dots[2].animate(run_time=3).shift(10 * m.RIGHT),
                    rate_func=m.linear,  # for each of the three
                )
        ```
    """
    from manimgx.animation.timeline import AnimationGroup, Wait, _flatten, prepare
    from manimgx.animation.transform import Compositor

    anims = [prepare(a) for a in _flatten(animations)]
    if not anims:
        raise ValueError("Called Scene.play with no animations")
    for anim in anims:
        for key, value in options.items():
            if value is not None:
                setattr(anim, key, value)
    start, index, where = self.clock, self.num_plays, _written()
    wait = anims[0] if len(anims) == 1 and isinstance(anims[0], Wait) else None
    self.num_plays += 1
    if wait is not None:
        end = start + wait._duration
        self._run(end, stop=wait.stop_condition, frozen=bool(wait.is_static_wait))
    else:
        anim = (
            anims[0]
            if len(anims) == 1
            else AnimationGroup(
                *anims, group=Group(), suspend_mobject_updating=False
            )
        )
        end = start + anim._duration
        self.compositor, self._animation = Compositor(), anim
        try:
            self._play(anim, start, end)
        finally:
            self.compositor, self._animation = None, None
    self.film.played(Play(index, start, self.clock, where), tuple(anims))
````

### wait

**Code**

```python
import manimgx as m

class SceneWaitExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        square.add_updater(lambda mob, dt: mob.rotate(dt * m.PI / 3))
        self.add(square)
        self.wait(2)  # time passes: the updater turns the square
        self.wait(1, frozen_frame=True)  # the picture holds
        self.wait(2)  # it turns on from where it stopped
```

Let time pass, playing nothing: the updaters keep running.

The video goes on for `duration` seconds, and `construct` goes on at their end. With a `stop_condition`, the wait ends at the first frame at which the condition holds, and the scene goes on from that frame's time. With `frozen_frame`, the picture holds instead: the video goes on for `duration`, but nothing moves, no updater runs, and time-based updaters go on afterward as if no time had passed (see `pause`).

```python
self.wait(duration=DEFAULT_WAIT_TIME, stop_condition=None, frozen_frame=None)
```

**`duration`**

How long, in seconds.

**`stop_condition`**

A function of no arguments, checked at every frame once it is drawn: the wait ends at the first at which it returns True. None: the wait lasts its whole duration.

**`frozen_frame`**

Whether the picture holds while the world stands still; it cannot be combined with a `stop_condition` (a ValueError). None or False: time runs.

        import manimgx as m

        class SceneWaitExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
                square.add_updater(lambda mob, dt: mob.rotate(dt * m.PI / 3))
                self.add(square)
                self.wait(2)  # time passes: the updater turns the square
                self.wait(1, frozen_frame=True)  # the picture holds
                self.wait(2)  # it turns on from where it stopped
        ```
    """
    from manimgx.animation.timeline import Wait

    self.play(
        Wait(
            run_time=duration,
            stop_condition=stop_condition,
            frozen_frame=frozen_frame,
        )
    )
````

### pause

Hold the picture while the world stands still: a `wait` with `frozen_frame`.

The video goes on for `duration`; no updater runs, and time-based updaters go on afterwards as if no time had passed.

```python
self.pause(duration=DEFAULT_WAIT_TIME)
```

**`duration`**

How long, in seconds.

### wait\_until

Let time pass until a condition holds: a `wait` that ends at the first frame at which `stop_condition` returns True, or after `max_time` seconds.

```python
self.wait_until(stop_condition, max_time=60)
```

**`stop_condition`**

A function of no arguments, checked at every frame once it is drawn.

**`max_time`**

The longest it waits, in seconds.

### time

The scene's time, in seconds.

In `construct`, it is 0 when the scene begins, and the end of each play or wait once it returns. During a play, while animations and updaters run, it is the time of the frame being made.

```python
self.time
```

## What it shows

### add

**Code**

```python
import manimgx as m

class SceneAddExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3.5, color=m.BLUE, fill_opacity=1)
        circle = m.Circle(radius=1.8, color=m.YELLOW, fill_opacity=1)
        circle.shift(1.8 * m.RIGHT)
        self.add(square, circle)  # the circle, added last, is on top
        self.wait()
        self.add(square)  # adding it again brings it to the front
        self.wait()
```

Put mobjects in the scene, from now on, in front of those it holds.

Each is drawn over the mobjects added before it (at an equal z-index), and under the foreground mobjects. A mobject the scene holds already moves to the front. One that is part of a group the scene holds is taken out of the group's place: the group is split, its other members staying where they are, each on its own (and the group's own updaters no longer run); a group added takes its members from wherever the scene held them. The updaters of the mobjects added run from now on: a time-based one's first `dt` counts from the moment its mobject joins the scene.

```python
self.add(*mobjects)
```

**`*mobjects`**

The mobjects, in order: the last is drawn on top.

        import manimgx as m

        class SceneAddExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=3.5, color=m.BLUE, fill_opacity=1)
                circle = m.Circle(radius=1.8, color=m.YELLOW, fill_opacity=1)
                circle.shift(1.8 * m.RIGHT)
                self.add(square, circle)  # the circle, added last, is on top
                self.wait()
                self.add(square)  # adding it again brings it to the front
                self.wait()
        ```
    """
    if any(m.updaters for mob in mobjects for m in mob.get_family()):
        present = {id(m) for m in self.get_mobject_family_members()}
        for mob in mobjects:  # joining the world: its updaters are live from now
            for m in mob.get_family():
                if id(m) not in present:
                    m._stamp(clock.now, recursive=False)
    new = remove_list_redundancies([*mobjects, *self.foreground_mobjects])
    self.mobjects = _restructure(self.mobjects, new) + new
    return self
````

### remove

Take mobjects out of the scene: they are no longer drawn, and their updaters stop.

A mobject that is part of a group the scene holds is taken out the same way: the group is split, its other members staying in the scene, each on its own. A mobject the scene does not hold is ignored. The mobjects themselves are not changed: adding one again shows it as it is then.

```python
self.remove(*mobjects)
```

**`*mobjects`**

The mobjects to take out.

### clear

Take every mobject out of the scene, the foreground ones too; the scene's own updaters stay.

```python
self.clear()
```

### replace

Put a mobject in the scene in another's place: where the other is drawn, even inside a group, which then holds the new one.

`new` is first taken out of the list it joins, if it is there. `ReplacementTransform` ends with it. A mobject the scene does not hold raises a ValueError.

```python
self.replace(old, new)
```

**`old`**

The mobject to replace: one the scene holds, or a part of one.

**`new`**

The mobject to put in its place.

### bring\_to\_front

Draw mobjects over the others, but under the foreground mobjects: the same as `add`.

```python
self.bring_to_front(*mobjects)
```

**`*mobjects`**

The mobjects, in order: the last is drawn on top.

### bring\_to\_back

Draw mobjects under all the others, at an equal z-index: they move to the start of the scene's mobjects, out of the foreground if they were in it.

A mobject the scene does not hold is added there, at the bottom.

```python
self.bring_to_back(*mobjects)
```

**`*mobjects`**

The mobjects, in order: the first is drawn at the bottom.

### add\_foreground\_mobjects

Put mobjects in the scene, in front: drawn over all the others, at an equal z-index, even those added after them.

```python
self.add_foreground_mobjects(*mobjects)
```

**`*mobjects`**

The mobjects, in order: the last is drawn on top.

### remove\_foreground\_mobjects

Take mobjects out of the front: they stay in the scene, where they are in its drawing order, and mobjects added later are drawn over them.

```python
self.remove_foreground_mobjects(*mobjects)
```

### mobjects

The mobjects the scene holds, in drawing order: each is drawn over those before it, at an equal z-index. `add` and `remove` change it.

### foreground\_mobjects

The mobjects kept in front: drawn over all the others, at an equal z-index (see `add_foreground_mobjects`). They are among the scene's `mobjects` too.

## The scene's own updaters

### add\_updater

Add an updater to the scene itself: a function it calls with the time that passed.

It is handed `dt`, the scene time in seconds since it last ran (or was added), at each instant the scene computes, after the updaters of the mobjects. It steps as a mobject's time-based updater does: on the simulation clock (`config.simulation_rate` ticks a second, and the end of each play and wait), unless it is a flow, which runs at every frame. What it returns is ignored.

```python
self.add_updater(func)
```

**`func`**

The updater: a function of one parameter, named `dt`.

### remove\_updater

Remove an updater from the scene, every time it was added.

This also cancels calls that have not yet run in the current update.

```python
self.remove_updater(func)
```

**`func`**

The updater.

## Sections

### next\_section

Begin a section of the film here: a slide, when the film is presented.

A film is a row of sections, each lasting until the next begins (the first begins with the film). Presented (`manimgx present`), the film plays a section and, by its type, stops at its end until the presenter goes on, goes on by itself, or plays it again and again until the presenter goes on. A section begins at a frame, whose picture a presentation stops on: if the scene's time falls between two frames, the world holds still until the next one. Rendered, a film just plays through its sections.

```python
self.next_section(name='unnamed', section_type='default.normal', skip_animations=False, *, notes='')
```

**`name`**

The section's name.

**`section_type`**

How a presentation plays the section that begins here: `"default.normal"` (or `"presentation.normal"`) stops at its end; `"presentation.skip"` goes on by itself; `"presentation.loop"` plays it again until the presenter goes on; `"presentation.complete_loop"` too, finishing its round first.

**`skip_animations`**

Accepted for Manim compatibility; ignored.

**`notes`**

What the presenter reads during the section.

## Its camera and its film

### camera

The scene's camera: what a frame shows. Move, scale or animate its `frame` to pan and zoom.

### frame

How many frames the scene has recorded: the number of the next one, which shows the world at `frame / fps` seconds.

### three\_d

Whether the scene's camera sees in three dimensions: True for a `ThreeDScene`.

### film

The film the scene records: `render` makes a new one, and returns it.

### num\_plays

How many plays and waits the scene has run.
