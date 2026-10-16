# Updaters

**The film's code**

```python
import manimgx as m

class UpdatersHero(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(color=m.YELLOW).shift(3 * m.LEFT)
        label = m.Text("dot", font_size=36)
        label.add_updater(lambda mob: mob.next_to(dot, m.UP))
        trail = m.TracedPath(dot.get_center, stroke_color=m.YELLOW, stroke_width=4)
        self.add(trail, dot, label)
        self.play(dot.animate.shift(6 * m.RIGHT), run_time=2)
        self.play(m.Rotate(dot, m.PI, about_point=m.ORIGIN), run_time=2)
        self.wait()
```

An animation changes a mobject for its run time. An updater changes it at every frame, for as long as it is attached: it keeps a rule while other things move. A label stays above a dot, a number shows where a tracker is, a shape turns as time passes.

An updater is a function: ManimGX calls it with the mobject at every frame, in plays and in waits alike. A function that also takes `dt` gets the time since it last ran, in seconds, for motion that goes on: `lambda mob, dt: mob.rotate(dt)` turns a mobject a radian a second.

## Add an updater

### add\_updater

**Code**

```python
import manimgx as m

class MobjectAddUpdaterExample(m.Scene):
    def construct(self) -> None:
        hand = m.Line(m.ORIGIN, 3 * m.RIGHT, color=m.BLUE)
        # time-based: a quarter turn about the origin every second
        hand.add_updater(
            lambda mob, dt: mob.rotate(dt * m.PI / 2, about_point=m.ORIGIN)
        )
        dot = m.Dot(radius=0.2, color=m.YELLOW)
        # per frame: at the hand's end, wherever it is
        dot.add_updater(lambda mob: mob.move_to(hand.get_end()))
        self.add(hand, dot)
        self.wait(3)
```

Add an updater: a function that keeps the mobject updated as time passes.

An updater is a function of the mobject, run once a frame — to keep a relation, such as a label beside a dot — or, if it has a parameter named `dt`, of the mobject and `dt`: the seconds of scene time since it last ran, or since it was added, the mobject joined the scene, or its updating resumed. A time-based updater moves the mobject by the time that passed: `lambda mob, dt: mob.rotate(dt * PI)` turns it half a turn a second, at any frame rate. What an updater returns is ignored.

The scene runs the updaters of the mobjects in it at every frame, after the animations playing have moved them to the frame's instant, and at the end of each play and wait: mobject by mobject in the order they were added to the scene, a mobject's own before its submobjects', and a recorder after all the rest. So add a mobject that follows another after it, or it sees where the other's updaters left it at the instant before. Updaters keep running while an animation plays the mobject, beneath the animation (see `suspend_mobject_updating` among the animation options). A time-based updater steps on the scene's simulation clock, `config.simulation_rate` ticks a second, so it takes the same steps at any frame rate; declare one that does the same however its time is split a flow, and it runs exactly at every frame instead.

```python
mobject.add_updater(update_function, index=None, call_updater=False)
```

**`update_function`**

The updater: a function of the mobject, or of the mobject and `dt`.

**`index`**

Where it goes among the mobject's updaters, which run in order; None for last.

**`call_updater`**

