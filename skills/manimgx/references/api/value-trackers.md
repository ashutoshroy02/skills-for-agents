# Value trackers

**The film's code**

```python
import manimgx as m

def curve(x: float) -> float:
    return x**2 / 4

class ValueTrackersHero(m.Scene):
    def construct(self) -> None:
        axes = m.Axes(x_range=[0, 5, 1], y_range=[0, 7, 1], x_length=8, y_length=5)
        graph = axes.plot(curve, color=m.BLUE)
        x = m.ValueTracker(1)
        dot = m.always_redraw(
            lambda: m.Dot(axes.c2p(x.get_value(), curve(x.get_value())), color=m.YELLOW)
        )
        number = m.always_redraw(
            lambda: m.DecimalNumber(x.get_value()).next_to(dot, m.UL)
        )
        self.add(axes, graph, dot, number)
        self.play(x.animate.set_value(4.5), run_time=3)
        self.wait()
```

A value tracker holds a number and shows nothing. Animate its number with `tracker.animate.set_value(10)`; read it with `tracker.get_value()` in an updater, or in a function that always\_redraw calls. One animation of a tracker then moves every mobject that reads it.

## ValueTracker

**Code**

```python
import manimgx as m

class ValueTrackerExample(m.Scene):
    def construct(self) -> None:
        x = m.ValueTracker(-4)
        line = m.NumberLine(x_range=(-6, 6, 1), length=12).add_numbers()
        pointer = m.Vector(1.5 * m.DOWN, color=m.YELLOW)
        pointer.add_updater(lambda p: p.next_to(line.n2p(x.get_value()), m.UP))
        label = m.MathTex("x", font_size=72, color=m.YELLOW)
        label.add_updater(lambda t: t.next_to(pointer, m.UP))
        self.add(line, pointer, label)
        self.play(x.animate.set_value(5), run_time=2)
        x -= 3
        self.wait(0.5)
        self.play(x.animate.increment_value(-5))
```

A number that animations can change and updaters can read.

The number is kept as the x coordinate of the tracker's one point, so whatever moves a mobject changes it: `tracker.animate.set_value(5)` takes it to 5 at the pace of the animation's rate function, and the updaters of other mobjects read it with `get_value`. A tracker is never drawn; add it to the scene only if it has updaters of its own. `tracker += 1` and `tracker -= 1` change the number at once.

```python
m.ValueTracker(value=0, **kwargs)
```

**`value`**

The real number it starts with; use ComplexValueTracker for complex numbers.

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

### get\_value

The number the tracker holds.

```python
tracker.get_value()
```

### set\_value

Set the number the tracker holds; through `animate`, animate it there.

```python
tracker.set_value(value)
```

**`value`**

The new number.

### increment\_value

Add to the number the tracker holds; through `animate`, animate the change.

```python
tracker.increment_value(d_value)
```

**`d_value`**

The amount to add; a negative one subtracts.

## ComplexValueTracker

**Code**

```python
import manimgx as m

class ComplexValueTrackerExample(m.Scene):
    def construct(self) -> None:
        plane = m.ComplexPlane().add_coordinates()
        z = m.ComplexValueTracker(2 + 1j)
        dot = m.Dot(radius=0.15, color=m.YELLOW)
        dot.add_updater(lambda d: d.move_to(plane.n2p(z.get_value())))
        self.add(plane, dot)
        self.play(z.animate.set_value(-3 + 2j))
        self.play(z.animate.set_value(z.get_value() * 1j))
        self.play(z.animate.set_value(z.get_value() / (1 + 1j)))
```

A complex number that animations can change and updaters can read.

The number is kept as the tracker's one point, its real part as x and its imaginary part as y, so an animation takes it along a straight line of the complex plane: `tracker.animate.set_value(3 + 2j)`. `+=` and `-=` change it at once, in complex arithmetic.

```python
m.ComplexValueTracker(value=0, **kwargs)
```

**`value`**

The number it starts with.

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

### get\_value

The complex number the tracker holds.

```python
tracker.get_value()
```

### set\_value

Set the complex number the tracker holds; through `animate`, animate it there, in a straight line.

```python
tracker.set_value(value)
```

**`value`**

The new number; a real one is taken as complex.
