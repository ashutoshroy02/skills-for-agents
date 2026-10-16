# Planes

**The film's code**

```python
import manimgx as m

class PlanesHero(m.Scene):
    def construct(self) -> None:
        plane = m.ComplexPlane().add_coordinates()
        z = m.Dot(plane.n2p(2 + 1j), color=m.YELLOW)
        label = m.MathTex("2 + i", color=m.YELLOW).next_to(z, m.UR, buff=0.1)
        self.play(m.Create(plane, run_time=2))
        self.play(m.GrowFromCenter(z), m.Write(label))
        self.play(plane.animate.apply_complex_function(lambda w: w**2 / 4), run_time=3)
        self.wait()
```

A plane is axes with a grid: a line at every step of each axis. Unless you size it, a number plane fills the frame, with the frame's own coordinates, so that a point of the plane is the point of the frame: it is the grid to see positions by. A complex plane reads its points as complex numbers, and a polar plane draws circles around its center and rays out of it.

A plane bends with everything on it: insert more curves first (prepare\_for\_nonlinear\_transform), and its lines curve smoothly.

## NumberPlane

**Code**

```python
import manimgx as m

class NumberPlaneExample(m.Scene):
    def construct(self) -> None:
        plane = m.NumberPlane(
            x_range=[-6.5, 6.5, 1],
            y_range=[-4, 4, 1],
            faded_line_ratio=2,
            background_line_style={"stroke_color": m.TEAL},
        )
        arrow = m.Arrow(plane.c2p(0, 0), plane.c2p(3, 2), buff=0)
        self.add(plane.add_coordinates(), arrow.set_color(m.YELLOW))
```

A number plane: axes over a grid, a line at every step of each axis's range; filling the frame, with the scene's own coordinates, unless sized.

The grid's lines are blue (`BLUE_D`) and 2 wide; with a `faded_line_ratio` above 1, fainter lines divide each step further, half as wide and half as opaque unless styled. The lines are drawn behind the axes, which are white, 2 wide, without ticks or tips; their numbers, when written, are small (font size 24), below and to the right of their points. By default the ranges span the frame, one scene unit per unit, so the plane's coordinates are the scene's. Everything Axes do, the plane does: converting coordinates, plotting, labeling.

Background styles and the faded-line ratio are construction inputs; the plane retains its drawn grid rather than those setup attributes.

```python
m.NumberPlane(x_range=None, y_range=None, x_length=None, y_length=None, background_line_style=None, faded_line_style=None, faded_line_ratio=1, **kwargs)
```

**`x_range`**

The x-axis's range, `[x_min, x_max, x_step]`: a vertical line of the grid at every step. None for the frame's width when the plane is made, by 1.

**`y_range`**

The y-axis's range, `[y_min, y_max, y_step]`: a horizontal line of the grid at every step. None for the frame's height when the plane is made, by 1.

**`x_length`**

The x-axis's length, in scene units; None for one scene unit per unit.

**`y_length`**

The y-axis's length, in scene units; None for one scene unit per unit.

**`background_line_style`**

Style keywords for the grid's lines, over their defaults; None for none.

**`faded_line_style`**

Style keywords for the fainter lines; None for the grid lines' style, at half their width and opacity.

**`faded_line_ratio`**

How many parts the fainter lines divide each step of the grid into: 1 for no fainter lines, 2 for one between each two grid lines.

It also takes the `Axes` keywords.

### prepare\_for\_nonlinear\_transform

**Code**

```python
import numpy as np

import manimgx as m

class PlanePrepareForNonlinearTransformExample(m.Scene):
    def construct(self) -> None:
        plane = m.ComplexPlane(x_range=[-3, 3, 0.5], y_range=[-2, 2, 0.5])
        plane.prepare_for_nonlinear_transform()
        self.add(plane)
        self.play(plane.animate.apply_complex_function(np.sin), run_time=3)
```

Split the plane's lines into many curves, so that a nonlinear function bends them smoothly.

A function applied to the plane (with apply\_function or apply\_complex\_function) moves the points of its lines, and a straight line is a single curve: moving its few points would barely bend it. Each part of the plane with fewer curves than `num_inserted_curves` is divided into that many.

```python
number_plane.prepare_for_nonlinear_transform(num_inserted_curves=50)
```

**`num_inserted_curves`**