Whether to run it once right away; a time-based one is handed a `dt` of 0.

        import manimgx as m

        class MobjectAddUpdaterExample(m.Scene):
            def construct(self) -> None:
                hand = m.Line(m.ORIGIN, 3 * m.RIGHT, color=m.BLUE)
                # time-based: a quarter turn about the origin every second
                hand.add_updater(
                    lambda mob, dt: mob.rotate(dt * m.PI / 2, about_point=m.ORIGIN)
                )
                dot = m.Dot(radius=0.2, color=m.YELLOW)
                # per frame: at the hand's end, wherever it is
                dot.add_updater(lambda mob: mob.move_to(hand.get_end()))
                self.add(hand, dot)
                self.wait(3)
        ```
    """
    if index is None:
        self.updaters.append(update_function)
    else:
        self.updaters.insert(index, update_function)
    if not _per_frame(update_function):
        self._since[update_function] = clock.now  # it integrates from now
    if call_updater:
        if _per_frame(update_function):
            update_function(self)
        else:
            cast("Callable[[Self, float], object]", update_function)(self, 0)
    return self
````

### remove\_updater

Remove an updater from the mobject, every time it was added.

This also cancels calls that have not yet run in the current update, including a recorder waiting for the other updaters to finish.

```python
mobject.remove_updater(update_function)
```

**`update_function`**

The updater to remove.

### clear\_updaters

Remove every updater of the mobject, including calls still waiting to run in the current update.

```python
mobject.clear_updaters(recursive=True)
```

**`recursive`**

Whether its whole family's updaters are removed too.

### get\_updaters

The mobject's own updaters, in the order they run.

Change them with add\_updater, remove\_updater and clear\_updaters, which keep their clocks with them.

```python
mobject.get_updaters()
```

Returns A snapshot of them.

### suspend\_updating

Stop the mobject's updaters from running, and its family's beneath it, until resume\_updating: nothing updated through a suspended mobject runs.

An animation suspends the updating of the mobject it plays while it plays, and runs the updaters beneath it instead (see add\_updater).

```python
mobject.suspend_updating(recursive=True)
```

**`recursive`**

Whether each member of its family is suspended too, so that it stays stopped where it is updated apart from the mobject (a member the scene also holds by itself), and when the mobject alone resumes.

### resume\_updating

Let the mobject's updaters run again, from now: the time they were suspended is not made up.

They are not run here: the scene runs them where it next brings the world — at the instant it is computing, when an animation resumes them as it finishes, else at the next one, such as the next frame.

```python
mobject.resume_updating(recursive=True)
```

**`recursive`**

Whether its whole family's updaters resume too: resumed alone, the mobject runs again, and the members beneath it that are not suspended themselves.

### update

Run each of the mobject's updaters once, now; nothing runs while its updating is suspended.

The scene runs updaters itself, at every frame: this runs them by hand, now.

```python
mobject.update(dt=0, recursive=True)
```

**`dt`**

The seconds handed to its time-based updaters.

**`recursive`**

Whether its submobjects' updaters run too, after its own.

### always

**Code**

```python
import manimgx as m

class MobjectAlwaysExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5).shift(4 * m.LEFT)
        label = m.Text("always above")
        label.always.next_to(square, m.UP)
        self.add(square, label)
        self.play(square.animate.shift(8 * m.RIGHT), run_time=2)
