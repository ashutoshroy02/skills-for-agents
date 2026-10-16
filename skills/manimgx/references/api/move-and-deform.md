# Move and deform

**The film's code**

```python
import manimgx as m
import numpy as np

class MoveAndDeformHero(m.Scene):
    def construct(self) -> None:
        grid = m.NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1]
        ).prepare_for_nonlinear_transform()
        self.add(grid)
        self.play(m.ApplyMatrix([[1, 1], [0, 1]], grid), run_time=2)
        self.play(
            m.ApplyFunction(
                lambda mob: mob.apply_function(
                    lambda p: p + 0.3 * np.array([np.sin(p[1]), np.sin(p[0]), 0])
                ),
                grid,
            ),
            run_time=2,
        )
        self.wait()
```

Some changes are not a method call: a turn about a point that the mobject keeps turning around, a trip along a path, a deformation of every point. These animations make them.

## Turn and follow

### Rotate

**Code**

```python
import manimgx as m

class RotateExample(m.Scene):
    def construct(self) -> None:
        pivot = m.Dot(radius=0.1)
        left = m.Rectangle(m.BLUE, width=2.5, height=1.2, fill_opacity=0.5)
        right = left.copy().set_color(m.YELLOW)
        left.shift(4 * m.LEFT)
        right.shift(2 * m.RIGHT)
        self.add(pivot, left, right)
        self.play(
            m.Rotate(left, m.PI / 2),
            m.Rotate(right, m.PI / 2, about_point=pivot.get_center()),
            run_time=2,
        )
```

Rotate a mobject rigidly about a point.

It turns by `angle` about `axis` around one pivot: `about_point`, or the point of its bounding box at `about_edge`, or its center, taken from the mobject as it is when the rotation begins. Every point travels along a circle about the pivot, so the mobject keeps its shape on the way, and an angle of `TAU` is a full turn.

```python
m.Rotate(mobject, angle=PI, axis=OUT, about_point=None, about_edge=None, **kwargs)
```

**`mobject`**

The mobject to rotate.

**`angle`**

The angle, in radians, counterclockwise about `axis`.

**`axis`**

The axis it turns about; the default, `OUT`, turns it in the plane of the screen.

**`about_point`**

The pivot; None to take it from `about_edge`, or the center.

**`about_edge`**

The direction of the point of its bounding box it turns about, when no `about_point` is given.

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

### Rotating

**Code**

```python
import manimgx as m

class RotatingExample(m.Scene):
    def construct(self) -> None:
        hand = m.Arrow(m.ORIGIN, 2.5 * m.UP, buff=0, color=m.YELLOW)
        self.add(m.Circle(radius=3, color=m.GREY), hand)
        self.play(m.Rotating(hand, -m.TAU, about_point=m.ORIGIN, run_time=4))
```

Rotate a mobject at a steady pace: by default, a full turn in 5 seconds.

A `Rotate` whose angle is `TAU` unless given another, at an even pace (`linear`), over 5 seconds.

```python
m.Rotating(mobject, angle=TAU, axis=OUT, about_point=None, about_edge=None, **kwargs)
```

**`mobject`**

The mobject to rotate.

**`angle`**

The angle, in radians, counterclockwise about `axis`.

**`axis`**

The axis it turns about; the default, `OUT`, turns it in the plane of the screen.

**`about_point`**

The pivot; None to take it from `about_edge`, or the center.

**`about_edge`**

The direction of the point of its bounding box it turns about, when no `about_point` is given.

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

### MoveAlongPath

**Code**

```python
import numpy as np

import manimgx as m

class MoveAlongPathExample(m.Scene):
    def construct(self) -> None:
        path = m.FunctionGraph(lambda x: 2 * np.sin(x), x_range=(-6, 6))
        dot = m.Dot(radius=0.2, color=m.ORANGE)
        self.add(path.set_color(m.GREY), dot)
        self.play(m.MoveAlongPath(dot, path, run_time=3))
```

Move a mobject along a path.

