# Appear and disappear

**The film's code**

```python
import manimgx as m

class AppearHero(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        word = m.Text("Write", font_size=56)
        star = m.Star(color=m.YELLOW, fill_opacity=0.5)
        circle = m.Circle(color=m.GREEN, fill_opacity=0.5)
        shapes = m.VGroup(square, word, star, circle).arrange(buff=0.8)
        self.play(
            m.Create(square),
            m.Write(word),
            m.GrowFromCenter(star),
            m.FadeIn(circle, shift=m.UP),
        )
        self.play(
            m.Uncreate(square),
            m.Unwrite(word),
            m.ShrinkToCenter(star),
            m.FadeOut(circle, shift=m.DOWN),
        )
```

An animation that brings a mobject in adds it to the scene as it begins: you don't add it first. One that takes a mobject out removes it from the scene as it ends. Between them, a mobject is drawn along its paths, written as by hand, faded, or grown from a point.

## Draw and write

### Create

**Code**

```python
import manimgx as m

class CreateExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=4, color=m.BLUE, fill_opacity=0.5)
        self.play(m.Create(square, run_time=2))
```

Draw a mobject into view along its paths, one part after another.

The mobject joins the scene when the animation begins. Each part is revealed from its start to its end; with the default `lag_ratio` of 1, a part begins when the one before it is drawn.

```python
m.Create(mobject, **kwargs)
```

**`mobject`**

The mobject to draw.

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

### Uncreate

**Code**

```python
import manimgx as m

class UncreateExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex("a^2 + b^2 = c^2", font_size=120)
        box = m.SurroundingRectangle(formula, buff=0.4, color=m.YELLOW)
        self.add(formula, box)
        self.play(m.Uncreate(box, run_time=2))
```

Undraw a mobject along its paths, and take it out of the scene.

Each part is erased from its end back to its start, one part after another in the order `Create` draws them. The mobject leaves the scene when the animation finishes.

```python
m.Uncreate(mobject, **kwargs)
```

**`mobject`**

The mobject to undraw.

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

### DrawBorderThenFill

**Code**

```python
import manimgx as m

class DrawBorderThenFillExample(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            m.Square(side_length=3, color=m.ORANGE, fill_opacity=1),
            m.Star(outer_radius=2, color=m.BLUE, fill_opacity=1),
        ).arrange(buff=1.5)
        self.play(m.DrawBorderThenFill(shapes, stroke_color=m.YELLOW))
```

Draw a mobject's outline, then fill it in.

In the first half, each part's border is drawn along its path, `stroke_width` wide, in the paint the part is seen in: its own stroke, if it draws one, or else its fill (a gradient stays one), unless `stroke_color` is given. In the second, the fill comes in while the border turns into the part's own stroke; where the part draws no stroke, the border thins away in the same paint. The parts end as they were. The mobject joins the scene when the animation begins. It runs 2 seconds, eased by `double_smooth`: smoothly in each half.

```python
m.DrawBorderThenFill(vmobject, stroke_width=2, stroke_color=None, **kwargs)
```

**`vmobject`**

The mobject to draw.

**`stroke_width`**

The border's width, in hundredths of a scene unit.

**`stroke_color`**

The border's color; None for the paint each part is seen in.

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

### Write

**Code**

```python
import manimgx as m

class WriteExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex(r"e^{i\pi} + 1 = 0", font_size=144)
        self.play(m.Write(formula))
```

Write a mobject as if by hand: each part's outline drawn, then filled in.

The drawing of `DrawBorderThenFill`, at an even pace (`linear`), its parts staggered: `lag_ratio` is 4 divided by the number of parts, at most 0.2, and it runs 1 second for fewer than 15 parts, 2 seconds otherwise. The mobject joins the scene when the animation begins. `Unwrite` erases it.

```python
m.Write(vmobject, reverse=False, **kwargs)
```

**`vmobject`**

The mobject to write, as a text or a formula.

**`reverse`**

Whether to write the parts from the last to the first (they keep their order, so the later ones stay drawn over the earlier ones); the mobject then leaves the scene when the animation finishes (unless given `remover=False`).

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

### Unwrite

**Code**