```

A proxy that turns each method call made on it into an updater: the call is made again every frame.

`label.always.next_to(dot, UP)` keeps the label above the dot, wherever the dot goes. Each call is also made right away, and adds one per-frame updater (see add\_updater); the proxy returns itself, so calls chain. The arguments are taken once, as written: pass the mobject to follow (`dot`), not its position (`dot.get_center()`), which stays where it was.

```python
mobject.always
```

        import manimgx as m

        class MobjectAlwaysExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(color=m.BLUE, fill_opacity=0.5).shift(4 * m.LEFT)
                label = m.Text("always above")
                label.always.next_to(square, m.UP)
                self.add(square, label)
                self.play(square.animate.shift(8 * m.RIGHT), run_time=2)
        ```
    """
    # CE's
    from manimgx.animation.transform import Always

    return Always(self)
````

## How time-based updaters run

ManimGX runs a time-based updater at each tick of the simulation clock, 60 times a second whatever the frame rate, so that a simulation gives the same result at every frame rate. A flow, which does the same however its time is split, runs at every frame instead; a recorder, which reads the world, runs after everything else.

### flow

**Code**

```python
import manimgx as m
from manimgx.mobject import flow

@flow
def orbit(dot: m.Mobject, dt: float) -> None:
    dot.rotate(dt * m.PI / 2, about_point=m.ORIGIN)  # a quarter turn a second

class FlowExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(3 * m.RIGHT, radius=0.25, color=m.YELLOW)
        dot.add_updater(orbit)
        self.add(m.Circle(radius=3, color=m.BLUE), dot)
        self.wait(3)
```

Declare a time-based updater a flow: one that does the same over some time however that time is split into steps.

A time-based updater is handed `dt`, the seconds since it last ran. Most compose: one that moves the mobject at a rate (`mob.shift(dt * velocity)`), or sets it by a function of the time it has run, does the same in one step of `dt` as in two of `dt / 2`. A flow runs at every instant the scene computes — each frame, and the end of each play and wait — handed exactly the time since, so every frame shows it at that frame's instant.

Any other time-based updater is simulated, since what it does may depend on its steps (an integrator, a ball that bounces): it steps on a clock of its own, `config.simulation_rate` ticks a second (60) and the end of each play and wait, so it takes the same steps at any frame rate, and a frame shows it as its last tick left it. While one is in the scene, the scene computes every tick, between frames too. Declare an updater that composes a flow to make it exact at every frame and to spare those ticks; always\_shift and always\_rotate add flows. An updater that only reads the world, as a traced path's does, is a recorder.

```python
manimgx.mobject.flow(updater)
```

**`updater`**

A time-based updater: a function of the mobject and `dt`.

Returns The same updater, declared a flow, to add with add\_updater.

        import manimgx as m
        from manimgx.mobject import flow

        @flow
        def orbit(dot: m.Mobject, dt: float) -> None:
            dot.rotate(dt * m.PI / 2, about_point=m.ORIGIN)  # a quarter turn a second

        class FlowExample(m.Scene):
            def construct(self) -> None:
                dot = m.Dot(3 * m.RIGHT, radius=0.25, color=m.YELLOW)
                dot.add_updater(orbit)
                self.add(m.Circle(radius=3, color=m.BLUE), dot)
                self.wait(3)
        ```
    """
    _FLOWS.add(_function(updater))
    return updater
````

### record

Declare a time-based updater a recorder: one that reads the world and changes only its own mobject, as a TracedPath's does.

The scene runs a recorder at every instant it computes — each tick of the simulation clock, each frame, and the end of each play and wait — once everything else is there: the animations playing, the mobjects' updaters and the scene's. At a frame or at the end of a play or wait, it runs twice: first on the world as time alone brought it there, as a tick sees it, then once the per-frame updaters have run, so it can tell their change apart (a traced path spreads it over the frame that ends there). A recorder is simulated (see flow): while one is in the scene, the scene computes the simulation clock's ticks.

```python
manimgx.mobject.record(updater)
```

**`updater`**

A time-based updater: a function of the mobject and `dt`, or such a method, decorated where its class defines it.

Returns The same updater, declared a recorder, to add with add\_updater.

## Ready-made updaters

### always\_redraw

**Code**

```python
import manimgx as m

class AlwaysRedrawExample(m.Scene):
    def construct(self) -> None:
        width = m.ValueTracker(2)
        box = m.always_redraw(
            lambda: m.Rectangle(width=width.get_value(), height=3, color=m.BLUE)
        )
        brace = m.always_redraw(lambda: m.Brace(box, m.DOWN, color=m.YELLOW))
        self.add(box, brace)
        self.play(width.animate.set_value(11), run_time=2)
        self.play(width.animate.set_value(5))
```

Make a mobject that is built anew every frame, by a function.

`func` builds the mobject now, and every frame the mobject becomes what `func` builds then (see `become`): it stays one object in the scene, and follows whatever `func` reads — value trackers, other mobjects. Use it for a shape that depends on others in a way no motion follows: a brace that fits a growing shape, a line between two moving dots, the area under a graph.

```python
m.always_redraw(func)
```

**`func`**

A function of no arguments that builds the mobject.