Its center travels along `path` from the path's start to its end, at an even speed along its length (as eased by the rate function), and the mobject keeps its shape. It starts at the path's start, wherever it was. Its own updaters act on it directly while it moves (`suspend_mobject_updating` is False).

```python
m.MoveAlongPath(mobject, path, **kwargs)
```

**`mobject`**

The mobject to move.

**`path`**

The curve it travels along.

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

## Through a function

Each point of the mobject goes where a function sends it. Curved images need more points: insert curves first (see insert\_n\_curves).

### ApplyFunction

**Code**

```python
import manimgx as m

class ApplyFunctionExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        self.add(square)

        def to_red_circle(mob: m.Mobject) -> m.Mobject:
            circle = m.Circle(radius=2, color=m.RED, fill_opacity=0.5)
            return circle.move_to(mob)

        self.play(m.ApplyFunction(to_red_circle, square))
```

Transform a mobject into what a function makes of it.

The function gets a copy of the mobject when the animation begins, and returns the state to transform into: the copy, changed, or a new mobject (anything else raises a TypeError).

```python
m.ApplyFunction(function, mobject, **kwargs)
```

**`function`**

A function from a copy of the mobject to its end state.

**`mobject`**

The mobject to transform.

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

### ApplyPointwiseFunction

**Code**

```python
import numpy as np

import manimgx as m

class ApplyPointwiseFunctionExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
        self.add(square)
        self.play(
            m.ApplyPointwiseFunction(
                lambda p: m.complex_to_R3(np.exp(m.R3_to_complex(p))), square
            )
        )
```

Transform a mobject into its image under a function of a point.

Each point p travels in a straight line to `function(p)`, and a path's curves are mapped as apply\_function maps them, cut into more curves where the function bends them. It runs 3 seconds.

```python
m.ApplyPointwiseFunction(function, mobject, **kwargs)
```

**`function`**

A function from a point to where it goes, in scene coordinates.

**`mobject`**

The mobject to move.

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

### ApplyMatrix

**Code**

```python
import manimgx as m

class ApplyMatrixExample(m.Scene):
    def construct(self) -> None:
        matrix = [[1, 1], [0, 2 / 3]]
        plane = m.NumberPlane()
        text = m.Text("Hello World!", font_size=72)
        self.add(plane, text)
        self.play(m.ApplyMatrix(matrix, plane), m.ApplyMatrix(matrix, text))
```

Transform a mobject by a matrix: each point p goes to M·p.

A 2 × 2 matrix acts on x and y, keeping z; a 3 × 3 one on all three (any other shape raises a ValueError). The points travel in straight lines. It runs 3 seconds.

```python
m.ApplyMatrix(matrix, mobject, about_point=ORIGIN, **kwargs)
```

**`matrix`**

The matrix, 2 × 2 or 3 × 3, as nested lists or an array.

**`mobject`**

The mobject to transform.

**`about_point`**

The point that stays where it is.

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

### ApplyComplexFunction

**Code**

```python
import manimgx as m

class ApplyComplexFunctionExample(m.Scene):
    def construct(self) -> None:
        plane = m.NumberPlane(x_range=(-3, 3, 0.5), y_range=(-3, 3, 0.5))
        plane.prepare_for_nonlinear_transform()
        self.add(plane)
        self.play(m.ApplyComplexFunction(lambda z: z**2 / 4, plane), run_time=2)
```

Transform a mobject into its image under a function of a complex number.

Each point (x, y, z) is taken as x + iy and travels in a straight line to its image under the function, keeping z, and a path's curves are mapped as apply\_function maps them.

```python
m.ApplyComplexFunction(function, mobject, **kwargs)
```

**`function`**

A function from a complex number to a complex number.

**`mobject`**

The mobject to move.

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

## Deform over time

### Homotopy

**Code**

```python
import numpy as np

import manimgx as m

class HomotopyExample(m.Scene):
    def construct(self) -> None:
        line = m.FunctionGraph(lambda x: 0, x_range=(-6, 6), color=m.BLUE)

        def wave(x: float, y: float, z: float, t: float) -> tuple[float, ...]:
            return (x, y + 1.5 * t * np.sin(2 * x - 6 * t), z)

        self.add(line)
        self.play(m.Homotopy(wave, line))
```