```python
import manimgx as m

class UnwriteExample(m.Scene):
    def construct(self) -> None:
        alice = m.Text("Alice", font_size=96)
        rest = m.Text("and Bob", font_size=96)
        m.VGroup(alice, rest).arrange(buff=0.4)
        self.add(alice, rest)
        self.play(m.Unwrite(rest))
```

Erase a mobject as if writing it backward, and take it out of the scene.

The reverse of `Write`: each part's fill fades into its outline, and the outline is undrawn, one part shortly after another, by default the last part first. The parts keep their order while it plays, so the later ones stay drawn over the earlier ones. The mobject leaves the scene when the animation finishes.

```python
m.Unwrite(vmobject, reverse=True, **kwargs)
```

**`vmobject`**

The mobject to erase.

**`reverse`**

Whether to erase the parts from the last to the first; False erases from the first.

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

## Fade

### FadeIn

**Code**

```python
import manimgx as m

class FadeInExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(2 * m.UP + 4 * m.LEFT, radius=0.2, color=m.YELLOW)
        names = ("plain", "shift", "target", "scale")
        words = m.VGroup(*(m.Text(name, font_size=60) for name in names))
        words.arrange(buff=0.8)
        self.add(dot)
        self.play(
            m.LaggedStart(
                m.FadeIn(words[0]),
                m.FadeIn(words[1], shift=m.DOWN),
                m.FadeIn(words[2], target_position=dot),
                m.FadeIn(words[3], scale=1.5),
                lag_ratio=0.5,
            )
        )
```

Fade mobjects into view.

They start transparent (moved back by `shift`, or at `target_position`, and `scale` times their size) and arrive as they are. They join the scene when the animation begins.

```python
m.FadeIn(*mobjects, shift=None, target_position=None, scale=1, **kwargs)
```

**`*mobjects`**

The mobjects to fade in, together; at least one.

**`shift`**

The direction and distance they move while fading in: they start this far behind their places.

**`target_position`**

Where they start from, when no `shift` is given: a point, or a mobject's center.

**`scale`**

Their size at the start, relative to their own.

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

### FadeOut

**Code**

```python
import manimgx as m

class FadeOutExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(2 * m.UP + 4 * m.LEFT, radius=0.2, color=m.YELLOW)
        names = ("plain", "shift", "target", "scale")
        words = m.VGroup(*(m.Text(name, font_size=60) for name in names))
        words.arrange(buff=0.8)
        self.add(dot, words)
        self.play(
            m.LaggedStart(
                m.FadeOut(words[0]),
                m.FadeOut(words[1], shift=m.DOWN),
                m.FadeOut(words[2], target_position=dot),
                m.FadeOut(words[3], scale=0.5),
                lag_ratio=0.5,
            )
        )
```

Fade mobjects out of view, and take them out of the scene.

They end transparent (moved along `shift`, or to `target_position`, and `scale` times their size). They leave the scene when the animation finishes, and are then as they were before it: adding them again shows them.

```python
m.FadeOut(*mobjects, shift=None, target_position=None, scale=1, **kwargs)
```

**`*mobjects`**

The mobjects to fade out, together; at least one.

**`shift`**

The direction and distance they move while fading out.

**`target_position`**

Where they go, when no `shift` is given: a point, or a mobject's center.

**`scale`**

Their size at the end, relative to their own.

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

## Grow and shrink

### GrowFromCenter

**Code**

```python
import manimgx as m

class GrowFromCenterExample(m.Scene):
    def construct(self) -> None:
        left = m.Circle(radius=1.5, color=m.BLUE, fill_opacity=0.5)
        right = m.Circle(radius=1.5, color=m.GREEN, fill_opacity=0.5)
        m.VGroup(left, right).arrange(buff=2)
        self.play(
            m.GrowFromCenter(left), m.GrowFromCenter(right, point_color=m.RED)
        )
```

Grow a mobject from its center.

It starts shrunk to nothing at its center, in `point_color` if given. The mobject joins the scene when the animation begins.

```python
m.GrowFromCenter(mobject, point_color=None, **kwargs)
```

**`mobject`**

The mobject to grow.

**`point_color`**

The color it starts in; None for its own.

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

### GrowFromPoint

**Code**

```python
import manimgx as m

class GrowFromPointExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(3 * m.UP + 5 * m.LEFT, radius=0.2, color=m.YELLOW)
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        self.add(dot)
        self.play(m.GrowFromPoint(square, dot, point_color=m.YELLOW))
```