Returns add it to the scene.

        import manimgx as m

        class AlwaysRedrawExample(m.Scene):
            def construct(self) -> None:
                width = m.ValueTracker(2)
                box = m.always_redraw(
                    lambda: m.Rectangle(width=width.get_value(), height=3, color=m.BLUE)
                )
                brace = m.always_redraw(lambda: m.Brace(box, m.DOWN, color=m.YELLOW))
                self.add(box, brace)
                self.play(width.animate.set_value(11), run_time=2)
                self.play(width.animate.set_value(5))
        ```
    """
    mob = func()
    mob.add_updater(lambda m: m.become(func()))
    return mob
````

### always\_rotate

**Code**

```python
import manimgx as m

class AlwaysRotateExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        square.shift(3.5 * m.LEFT)
        m.always_rotate(square, rate=m.PI / 2)  # a quarter turn a second
        center = m.Dot(3.5 * m.RIGHT, color=m.YELLOW)
        moon = m.Dot(3.5 * m.RIGHT + 2 * m.UP, radius=0.25, color=m.TEAL)
        m.always_rotate(moon, rate=-m.PI, about_point=center.get_center())
        self.add(square, center, moon)
        self.wait(4)
```

Keep a mobject turning, at a steady speed.

It adds a time-based updater, a flow, so at every frame the mobject is at exactly the angle its speed has brought it to, through plays and waits alike.

```python
m.always_rotate(mobject, rate=20 * DEGREES, axis=OUT, **kwargs)
```

**`mobject`**

The mobject to turn.

**`rate`**

The speed, in radians per second; a positive one turns counterclockwise.

**`axis`**

The axis it turns about.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

Returns The mobject, with its updater.

        import manimgx as m

        class AlwaysRotateExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
                square.shift(3.5 * m.LEFT)
                m.always_rotate(square, rate=m.PI / 2)  # a quarter turn a second
                center = m.Dot(3.5 * m.RIGHT, color=m.YELLOW)
                moon = m.Dot(3.5 * m.RIGHT + 2 * m.UP, radius=0.25, color=m.TEAL)
                m.always_rotate(moon, rate=-m.PI, about_point=center.get_center())
                self.add(square, center, moon)
                self.wait(4)
        ```
    """
    mobject.add_updater(flow(lambda m, dt: m.rotate(dt * rate, axis, **kwargs)))
    return mobject
````

### always\_shift

**Code**

```python
import manimgx as m

class AlwaysShiftExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.8)
        square.shift(5 * m.LEFT)
        m.always_shift(square, m.RIGHT, rate=2.5)
        self.add(square)
        self.play(square.animate.set_color(m.YELLOW), run_time=2)
        self.wait(2)
```

Keep a mobject moving in a direction, at a steady speed.

It adds a time-based updater, a flow, so at every frame the mobject is exactly where its speed has brought it, through plays and waits alike.

```python
m.always_shift(mobject, direction=RIGHT, rate=0.1)
```

**`mobject`**

The mobject to move.

**`direction`**

The direction to move in; only its direction counts, not its length.

**`rate`**

The speed, in scene units per second.

Returns The mobject, with its updater.

        import manimgx as m

        class AlwaysShiftExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.8)
                square.shift(5 * m.LEFT)
                m.always_shift(square, m.RIGHT, rate=2.5)
                self.add(square)
                self.play(square.animate.set_color(m.YELLOW), run_time=2)
                self.wait(2)
        ```
    """
    unit = normalize(direction)
    mobject.add_updater(flow(lambda m, dt: m.shift(dt * rate * unit)))
    return mobject
````

### turn\_animation\_into\_updater

**Code**

```python
import manimgx as m

class TurnAnimationIntoUpdaterExample(m.Scene):
    def construct(self) -> None:
        shape = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
        squares = m.VGroup(*(shape.copy() for _ in range(3))).arrange(buff=1.5)
        self.add(squares)
        for i, square in enumerate(squares):  # half a second apart
            m.turn_animation_into_updater(
                m.Rotate(square, m.PI / 2, run_time=1), delay=0.5 * i
            )
        self.wait(2.5)
```