How many curves each line has at least.

        import numpy as np

        import manimgx as m

        class PlanePrepareForNonlinearTransformExample(m.Scene):
            def construct(self) -> None:
                plane = m.ComplexPlane(x_range=[-3, 3, 0.5], y_range=[-2, 2, 0.5])
                plane.prepare_for_nonlinear_transform()
                self.add(plane)
                self.play(plane.animate.apply_complex_function(np.sin), run_time=3)
        ```
    """
    for mob in self.family_members_with_points():
        if isinstance(mob, VMobject):
            num_curves = mob.get_num_curves()
            if num_inserted_curves > num_curves:
                mob.insert_n_curves(num_inserted_curves - num_curves)
    return self
````

## ComplexPlane

**Code**

```python
import manimgx as m

class ComplexPlaneExample(m.Scene):
    def construct(self) -> None:
        plane = m.ComplexPlane(x_range=[-6.5, 6.5, 1]).add_coordinates()
        self.add(plane)
        for z, name in ((2 + 1j, "2+i"), (-3 - 2j, "-3-2i")):
            dot = m.Dot(plane.n2p(z), radius=0.12, color=m.YELLOW)
            self.add(dot, m.MathTex(name).next_to(dot, m.UR, buff=0.1))
```

A complex plane: a NumberPlane whose points are complex numbers, x + yi at the point of coordinates (x, y).

number\_to\_point (`n2p`) and point\_to\_number (`p2n`) convert between numbers and points, and add\_coordinates writes the real numbers along the x-axis and the imaginary ones (with `i`) along the y-axis. A function of complex numbers maps the plane with apply\_complex\_function. It takes the arguments of a NumberPlane, and does everything it does.

```python
m.ComplexPlane(x_range=None, y_range=None, x_length=None, y_length=None, background_line_style=None, faded_line_style=None, faded_line_ratio=1, **kwargs)
```

It also takes the `Axes` keywords.

### number\_to\_point

Convert a complex number to its point on the plane: x + yi to the point of coordinates (x, y).

`n2p` is its short name.

```python
complex_plane.number_to_point(number)
```

**`number`**

The number; a real number is on the x-axis.

Returns The point, in scene coordinates.

### point\_to\_number

Convert a point to the complex number at it: x + yi, for the point's coordinates (x, y).

`p2n` is its short name.

```python
complex_plane.point_to_number(point)
```

**`point`**

The point, in scene coordinates.

### get\_coordinate\_labels

Make labels for numbers of the plane: a real number by its point on the x-axis, an imaginary one, with `i`, by its point on the y-axis.

A number is written as its larger part: its imaginary part, by the y-axis, if that is larger in size than its real part; its real part, by the x-axis, otherwise. Each is written as the axis numbers its ticks (see get\_number\_mobject).

```python
complex_plane.get_coordinate_labels(*numbers, **kwargs)
```

**`*numbers`**

The numbers to label; none for the ticks of both axes, but 0.

It also takes the `DecimalNumber` keywords.

Returns A new group of the labels, kept as the plane's `coordinate_labels`; not added to the plane.

### add\_coordinates

Label numbers of the plane, as get\_coordinate\_labels makes the labels, and add them to the plane.

```python
complex_plane.add_coordinates(*numbers, **kwargs)
```

**`*numbers`**

The numbers to label; none for the ticks of both axes, but 0.

It also takes the `DecimalNumber` keywords.

## PolarPlane

**Code**

```python
import manimgx as m

class PolarPlaneExample(m.Scene):
    def construct(self) -> None:
        planes = m.VGroup(
            m.PolarPlane(radius_max=2, size=5.5, radius_step=0.5),
            m.PolarPlane(
                radius_max=2,
                size=5.5,
                azimuth_units="degrees",
                azimuth_step=12,
                faded_line_ratio=2,
            ),
        )
        for plane in planes:
            plane.add_coordinates()
        self.add(planes.arrange(buff=1.5))
