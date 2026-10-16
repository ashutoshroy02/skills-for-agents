# Together and in turn

**The film's code**

```python
import manimgx as m

class TogetherHero(m.Scene):
    def construct(self) -> None:
        dots = m.VGroup(*[m.Dot(radius=0.2, color=m.YELLOW) for _ in range(6)]).arrange(
            buff=0.8
        )
        self.play(
            m.LaggedStart(*[m.GrowFromCenter(dot) for dot in dots], lag_ratio=0.3)
        )
        self.play(m.Succession(*[dot.animate.shift(m.UP) for dot in dots], run_time=2))
        self.play(m.AnimationGroup(*[dot.animate.shift(m.DOWN) for dot in dots]))
        self.wait()
```

`self.play(a, b)` plays a and b together. A group plays animations as one: together, one after another, or each a little after the one before it. A group is an animation itself, so groups nest, and a group plays inside a larger play.

## AnimationGroup

**Code**

```python
import manimgx as m

class AnimationGroupExample(m.Scene):
    def construct(self) -> None:
        shapes = (
            m.VGroup(
                m.Square(color=m.BLUE, fill_opacity=0.5),
                m.Circle(color=m.YELLOW, fill_opacity=0.5),
                m.Triangle(color=m.GREEN, fill_opacity=0.5),
            )
            .scale(1.2)
            .arrange(buff=1)
        )
        self.play(
            m.AnimationGroup(
                m.Create(shapes[0]),
                m.FadeIn(shapes[1], shift=m.UP),
                m.GrowFromCenter(shapes[2]),
                lag_ratio=0.5,
            )
        )
```

Play animations together, each in its own window of the group's time.

The parts are laid out in time: each begins when the part before it has played `lag_ratio` of its run time (all together with the default 0, one after another at 1, overlapping in between), and plays for its own run time. The group lasts until its last part ends, unless given a `run_time`, which stretches or squeezes the whole layout to fit. Its rate function (by default `linear`) warps the group's time, and each part still eases its own window with its own.

A part begins when its window opens, taking its mobjects as they are then (and bringing its mobject into the scene, if it introduces it), and finishes when its window closes, whatever else is still playing, leaving the scene as it leaves it (a remover's mobject leaves it). A part whose window ends with the group's finishes with the group, where the group's rate function ends its time. Before its window a part has touched nothing; after it, what it did stays done. The group itself is not a mobject of the scene: it adds nothing of its own. `Scene.play` plays several animations as such a group.

```python
m.AnimationGroup(*animations, group=None, **kwargs)
```

**`*animations`**

The animations, or iterables of them.

**`group`**

The mobject the group animates; by default, a group of its parts' mobjects, but those that parts introduce.

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

### run\_time

How long the group plays, in seconds: the run time it was given, else where its last part ends.

```python
animation_group.run_time
```

## Succession

**Code**

```python
import manimgx as m

class SuccessionExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
        square.shift(3 * m.LEFT)
        self.play(
            m.Succession(
                m.Create(square),
                square.animate.shift(6 * m.RIGHT),
                m.Rotate(square, m.PI / 4),
                square.animate.set_color(m.YELLOW),
            )
        )
```

Play animations one after another.

An `AnimationGroup` whose `lag_ratio` is 1: each part begins when the one before it ends, from the state it left.

```python
m.Succession(*animations, group=None, **kwargs)
```

**`*animations`**

The animations, in order, or iterables of them.

**`group`**

The mobject the group animates; by default, a group of its parts' mobjects, but those that parts introduce.

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

## LaggedStart

**Code**

```python
import manimgx as m

class LaggedStartExample(m.Scene):
    def construct(self) -> None:
        dots = m.VGroup(*(m.Dot(radius=0.25, color=m.YELLOW) for _ in range(8)))
        dots.arrange(buff=0.8).shift(2 * m.UP)
        self.add(dots)
        self.play(
            m.LaggedStart(
                *(dot.animate.shift(4 * m.DOWN) for dot in dots), lag_ratio=0.2
            )
        )
```

Play animations one shortly after another, overlapping.

An `AnimationGroup` whose `lag_ratio` is small (0.05 by default): each part begins when the one before it has played that fraction of its run time.

```python
m.LaggedStart(*animations, group=None, **kwargs)
```

**`*animations`**

The animations, in order, or iterables of them.

**`group`**

The mobject the group animates; by default, a group of its parts' mobjects, but those that parts introduce.

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

## LaggedStartMap

**Code**

```python
import manimgx as m

class LaggedStartMapExample(m.Scene):
    def construct(self) -> None:
        dots = m.VGroup(*(m.Dot(radius=0.2) for _ in range(35)))
        dots.arrange_in_grid(rows=5, cols=7, buff=0.6)
        self.play(m.LaggedStartMap(m.GrowFromCenter, dots, lag_ratio=0.1))
```

Play an animation on each submobject of a mobject, one shortly after another.

Each submobject's animation is `animation_class(*arg_creator(submobject), **kwargs)` (by default, `animation_class(submobject, **kwargs)`), and they play as a `LaggedStart`. `run_time` (2 seconds by default) and `lag_ratio` time the whole; every other option goes to each animation.

```python
m.LaggedStartMap(animation_class, mobject, arg_creator=None, **kwargs)
```

**`animation_class`**

The animation to play on each submobject: a class, or any function returning an animation.

**`mobject`**

The mobject whose submobjects are animated.

**`arg_creator`**

A function from a submobject to the animation's positional arguments; None for the submobject alone.

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

## ChangeSpeed

**Code**

```python
import manimgx as m

class ChangeSpeedExample(m.Scene):
    def construct(self) -> None:
        steady = m.Dot(5 * m.LEFT + m.UP, radius=0.25, color=m.BLUE)
        slowed = m.Dot(5 * m.LEFT + m.DOWN, radius=0.25, color=m.YELLOW)
        self.add(steady, slowed)
        self.play(
            steady.animate(run_time=2, rate_func=m.linear).set_x(5),
            m.ChangeSpeed(
                slowed.animate(run_time=2, rate_func=m.linear).set_x(5),
                speedinfo={0.3: 1, 0.4: 0.2, 0.6: 0.2, 0.7: 1},
            ),
        )
```

Play an animation faster or slower along the way: at speeds that change as it plays.

`speedinfo` gives speeds at points of the animation's progress: `{0.5: 2}` plays it at its own speed at the start, speeding up to twice as fast at its middle, and twice as fast from there on. Between two points the speed changes steadily (at a constant acceleration, in the scene's time), so the stretch from progress `a` to `b`, at speeds `v` and `w`, takes `(b - a) · 2 / (v + w)` of the animation's run time; the play lasts as long as its stretches take. Unless given, the speed at the start is 1 and the speed at the end the last point's.