Play an animation from an updater of its mobject, on the mobject's own time, instead of in a play.

The animation begins at once: it takes its mobject as it is now, and shows its start. Its time then runs with the scene's, from now or from when the mobject joins the scene; after `delay` seconds it plays, at its run time and rate function. When it ends, it finishes and its updater is removed; with `cycle`, it starts over from its beginning instead, again and again. Nothing is added to the scene or taken out of it: add the mobject yourself. The animation and its time are the mobject's: a copy of it plays a copy of them, on itself.

```python
m.turn_animation_into_updater(animation, cycle=False, delay=0)
```

**`cycle`**

Whether it repeats forever.

**`delay`**

How long it waits before it starts, in seconds.

Returns The animation's mobject, with its updater.

        import manimgx as m

        class TurnAnimationIntoUpdaterExample(m.Scene):
            def construct(self) -> None:
                shape = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
                squares = m.VGroup(*(shape.copy() for _ in range(3))).arrange(buff=1.5)
                self.add(squares)
                for i, square in enumerate(squares):  # half a second apart
                    m.turn_animation_into_updater(
                        m.Rotate(square, m.PI / 2, run_time=1), delay=0.5 * i
                    )
                self.wait(2.5)
        ```
    """
    mobject = animation.mobject
    animation.suspend_mobject_updating = False
    animation.begin()
    animation.interpolate(
        0
    )  # the object is the animation's from now: at its start, until then
    # the animation and its time are kept on the mobject, so that a copy of it plays a copy
    # of them: the updater holds only their key, and plays those of the mobject it runs on
    key = next(_PLAYED_KEYS)
    played: dict[int, _Played] = mobject.__dict__.setdefault("_played", {})
    played[key] = _Played(animation, -delay)

    def update(m: Mobject, dt: float) -> None:
        state = m.__dict__.get("_played", {}).get(key)
        if state is None:  # nothing of its own to play
            return
        state.elapsed += dt  # its time now: what this frame shows
        if state.elapsed < 0:
            return
        animation, elapsed = state.animation, state.elapsed
        run_time = animation.get_run_time()
        if run_time > 0 and (cycle or elapsed < run_time):
            animation.interpolate(
                (elapsed / run_time) % 1 if cycle else elapsed / run_time
            )
            animation.advance(clock.now)
        else:
            animation.finish()
            m.remove_updater(update)
            del m.__dict__["_played"][key]

    mobject.add_updater(flow(update))  # the animation at the time it has run
    return mobject
````

### cycle\_animation

**Code**

```python
import manimgx as m

class CycleAnimationExample(m.Scene):
    def construct(self) -> None:
        orbit = m.Circle(radius=3, color=m.BLUE)
        planet = m.Dot(orbit.get_start(), radius=0.25, color=m.YELLOW)
        m.cycle_animation(
            m.MoveAlongPath(planet, orbit, rate_func=m.linear, run_time=2)
        )
        self.add(orbit, planet)
        self.wait(4)