Grow a mobject from a point.

It starts shrunk to nothing at `point`, in `point_color` if given, and grows to its size and place. The mobject joins the scene when the animation begins.

```python
m.GrowFromPoint(mobject, point, point_color=None, **kwargs)
```

**`mobject`**

The mobject to grow.

**`point`**

The point it grows from, or a mobject whose center it grows from (taken when the animation is made).

**`point_color`**

The color it starts in; None for its own.

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

### GrowFromEdge

**Code**

```python
import manimgx as m

class GrowFromEdgeExample(m.Scene):
    def construct(self) -> None:
        squares = m.VGroup(
            *(m.Square(side_length=2.5, fill_opacity=0.5) for _ in range(3))
        ).arrange(buff=1.5)
        squares.set_color_by_gradient(m.BLUE, m.GREEN)
        self.play(
            m.GrowFromEdge(squares[0], m.DOWN),
            m.GrowFromEdge(squares[1], m.RIGHT),
            m.GrowFromEdge(squares[2], m.UR),
        )
```

Grow a mobject from an edge or a corner of its bounding box.

It starts shrunk to nothing there, in `point_color` if given. The mobject joins the scene when the animation begins.

```python
m.GrowFromEdge(mobject, edge, point_color=None, **kwargs)
```

**`mobject`**

The mobject to grow.

**`edge`**

The direction of the edge (as `DOWN`, its bottom) or the corner (as `UR`, its top right) it grows from.

**`point_color`**

The color it starts in; None for its own.

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

### GrowArrow

**Code**

```python
import manimgx as m

class GrowArrowExample(m.Scene):
    def construct(self) -> None:
        right = m.Arrow(3 * m.LEFT, 3 * m.RIGHT, color=m.BLUE).shift(1.5 * m.UP)
        up = m.Arrow(3 * m.LEFT, 3 * m.RIGHT + 1.5 * m.UP, color=m.YELLOW)
        up.shift(1.5 * m.DOWN)
        self.play(m.GrowArrow(right), m.GrowArrow(up, point_color=m.RED))
```

Grow an arrow from its start; its tip grows with it.

The arrow joins the scene when the animation begins.

```python
m.GrowArrow(arrow, point_color=None, **kwargs)
```

**`arrow`**

The arrow to grow.

**`point_color`**

The color it starts in; None for its own.

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

### SpinInFromNothing

**Code**

```python
import manimgx as m

class SpinInFromNothingExample(m.Scene):
    def construct(self) -> None:
        left = m.Square(side_length=2.5, color=m.BLUE, fill_opacity=0.5)
        right = m.Star(outer_radius=1.5, color=m.YELLOW, fill_opacity=0.5)
        m.VGroup(left, right).arrange(buff=3)
        self.play(
            m.SpinInFromNothing(left),
            m.SpinInFromNothing(right, angle=m.TAU, point_color=m.RED),
            run_time=2,
        )
```

Grow a mobject from its center while spinning it into place.

It turns through `angle` as it grows (counterclockwise, for a positive angle). The mobject joins the scene when the animation begins.

```python
m.SpinInFromNothing(mobject, angle=PI / 2, point_color=None, **kwargs)
```

**`mobject`**

The mobject to spin in.

**`angle`**

How far it turns on its way, in radians.

**`point_color`**

The color it starts in; None for its own.

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

### ShrinkToCenter

**Code**

```python
import manimgx as m

class ShrinkToCenterExample(m.Scene):
    def construct(self) -> None:
        circles = m.VGroup(
            *(
                m.Circle(radius=1.2, color=color, fill_opacity=0.5)
                for color in (m.BLUE, m.YELLOW, m.GREEN)
            )
        ).arrange(buff=1)
        self.add(circles)
        self.play(m.ShrinkToCenter(circles[1]))
```

Shrink a mobject to nothing at its center.

It stays in the scene, shrunk to a point: pass `remover=True` to take it out when the animation finishes.

```python
m.ShrinkToCenter(mobject, **kwargs)
```

**`mobject`**

The mobject to shrink.

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

### SpiralIn

**Code**