Deform a mobject by a homotopy: a function of each point and the progress.

At progress t, from 0 to 1 (eased by the rate function), the mobject is the image of the mobject as it began: each point (x, y, z) goes to `homotopy(x, y, z, t)`, and a path's curves are mapped as apply\_function maps them. It runs 3 seconds.

```python
m.Homotopy(homotopy, mobject, apply_function_kwargs=None, **kwargs)
```

**`homotopy`**

A function of x, y, z and t, returning where the point is at t.

**`mobject`**

The mobject to deform.

**`apply_function_kwargs`**

Where the coordinates are measured from: `{"about_point": ...}` or `{"about_edge": ...}`; None for the origin.

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

### ComplexHomotopy

**Code**

```python
import numpy as np

import manimgx as m

class ComplexHomotopyExample(m.Scene):
    def construct(self) -> None:
        plane = m.NumberPlane(x_range=(-3, 3), y_range=(-3, 3))
        plane.prepare_for_nonlinear_transform()
        self.add(plane)
        self.play(
            m.ComplexHomotopy(lambda z, t: z * np.exp(0.5j * t * abs(z)), plane)
        )
```

Deform a mobject by a complex homotopy: a function of x + iy and the progress.

At progress t, from 0 to 1 (eased by the rate function), the mobject is the image of the mobject as it began: each point (x, y, z) goes to `complex_homotopy(x + iy, t)`, keeping z, and a path's curves are mapped as apply\_function maps them. It runs 3 seconds.

```python
m.ComplexHomotopy(complex_homotopy, mobject, **kwargs)
```

**`complex_homotopy`**

A function of z and t, returning where the point is at t, as a complex number.

**`mobject`**

The mobject to deform.

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

### ApplyWave

**Code**

```python
import manimgx as m

class ApplyWaveExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("WaveWaveWave", font_size=120)
        self.add(text)
        self.play(m.ApplyWave(text))
        self.play(m.ApplyWave(text, ripples=3, amplitude=0.4))
```

Send a wave through a mobject, from left to right.

Its points are displaced along `direction`, by up to `amplitude`, as the wave passes them, and are back in place once it has passed. It runs 2 seconds.

```python
m.ApplyWave(mobject, direction=UP, amplitude=0.2, wave_func=smooth, time_width=1, ripples=1, **kwargs)
```

**`mobject`**

The mobject to wave.

**`direction`**

The direction the points are displaced in.

**`amplitude`**

How far they are displaced at most, in scene units.

**`wave_func`**

The shape of each ripple's rise: a rate function.

**`time_width`**

The wave's width, as a fraction of the mobject's width.

**`ripples`**

How many ripples the wave has.

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

### PhaseFlow

**Code**

```python
import numpy as np

import manimgx as m

class PhaseFlowExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=0.5)
        square.shift(3 * m.RIGHT)
        self.add(m.Dot(), square)

        def spiral(p: np.ndarray) -> np.ndarray:
            return np.array([-p[1] - 0.3 * p[0], p[0] - 0.3 * p[1], 0.0])

        self.play(m.PhaseFlow(spiral, square, virtual_time=m.PI, run_time=3))
```

Carry a mobject's points along a vector field.

Each point moves with the velocity `function` gives it where it is, for `virtual_time` units of the field's time over the animation, from where it is when the animation begins. The flow is integrated in steps of the field's time, `config.simulation_rate` a second of the animation, by the classical Runge–Kutta method, so it is the same at every frame rate; a frame between steps shows the flow carried on from the step before it. A path's curves are mapped as apply\_function maps them. It runs at an even pace (`linear`), and the mobject's own updaters act on it directly (`suspend_mobject_updating` is False).

```python
m.PhaseFlow(function, mobject, virtual_time=1, **kwargs)
```

**`function`**

The vector field: a function from a point to its velocity.

**`mobject`**

The mobject to carry.

**`virtual_time`**

How long the points flow, in the field's units of time.

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