With `affects_speed_updaters`, the updaters added with `ChangeSpeed.add_updater` run at the same speeds while it plays, so that whatever they move keeps pace with the animation.

The speeds change only the animation's timing: it keeps its own rate function (and its parts' stagger), so at a speed of 1 throughout it is the animation itself.

```python
m.ChangeSpeed(anim, speedinfo, affects_speed_updaters=True, **kwargs)
```

**`anim`**

The animation to play.

**`speedinfo`**

Speeds at points of the animation's progress, from 0 to 1: a speed of 2 plays it twice as fast, 0.5 half as fast.

**`affects_speed_updaters`**

Whether the updaters added with `ChangeSpeed.add_updater` follow the speeds while it plays.

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

### add\_updater

Add an updater to a mobject whose time follows the speed of any `ChangeSpeed` playing.

A time-based updater added this way is handed, as `dt`, the time of a clock that runs with the scene's, except while a `ChangeSpeed` with `affects_speed_updaters` plays: then it runs at that `ChangeSpeed`'s speeds (its `speedinfo`, whatever its rate function eases), and while several play at once, at the speeds of the one that began last. The clock never runs backward. It keeps its kind: a flow stays a flow, and any other time-based updater still steps on the simulation clock. A per-frame updater has no time, and is added as it is.

```python
ChangeSpeed.add_updater(mobject, update_function, index=None, call_updater=False)
```

**`mobject`**

The mobject to add it to.

**`update_function`**

The updater: a function of the mobject, or of the mobject and `dt` (see `add_updater`).

**`index`**

Where it goes among the mobject's updaters, which run in order; None for last.

**`call_updater`**

Whether to run it once right away; a time-based one is handed a `dt` of 0.

## Wait

**Code**

```python
import manimgx as m

class WaitExample(m.Scene):
    def construct(self) -> None:
        finish = m.Line(3 * m.UP, 3 * m.DOWN, color=m.RED).shift(3 * m.RIGHT)
        dot = m.Dot(4 * m.LEFT, radius=0.3, color=m.YELLOW)
        dot.add_updater(lambda mob, dt: mob.shift(3 * dt * m.RIGHT))
        self.add(finish, dot)
        self.play(m.Wait(10, stop_condition=lambda: dot.get_x() >= 3))
```

Let the scene's time run on, animating nothing.

The scene's updaters and its mobjects' keep running through it; `Scene.wait` plays one. Played alone, it can end early, at `stop_condition`, or freeze the frame; in a composition, it only takes up its time.

```python
m.Wait(run_time=1, stop_condition=None, frozen_frame=None, **kwargs)
```

**`run_time`**

How long it lasts, in seconds.

**`stop_condition`**

A function checked at every frame: the wait ends at the first frame at which it returns True. None: it lasts its whole run time.

**`frozen_frame`**

Whether time stands still: one frame is held, and the updaters do not run, then go on as if no time had passed. It cannot be combined with a `stop_condition` (a ValueError).

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

## Add

**Code**

```python
import manimgx as m

class AddExample(m.Scene):
    def construct(self) -> None:
        words = m.VGroup(
            *(m.Text(word, font_size=96) for word in ("one", "two", "three"))
        ).arrange(m.DOWN, buff=0.5)
        box = m.SurroundingRectangle(words, buff=0.5, color=m.BLUE)
        self.play(
            m.Create(box, run_time=3),
            m.Succession(*(m.Add(word, run_time=1) for word in words)),
        )
```

Add mobjects to the scene at a moment of a composition.

It adds its mobjects when it begins and, by default, takes no time: in a `Succession`, they appear when the animations before it have finished. With a `run_time`, it holds that long after adding them.

```python
m.Add(*mobjects, **kwargs)
```

**`*mobjects`**

The mobjects to add; several are added as one group.

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