```

Play an animation over and over, from an updater of its mobject: `turn_animation_into_updater` with `cycle`.

Each cycle starts the animation over from its beginning: an animation that does not end where it began jumps back at every cycle.

```python
m.cycle_animation(animation, delay=0)
```

**`delay`**

How long it waits before its first cycle, in seconds.

Returns The animation's mobject, with its updater.

        import manimgx as m

        class CycleAnimationExample(m.Scene):
            def construct(self) -> None:
                orbit = m.Circle(radius=3, color=m.BLUE)
                planet = m.Dot(orbit.get_start(), radius=0.25, color=m.YELLOW)
                m.cycle_animation(
                    m.MoveAlongPath(planet, orbit, rate_func=m.linear, run_time=2)
                )
                self.add(orbit, planet)
                self.wait(4)
        ```
    """
    return turn_animation_into_updater(animation, cycle=True, delay=delay)
````

## Updaters as animations

### UpdateFromFunc

**Code**

```python
import manimgx as m

class UpdateFromFuncExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(4 * m.LEFT, radius=0.2, color=m.YELLOW)
        label = m.Text("dot", font_size=60)
        self.add(dot, label)
        self.play(
            dot.animate.shift(8 * m.RIGHT),
            m.UpdateFromFunc(label, lambda mob: mob.next_to(dot, m.UP)),
            run_time=2,
        )
```

Call a function on a mobject at every frame, for the animation's run time.

The function gets the mobject, not the progress: use it to keep a mobject up to date while other animations play. The mobject's own updaters act on it directly (`suspend_mobject_updating` is False).

```python
m.UpdateFromFunc(mobject, update_function, **kwargs)
```

**`mobject`**

The mobject to update.

**`update_function`**

A function of the mobject, called at every frame.

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

It also takes the animation keywords.

### UpdateFromAlphaFunc

**Code**

```python
import manimgx as m

class UpdateFromAlphaFuncExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)

        def slide(mob: m.Square, alpha: float) -> None:
            mob.move_to((8 * alpha - 4) * m.RIGHT)
            mob.set_color(m.interpolate_color(m.BLUE, m.YELLOW, alpha))

        self.play(m.UpdateFromAlphaFunc(square, slide, run_time=2))
```

Call a function on a mobject at every frame, with the animation's progress.

The function gets the mobject and the progress, eased by the rate function, and sets the mobject as it is at that progress. The mobject's own updaters act on it directly (`suspend_mobject_updating` is False).

```python
m.UpdateFromAlphaFunc(mobject, update_function, **kwargs)
```

**`mobject`**

The mobject to update.

**`update_function`**

A function of the mobject and the eased progress, from 0 to 1.

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

It also takes the animation keywords.

### MaintainPositionRelativeTo

**Code**

```python
import manimgx as m

class MaintainPositionRelativeToExample(m.Scene):
    def construct(self) -> None:
        leader = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
        follower = m.Circle(color=m.YELLOW).next_to(leader, m.RIGHT, buff=0.5)
        m.VGroup(leader, follower).shift(4 * m.LEFT + 1.5 * m.DOWN)
        self.add(leader, follower)
        self.play(
            leader.animate.shift(5 * m.RIGHT + 3 * m.UP),
            m.MaintainPositionRelativeTo(follower, leader),
            run_time=2,
        )
```

Keep a mobject at the same offset from another's center, at every frame.

The offset is the one between their centers when the animation is made; play it together with the animations that move `tracked_mobject`.

```python
m.MaintainPositionRelativeTo(mobject, tracked_mobject, **kwargs)
```

**`mobject`**

The mobject to keep in place.

**`tracked_mobject`**

The mobject it follows.

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

It also takes the animation keywords.

## Trails and outlines

### TracedPath

**Code**

```python
import manimgx as m

class TracedPathExample(m.Scene):
    def construct(self) -> None:
        wheel = m.Circle(radius=1, color=m.BLUE).shift(5 * m.LEFT)
        dot = m.Dot(wheel.get_bottom(), radius=0.12, color=m.YELLOW)
        rolling = m.VGroup(wheel, dot)
        path = m.TracedPath(
            dot.get_center, stroke_color=m.YELLOW, stroke_width=4
        )

        def roll(mob: m.Mobject, dt: float) -> None:  # 2.5 radians a second
            mob.rotate(-2.5 * dt, about_point=mob[0].get_center())

        rolling.add_updater(roll)
        self.add(path, rolling)
        # 2.5 units a second: the wheel rolls without slipping
        self.play(
            rolling.animate.shift(10 * m.RIGHT), run_time=4, rate_func=m.linear
        )
```

The path a moving point traces: a line through everywhere it has been.

`traced_point_func` gives the point. The path records where it is at every tick of the simulation clock (`config.simulation_rate` times a second) and at the end of each play and wait, so it is the same path at any frame rate; at a frame between two ticks, it runs on to where the point is then. It traces while it is in the scene, from when it joins it, and at each instant once everything else has moved: its updater is a recorder.

A per-frame updater moves the point at frames only, so what it moves the point by at a frame is its change over the frame that ends there: the path spreads that move over the frame, in proportion to time. A point that a play carries while a per-frame updater turns it traces one smooth curve, not stairs. With `dissipating_time`, only the stretch traced in the last that many seconds remains.

```python
m.TracedPath(traced_point_func, dissipating_time=None, **kwargs)
```

**`traced_point_func`**

A function of no arguments that gives the point to trace (`dot.get_center`).

**`dissipating_time`**

How long each stretch of the path remains, in seconds; None: all of it remains.

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

It also takes the style keywords.

### AnimatedBoundary

**Code**

```python
import manimgx as m

class AnimatedBoundaryExample(m.Scene):
    def construct(self) -> None:
        word = m.Text("So shiny!", font_size=144)
        boundary = m.AnimatedBoundary(
            word,
            colors=[m.RED, m.YELLOW, m.BLUE],
            max_stroke_width=8,
            cycle_rate=1,  # a color a second
        )
        self.add(word, boundary)
        self.wait(3)
```

An outline that keeps drawing itself around a mobject, cycling through colors.

Each cycle draws the mobject's outline in the next color, while the outline the cycle before drew thins away; with `back_and_forth`, every other cycle draws it the other way around. It follows the mobject: every frame, it takes the mobject's outline as it is then. It draws only the outline: add it to the scene with the mobject.

```python
m.AnimatedBoundary(vmobject, colors=(BLUE_D, BLUE_B, BLUE_E, GREY_BROWN), max_stroke_width=3, cycle_rate=0.5, back_and_forth=True, draw_rate_func=smooth, fade_rate_func=smooth, **kwargs)
```

**`vmobject`**

The mobject to outline.

**`colors`**

The colors, one per cycle, in turn.

**`max_stroke_width`**

The outline's stroke width, in hundredths of a scene unit.

**`cycle_rate`**

How many cycles a second.

**`back_and_forth`**

Whether every other cycle draws the outline from its end back to its start.

**`draw_rate_func`**

How each drawing is paced: a rate function.

**`fade_rate_func`**

How each thinning away is paced: a rate function.

**`color`**

The color of both fill and stroke (default white); None for the class's default.

**`fill_color`**

The fill's color; `color` if not given. Several colors make a gradient along `sheen_direction`.

**`fill_opacity`**

The fill's opacity, from 0 to 1 (default 0: no fill).

**`stroke_color`**

The stroke's color; `color` if not given. Several colors make a gradient.

**`stroke_opacity`**

The stroke's opacity, from 0 to 1 (default 1).

**`stroke_width`**

The stroke's width, in hundredths of a scene unit (default 4; 0: no stroke).

**`background_stroke_color`**

The color of an outline drawn behind the fill (default black).

**`background_stroke_opacity`**

The outline's opacity, from 0 to 1 (default 1).

**`background_stroke_width`**

The outline's width, in hundredths of a scene unit (default 0: none).

**`sheen_factor`**

How much the colors lighten toward `sheen_direction`, from -1 to 1 (default 0); a negative factor darkens.

**`sheen_direction`**

The direction the colors lighten toward (default `UL`).

**`joint_type`**

How the stroke is joined where its path turns: round, beveled or mitered, as a two-dimensional scene draws it (see LineJointType; default AUTO: mitered).

**`cap_style`**

How the stroke ends, at each end it shows (an open path's, a dash's): round, butt or square, as a two-dimensional scene draws it (see CapStyleType; default AUTO: butt).

**`shade_in_3d`**

Whether a three-dimensional scene's light shades the mobject.

**`material`**

How its surface reflects the scene's lights in a three-dimensional scene (see Material); None: Manim's shading (default).

**`name`**

A name for the mobject; its class's name if not given.

**`z_index`**

Its place in the drawing order: a higher index is drawn over a lower one (default 0).

**`target`**

The state `MoveToTarget` moves the mobject to.

It also takes the style keywords.