```python
import manimgx as m

class SpiralInExample(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            m.Circle(color=m.GREEN, fill_opacity=1),
            m.Square(color=m.BLUE, fill_opacity=1),
            m.Triangle(color=m.YELLOW, fill_opacity=1),
            m.Star(color=m.RED, fill_opacity=1),
        ).arrange(buff=1)
        self.play(m.SpiralIn(shapes, run_time=2))
```

Fly the submobjects of a mobject in from far away, spiralling into place.

Each comes home to where it is when the animation begins, from `scale_factor` + 1 times as far from the mobject's center: on the way it turns once around that center (and back once about its own, so it keeps its orientation), and it fades in over the first `fade_in_fraction` of the way. The mobject joins the scene when the animation begins; making the animation changes nothing.

```python
m.SpiralIn(shapes, scale_factor=8, fade_in_fraction=0.3, **kwargs)
```

**`shapes`**

The mobject whose submobjects spiral in.

**`scale_factor`**

How far out they start: `scale_factor` + 1 times as far from the center as their places.

**`fade_in_fraction`**

The fraction of the way over which they fade in, from 0 to 1.

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

## Part by part

### ShowIncreasingSubsets

**Code**

```python
import manimgx as m

class ShowIncreasingSubsetsExample(m.Scene):
    def construct(self) -> None:
        dots = m.VGroup(*(m.Dot(radius=0.4) for _ in range(8)))
        dots.arrange(buff=0.6).set_color_by_gradient(m.BLUE, m.YELLOW)
        self.play(m.ShowIncreasingSubsets(dots, rate_func=m.linear, run_time=2))
```

Show the submobjects of a group one more at a time.

At progress p, eased by the rate function, the first ⌊p·n⌋ of its n submobjects are shown and the rest are hidden: left out of the picture, not changed, so each part shows as it is, whatever else plays on it. The group joins the scene when the animation begins. A part still hidden when the animation ends stays unseen, left transparent; a remover's group leaves the scene as it is. Pass `rate_func=linear` for an even pace.

```python
m.ShowIncreasingSubsets(group, int_func=floor, **kwargs)
```

**`group`**

The group whose submobjects are shown.

**`int_func`**

How many are shown: a function of p·n (the default rounds down).

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

### ShowSubmobjectsOneByOne

**Code**

```python
import manimgx as m

class ShowSubmobjectsOneByOneExample(m.Scene):
    def construct(self) -> None:
        polygons = (
            m.VGroup(
                *(m.RegularPolygon(n, fill_opacity=1) for n in range(3, 9))
            )
            .set_color(m.YELLOW)
            .scale(2.5)
        )
        self.play(
            m.ShowSubmobjectsOneByOne(polygons, rate_func=m.linear, run_time=3)
        )
```

Show mobjects one at a time, each in place of the one before.

At progress p, eased by the rate function, only the ⌈p·n⌉-th of the n mobjects is shown, as it is, and the others are hidden; when the animation ends, those it hides stay unseen, left transparent. Pass `rate_func=linear` for an even pace.

```python
m.ShowSubmobjectsOneByOne(group, int_func=ceil, **kwargs)
```

**`group`**

The mobjects to show in turn.

**`int_func`**

Which one is shown: a function of p·n (the default rounds up).

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

## Type text

### AddTextLetterByLetter

**Code**

```python
import manimgx as m

class AddTextLetterByLetterExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Hello, world!", font_size=96)
        self.play(m.AddTextLetterByLetter(text, time_per_char=0.15))
```

Type a text in, one letter at a time.

The letters appear one after another at an even pace (`linear`), `time_per_char` seconds each unless a `run_time` is given. The text joins the scene when the animation begins.

```python
m.AddTextLetterByLetter(text, int_func=ceil, time_per_char=0.1, **kwargs)
```

**`text`**

The text to type, whose submobjects are its letters; a text without any raises a ValueError.

**`int_func`**

How many letters are shown: a function of the progress times the number of letters (the default rounds up, so the first shows at once).

**`time_per_char`**

How long each letter takes, in seconds.

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

### RemoveTextLetterByLetter

**Code**

```python
import manimgx as m

class RemoveTextLetterByLetterExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Hello, world!", font_size=96)
        self.add(text)
        self.play(m.RemoveTextLetterByLetter(text, time_per_char=0.15))
```