```

A polar plane: circles around its origin, one at every step of the radius, and lines out from it, a fraction of a turn apart; blue over white axes without ticks or tips, unless styled.

The plane is a disc of radius `radius_max`, centered on the scene's origin, its x- and y-axes its radii. add\_coordinates numbers the radii and labels the lines' angles, in `azimuth_units`: fractions of π (3π/4), of τ, degrees, gradians, or fractions of a turn. polar\_to\_point (`pr2pt`) converts polar coordinates to points, and plot\_polar\_graph plots curves r = f(θ); everything Axes do, the plane does.

Background styles and the faded-line ratio are construction inputs; the plane retains its drawn grid rather than those setup attributes.

```python
m.PolarPlane(radius_max=None, size=None, radius_step=1, azimuth_step=None, azimuth_units='PI radians', azimuth_compact_fraction=True, azimuth_offset=0, azimuth_direction='CCW', azimuth_label_buff=SMALL_BUFF, azimuth_label_font_size=24, radius_config=None, background_line_style=None, faded_line_style=None, faded_line_ratio=1, **kwargs)
```

**`radius_max`**

The radius of the outer circle, in the plane's units; None for half the frame's short side when the plane is made (4).

**`size`**

The plane's width, its diameter, in scene units; None for one scene unit per unit.

**`radius_step`**

The distance between two circles, in the plane's units.

**`azimuth_step`**

How many lines divide the full turn: a line every turn divided by it; None for the units' own: 20 for radians, 36 for degrees, 40 for gradians, 1 for fractions of a turn.

**`azimuth_units`**

How the angles are labeled: `"PI radians"` (fractions of π), `"TAU radians"` (fractions of τ), `"degrees"`, `"gradians"`, or None (fractions of a turn, as decimals).

**`azimuth_compact_fraction`**

Whether a fraction of π or τ is written with the constant in its numerator (3π/4), rather than after it (¾ π).

**`azimuth_offset`**

The angle of the line labeled 0, in radians, counterclockwise from the right: the lines and their labels turn with it.

**`azimuth_direction`**

The direction the angles increase in: `"CCW"`, counterclockwise, or `"CW"`, clockwise.

**`azimuth_label_buff`**

The gap between the outer circle and the angles' labels, in scene units.

**`azimuth_label_font_size`**

The font size of the angles' labels.

**`radius_config`**

Number line keywords for the radii's axes, over the plane's own (no ticks, no tips, 2 wide, font size 24, numbers below and to the left); None for none.

**`background_line_style`**

Style keywords for the circles and lines, over their defaults: blue (`BLUE_D`), 2 wide, opaque; None for none.

**`faded_line_style`**

Style keywords for the fainter circles and lines; None for the others' style, at half their width and opacity.

**`faded_line_ratio`**

How many parts fainter circles and lines divide each step into: 1 for none.

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

### get\_coordinate\_labels

Number the plane's radii, and make labels for its angles.

The radii are numbered along the x-axis, right of the center; the numbers are added to the axis. The angles' labels, in the plane's `azimuth_units`, go around the outer circle, `azimuth_label_buff` beyond it: placed for a plane centered on the scene's origin, as it is made.

```python
polar_plane.get_coordinate_labels(r_values=None, a_values=None)
```

**`r_values`**

The radii to number, in the plane's units; None for every circle's but 0.

**`a_values`**

The angles to label, as fractions of a turn (0.25 is a quarter turn); None for every line's.

Returns A new group of the x-axis, now numbered, and a group of the angles' labels (not added to the plane); kept as the plane's `coordinate_labels`.

### add\_coordinates

Number the plane's radii along its x-axis, and label its angles around it, as get\_coordinate\_labels makes them.

```python
polar_plane.add_coordinates(r_values=None, a_values=None)
```

**`r_values`**

The radii to number, in the plane's units; None for every circle's but 0.

**`a_values`**

The angles to label, as fractions of a turn (0.25 is a quarter turn); None for every line's.

### get\_radian\_label

Make the label of an angle in radians: a fraction of π, or of τ if the plane's units are `"TAU radians"`.

The fraction is the nearest with a denominator up to 100, written as the plane's `azimuth_compact_fraction` says: 3π/4, or ¾ π.

```python
polar_plane.get_radian_label(number, **kwargs)
```

**`number`**

The angle, as a fraction of a turn (0.375 for 3π/4).

It also takes the `MathTex` keywords and the style keywords.

Returns A new MathTex.

## Complex numbers and points

A point `[x, y, 0]` stands for the complex number x + yi.

### complex\_to\_R3

The point of a complex number: its real part as x, its imaginary part as y.

```python
m.complex_to_R3(complex_num)
```

**`complex_num`**

The number.

Returns The point, with a z of 0.

### R3\_to\_complex

The complex number of a point: x + iy (its z is ignored).

```python
m.R3_to_complex(point)
```

### complex\_func\_to\_R3\_func

A function of complex numbers as a function of points: a point (x, y, z) goes where the function sends x + iy, with a z of 0.

```python
m.complex_func_to_R3_func(complex_func)
```

**`complex_func`**

The function of complex numbers.

Returns The function of points.
