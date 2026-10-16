# Animate a change

**The film's code**

```python
import manimgx as m

class AnimateHero(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        self.play(m.Create(square))
        self.play(square.animate.shift(3 * m.RIGHT).set_color(m.YELLOW))
        self.play(square.animate(run_time=2).rotate(m.PI / 2).scale(0.5))
        self.play(square.animate.move_to(m.ORIGIN).set_color(m.BLUE))
```

`square.shift(m.RIGHT)` moves the square at once. `square.animate.shift(m.RIGHT)` makes an animation that moves it: give it to `play`, and the square moves for the animation's run time. Chain several calls after `.animate`, and they happen together. Give `.animate` the animation keywords, `square.animate(run_time=2)`, to time it.

`.animate` goes from the mobject as it is when the animation starts to the mobject as the calls leave it: each point travels on a straight line, unless you give a `path_arc`.

## animate

**Code**

```python
import manimgx as m

class MobjectAnimateExample(m.Scene):
    def construct(self) -> None:
        triangle = m.Triangle(color=m.BLUE, fill_opacity=0.5)
        self.add(triangle)
        self.play(triangle.animate.shift(3 * m.LEFT).scale(1.5))
        self.play(triangle.animate.rotate(m.PI).set_color(m.YELLOW))
        self.play(triangle.animate(path_arc=m.PI).move_to(3 * m.RIGHT))
```

An animation of the mobject, built from the method calls made on it.

`square.animate.shift(RIGHT).scale(2)` is an animation that moves the square right and doubles its size: pass it to Scene.play. Each call is recorded — and tried at once on a copy, so a wrong call fails where it is written — and returns the animation, so calls chain. The calls are carried out on the mobject as it is when the animation begins, and the animation tweens it from that state to the result: in `Succession(square.animate.shift(RIGHT), square.animate.rotate(PI / 2))`, the square turns about its center where the shift left it. When the animation finishes, the calls are carried out on the mobject itself.

The motion follows the calls: a turn among them (`rotate`, `flip`) turns the mobject rigidly about its pivot, through its whole angle (`rotate(TAU)` is a full turn); every other call moves its center straight; and the rest of the change (a size, a color, a new shape) blends along the way. Call `animate` with options before any method — `square.animate(run_time=2, rate_func=linear).shift(UP)` — to set the animation's Transform options; a `path_arc` or a `path_func` among them replaces the motion. Call it with a function — `square.animate(lambda s: s.shift(UP))` — to record that function as a call. Call a method of your own class so: through `animate`, a type checker knows only ManimGX's methods, but it checks a function against the mobject's class.

```python
mobject.animate
```

        import manimgx as m

        class MobjectAnimateExample(m.Scene):
            def construct(self) -> None:
                triangle = m.Triangle(color=m.BLUE, fill_opacity=0.5)
                self.add(triangle)
                self.play(triangle.animate.shift(3 * m.LEFT).scale(1.5))
                self.play(triangle.animate.rotate(m.PI).set_color(m.YELLOW))
                self.play(triangle.animate(path_arc=m.PI).move_to(3 * m.RIGHT))
        ```
    """
    from manimgx.animation.transform import Animate

    return Animate(self)
````

## Animate

**Code**

```python
import manimgx as m

class AnimateExample(m.Scene):
    def construct(self) -> None:
        bar = m.Rectangle(width=3, height=1, color=m.BLUE, fill_opacity=0.5)
        self.add(bar.shift(4 * m.LEFT))
        self.play(
            bar.animate(run_time=2)
            .shift(8 * m.RIGHT)
            .rotate(m.PI / 2)
            .set_color(m.YELLOW)
        )
```

An animation of a mobject's method calls.

It is what `mobject.animate` returns. Call methods on it as on the mobject, `square.animate.shift(RIGHT).scale(2)`, and play it: it is the animation. Each call is recorded and tried at once on a copy, so a wrong call fails where it is written, and the calls are carried out on the mobject as it is when the animation begins (in a `Succession`, after the parts before it). When it finishes, the mobject is exactly what the calls make of it.

The mobject moves as the calls do: a turn among them (`rotate`, `flip`) turns it rigidly, through its whole angle (`rotate(TAU)` is a full turn), about its pivot as the motion carries it; any other call moves its center in a straight line; and the rest of the change (a scale, a color, a new shape) happens along the way. A `path_arc` or `path_func` of its own replaces that motion.

Called before any method, it takes the animation's options: `square.animate(run_time=2, rate_func=linear).shift(RIGHT)`. It also takes an edit, a function applied to the mobject as a method would be: `square.animate(lambda mob: mob.shift(RIGHT))`.

```python
m.Animate(mobject)
```

**`mobject`**

The mobject whose method calls are animated.

## To a prepared state

### MoveToTarget

**Code**

```python
import manimgx as m

class MoveToTargetExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=2, color=m.BLUE).shift(3 * m.LEFT)
        target = circle.generate_target()
        target.set_fill(m.GREEN, opacity=0.5).scale(0.5).shift(6 * m.RIGHT)
        self.add(circle)
        self.play(m.MoveToTarget(circle))
```

Transform a mobject into its `target`.

Make the target first with `generate_target`, a copy of the mobject, and change it as you like; the animation transforms the mobject into it. A mobject without a target raises a ValueError.

```python
m.MoveToTarget(mobject, **kwargs)
```

**`mobject`**

The mobject to transform; its `target` is what it becomes.

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

### Restore

**Code**

```python
import manimgx as m

class RestoreExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        square.save_state()
        square.scale(0.5).rotate(m.PI / 4).shift(4 * m.LEFT)
        square.set_color(m.YELLOW)
        self.add(square)
        self.play(m.Restore(square, run_time=2))
```

Transform a mobject back into the state it saved.

Save the state first with `save_state`; the animation transforms the mobject into it.

```python
m.Restore(mobject, **kwargs)
```

**`mobject`**

The mobject to restore.

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