Remove a text one letter at a time, from the last, and take it out of the scene.

The reverse of `AddTextLetterByLetter`: the letters disappear from the last to the first, `time_per_char` seconds each unless a `run_time` is given. The text leaves the scene when the animation finishes, as it was before it: adding it again shows it.

```python
m.RemoveTextLetterByLetter(text, int_func=ceil, time_per_char=0.1, **kwargs)
```

**`text`**

The text to remove, whose submobjects are its letters; a text without any raises a ValueError.

**`int_func`**

How many letters are still shown: a function of what is left of the progress times the number of letters (the default rounds up).

**`time_per_char`**

How long each letter takes, in seconds.

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

### AddTextWordByWord

**Code**

```python
import manimgx as m

class AddTextWordByWordExample(m.Scene):
    def construct(self) -> None:
        words = m.VGroup(
            *(m.Text(word, font_size=120) for word in ("Word", "by", "word"))
        ).arrange(buff=0.5)
        self.play(m.AddTextWordByWord(words, time_per_char=0.12))
```

Type words in, letter by letter, pausing briefly after each word.

Each submobject of `text_mobject` is a word, and the words come in turn: a word's own submobjects, its letters, appear one after another, `time_per_char` seconds each; then the word holds for 0.005 × (its number of letters)^1.5 seconds. Give it a group of words, such as a `VGroup` of `Text`s: the submobjects of a single `Text` are its letters, which have no parts of their own to type, so each appears whole in its turn.

```python
m.AddTextWordByWord(text_mobject, time_per_char=0.06, **kwargs)
```

**`text_mobject`**

The words: a group whose submobjects are words made of letters.

**`time_per_char`**

How long each letter takes, in seconds.

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

### TypeWithCursor

**Code**

```python
import manimgx as m

class TypeWithCursorExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Typing...", font_size=96, color=m.PURPLE)
        cursor = m.Rectangle(m.GREY_A, height=1.1, width=0.4, fill_opacity=1)
        cursor.move_to(text[0])
        self.play(m.TypeWithCursor(text, cursor))
```

Type a text in letter by letter, with a cursor after the last letter typed.

The letters appear as with `AddTextLetterByLetter`, and the cursor, shown as it is, moves along after them. The cursor becomes part of the text, at its end, and stays there when the animation finishes unless `leave_cursor_on` is False. The text joins the scene when the animation begins.

```python
m.TypeWithCursor(text, cursor, buff=0.1, keep_cursor_y=True, leave_cursor_on=True, time_per_char=0.1, **kwargs)
```

**`text`**

The text to type, whose submobjects are its letters.

**`cursor`**

The cursor: any mobject, such as a thin rectangle.

**`buff`**

The gap between the last letter and the cursor, in scene units.

**`keep_cursor_y`**

Whether the cursor keeps its own height as it moves; if not, it moves at the text's middle height.

**`leave_cursor_on`**

Whether the cursor stays at the end of the text when the animation finishes.

**`time_per_char`**

How long each letter takes, in seconds.

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

### UntypeWithCursor

**Code**

```python
import manimgx as m

class UntypeWithCursorExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Deleting...", font_size=96, color=m.PURPLE)
        cursor = m.Rectangle(m.GREY_A, height=1.1, width=0.4, fill_opacity=1)
        cursor.move_to(text[0])
        self.add(text)
        self.play(m.UntypeWithCursor(text, cursor))
```

Delete a text letter by letter, with a cursor after the last letter left.

The reverse of `TypeWithCursor`: the letters disappear from the last to the first. The text leaves the scene when the animation finishes, as it was before it (adding it again shows it); the cursor becomes part of the text, and leaves with it.

```python
m.UntypeWithCursor(text, cursor, buff=0.1, keep_cursor_y=True, leave_cursor_on=True, time_per_char=0.1, **kwargs)
```

**`text`**

The text to delete, whose submobjects are its letters.

**`cursor`**

The cursor: any mobject, such as a thin rectangle.

**`buff`**

The gap between the last letter and the cursor, in scene units.

**`keep_cursor_y`**

Whether the cursor keeps its own height as it moves; if not, it moves at the text's middle height.

**`leave_cursor_on`**

Whether the cursor stays part of the text when the animation finishes.

**`time_per_char`**

How long each letter takes, in seconds.

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
