# Size and angle

**The film's code**

```python
import manimgx as m

class SizeAndAngleHero(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            *[
                m.Square(side_length=1.6, color=m.BLUE, fill_opacity=0.5)
                for _ in range(4)
            ]
        )
        shapes.arrange(buff=1.2)
        names = m.VGroup(
            m.Text("scale(1.4)", font="monospace", font_size=30),
            m.Text("rotate(PI / 4)", font="monospace", font_size=30),
            m.Text("stretch(1.6, 0)", font="monospace", font_size=30),
            m.Text("flip()", font="monospace", font_size=30),
        )
        for shape, name in zip(shapes, names, strict=True):
            name.next_to(shape, m.DOWN, buff=1.1)
        marker = m.Dot(color=m.YELLOW).move_to(shapes[3].get_corner(m.UR))
        shapes[3].add(marker)
        self.add(shapes, names)
        self.play(
            shapes[0].animate.scale(1.4),
            shapes[1].animate.rotate(m.PI / 4),
            shapes[2].animate.stretch(1.6, 0),
            shapes[3].animate.flip(),
            run_time=2,
        )
        self.wait()
```

A mobject's size is its bounding box's: its width and its height. Most shapes take their size when you make them (a circle its `radius`, a text its `font_size`); these methods change it later, about the mobject's center unless you give another point.

An angle is in radians: a whole turn is `m.TAU`, half a turn `m.PI`, and `30 * m.DEGREES` is 30 degrees. A positive angle turns counterclockwise.

## Size

### width

The mobject's width, in scene units: its bounding box's extent along x, from the leftmost of what it draws to the rightmost. Set it to scale the mobject to that width, in proportion, about its center.

```python
mobject.width
```

### height

The mobject's height, in scene units: its bounding box's extent along y, from the lowest of what it draws to the highest. Set it to scale the mobject to that height, in proportion, about its center.

```python
mobject.height
```

### scale

**Code**

```python
import manimgx as m

class MobjectScaleExample(m.Scene):
    def construct(self) -> None:
        a = m.Square(color=m.BLUE, fill_opacity=0.5)
        b, c = a.copy(), a.copy()
        m.VGroup(a, b, c).arrange(buff=2.5)
        for square, text in zip(
            (a, b, c), ("scale(2)", "about_edge=DL", "[0.5, 1.5, 1]")
        ):
            self.add(m.Text(text, font_size=32).next_to(square, m.DOWN, 2))
        self.add(a, b, c)
        self.play(
            a.animate.scale(2),
            b.animate.scale(2, about_edge=m.DL),
            c.animate.scale([0.5, 1.5, 1]),
        )
```

Scale the mobject and its whole family about a point: by one factor, or by one per axis.

Stroke widths stay as they are, unless `scale_stroke`.

```python
mobject.scale(scale_factor, scale_stroke=False, *, about_point=None, about_edge=None)
```

**`scale_factor`**

The factor: 2 doubles the mobject's size, 0.5 halves it, and a negative factor also reflects it through the point; or its factors along x, y and z.

**`scale_stroke`**

Whether stroke widths scale too, by the factor (for factors per axis, the geometric mean of the sizes of x's and y's).

**`about_point`**

The point that stays fixed; None: see `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction (DL for its bottom left corner); None for its center.

        import manimgx as m

        class MobjectScaleExample(m.Scene):
            def construct(self) -> None:
                a = m.Square(color=m.BLUE, fill_opacity=0.5)
                b, c = a.copy(), a.copy()
                m.VGroup(a, b, c).arrange(buff=2.5)
                for square, text in zip(
                    (a, b, c), ("scale(2)", "about_edge=DL", "[0.5, 1.5, 1]")
                ):
                    self.add(m.Text(text, font_size=32).next_to(square, m.DOWN, 2))
                self.add(a, b, c)
                self.play(
                    a.animate.scale(2),
                    b.animate.scale(2, about_edge=m.DL),
                    c.animate.scale([0.5, 1.5, 1]),
                )
        ```
    """
    if scale_stroke:
        length = length_factor(scale_factor)
        for mob in self.get_family():
            mob.paint = mob.paint.but(
                stroke_width=length * mob.get_stroke_width(),
                background_width=length * mob.get_stroke_width(background=True),
            )
    if isinstance(scale_factor, (int, float)):  # one factor: a scale about a point
        if about_point is None:
            edge = ORIGIN if about_edge is None else about_edge
            about_point = self.get_critical_point(edge)
        about = np.array(about_point, dtype=float)
        for mob in self.family_members_with_points():
            mob._geometry = mob._geometry.scaled(float(scale_factor), about)
        return self
    return self._apply_linear(
        np.diag(axis_factors(scale_factor)), about_point, about_edge
    )
````

### scale\_to\_fit\_width

Scale the mobject in proportion to a width.

```python
mobject.scale_to_fit_width(width, **kwargs)
```

**`width`**

The width, in scene units.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### scale\_to\_fit\_height

Scale the mobject in proportion to a height.

```python
mobject.scale_to_fit_height(height, **kwargs)
```

**`height`**

The height, in scene units.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### match\_width

Scale the mobject in proportion to another's width.

```python
mobject.match_width(mobject, **kwargs)
```

**`mobject`**

The mobject to match.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### match\_height

Scale the mobject in proportion to another's height.

```python
mobject.match_height(mobject, **kwargs)
```

**`mobject`**

The mobject to match.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### stretch

**Code**

```python
import manimgx as m

class MobjectStretchExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=1.5, color=m.BLUE, fill_opacity=0.5)
        self.add(circle)
        self.play(circle.animate.stretch(3, 0))
        self.play(circle.animate.stretch(0.5, 1, about_edge=m.DOWN))
```

Stretch the mobject and its whole family along one axis: scale that coordinate of every point, about a point, and keep the others.

Stroke widths stay as they are.

```python
mobject.stretch(factor, dim, *, about_point=None, about_edge=None)
```

**`factor`**

The factor: 2 makes the mobject twice as long along the axis.

**`dim`**

The axis: 0 for x (its width), 1 for y (its height), 2 for z.

**`about_point`**

The point that stays fixed; None: see `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction (DOWN for the middle of its bottom edge); None for its center.

        import manimgx as m

        class MobjectStretchExample(m.Scene):
            def construct(self) -> None:
                circle = m.Circle(radius=1.5, color=m.BLUE, fill_opacity=0.5)
                self.add(circle)
                self.play(circle.animate.stretch(3, 0))
                self.play(circle.animate.stretch(0.5, 1, about_edge=m.DOWN))
        ```
    """
    linear = np.eye(3)
    linear[dim, dim] = factor
    return self._apply_linear(linear, about_point, about_edge)
````

### stretch\_to\_fit\_width

Stretch the mobject horizontally to a width; its height stays.

```python
mobject.stretch_to_fit_width(width, **kwargs)
```

**`width`**

The width, in scene units.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### stretch\_to\_fit\_height

Stretch the mobject vertically to a height; its width stays.

```python
mobject.stretch_to_fit_height(height, **kwargs)
```

**`height`**

The height, in scene units.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

### replace

Put the mobject in another's place: scaled to its extent along one axis (or stretched to its width and height), and centered on it.

The other mobject stays where it is.

```python
mobject.replace(mobject, dim_to_match=0, stretch=False)
```

**`mobject`**

The mobject whose place it takes.

**`dim_to_match`**

The axis whose extent it takes, in proportion: 0 for x (the width), 1 for y (the height), 2 for z.

**`stretch`**

Whether to stretch it to the other's width and height instead.

## Angle

### m.PI

π: half a turn, in radians.

### m.TAU

τ = 2π: a whole turn, in radians.

### m.DEGREES

One degree, in radians: `30 * DEGREES` is a twelfth of a turn.

### rotate

**Code**

```python
import manimgx as m

class MobjectRotateExample(m.Scene):
    def construct(self) -> None:
        a = m.Square(side_length=2.5, color=m.BLUE, fill_opacity=0.5)
        b = m.Square(side_length=2.5, color=m.YELLOW, fill_opacity=0.5)
        m.VGroup(a, b).arrange(buff=4)
        pivot = m.Dot(b.get_corner(m.DL), radius=0.12, color=m.RED)
        self.add(a, b, pivot)
        self.play(
            a.animate.rotate(m.PI / 4),
            b.animate.rotate(m.PI / 2, about_edge=m.DL),
        )
```

Rotate the mobject and its whole family by an angle, about an axis through a point.

Its sheen direction turns with it. Through animate, the mobject turns rigidly through the whole angle.

```python
mobject.rotate(angle, axis=OUT, *, about_point=None, about_edge=None)
```

**`angle`**

The angle, in radians: counterclockwise as seen from where `axis` points (on the screen, for the default axis).

**`axis`**

The axis's direction (default OUT, out of the screen: a turn in the plane).

**`about_point`**

The point the axis goes through; None: see `about_edge`.

**`about_edge`**

The point of the mobject's bounding box the axis goes through, named by a direction (DL for its bottom left corner); None for its center.

        import manimgx as m

        class MobjectRotateExample(m.Scene):
            def construct(self) -> None:
                a = m.Square(side_length=2.5, color=m.BLUE, fill_opacity=0.5)
                b = m.Square(side_length=2.5, color=m.YELLOW, fill_opacity=0.5)
                m.VGroup(a, b).arrange(buff=4)
                pivot = m.Dot(b.get_corner(m.DL), radius=0.12, color=m.RED)
                self.add(a, b, pivot)
                self.play(
                    a.animate.rotate(m.PI / 4),
                    b.animate.rotate(m.PI / 2, about_edge=m.DL),
                )
        ```
    """
    rot = rotation_matrix(angle, axis)
    self._rotate_direction_state(rot)
    return self._apply_linear(rot, about_point, about_edge)
````

### flip

**Code**

```python
import manimgx as m

class MobjectFlipExample(m.Scene):
    def construct(self) -> None:
        word = m.Text("flip", font_size=160, color=m.YELLOW)
        self.add(word)
        self.play(word.animate.flip())
        self.play(word.animate.flip(m.RIGHT))
```

Flip the mobject and its whole family over: turn it half around an axis through a point, which mirrors it across that axis.

About the default UP axis, it is mirrored left to right; about RIGHT, upside down. Through animate, it turns over, through space.

```python
mobject.flip(axis=UP, *, about_point=None, about_edge=None)
```

**`axis`**

The axis's direction (default UP).

**`about_point`**

The point the axis goes through; None: see `about_edge`.

**`about_edge`**

The point of the mobject's bounding box the axis goes through, named by a direction; None for its center.

        import manimgx as m

        class MobjectFlipExample(m.Scene):
            def construct(self) -> None:
                word = m.Text("flip", font_size=160, color=m.YELLOW)
                self.add(word)
                self.play(word.animate.flip())
                self.play(word.animate.flip(m.RIGHT))
        ```
    """
    return self.rotate(
        TAU / 2, axis, about_point=about_point, about_edge=about_edge
    )
````

### rotation\_matrix

The matrix of a rotation about an axis through the origin.

Raises ValueError for a zero axis: a turn about no axis is no turn at all.

```python
m.rotation_matrix(angle, axis=_OUT)
```

**`angle`**

The angle, in radians, counterclockwise as seen from the tip of `axis`.

**`axis`**

The axis's direction (its length does not matter).

Returns The 3×3 rotation matrix.

## Any change

### put\_start\_and\_end\_on

Move, turn and scale the mobject so its first point is at `start` and its last at `end`; its shape stays, scaled in proportion.

A mobject whose first and last points coincide is only moved.

```python
mobject.put_start_and_end_on(start, end)
```

**`start`**

Where its first point goes.

**`end`**

Where its last point goes.

### apply\_matrix

**Code**

```python
import manimgx as m

class MobjectApplyMatrixExample(m.Scene):
    def construct(self) -> None:
        grid = m.NumberPlane()
        square = m.Square(color=m.YELLOW, fill_opacity=0.5).shift(m.UR)
        shear = [[1, 1], [0, 1]]
        self.add(grid, square)
        self.play(
            grid.animate.apply_matrix(shear),
            square.animate.apply_matrix(shear),
            run_time=2,
        )
```

Transform the mobject and its whole family by a matrix: each point, taken relative to a fixed point, is multiplied by it.

```python
mobject.apply_matrix(matrix, *, about_point=None, about_edge=None)
```

**`matrix`**

A 3 × 3 matrix, or a smaller one (2 × 2) that acts on the first coordinates and keeps the rest.

**`about_point`**

The point that stays fixed; with neither this nor `about_edge`, the origin.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction.

        import manimgx as m

        class MobjectApplyMatrixExample(m.Scene):
            def construct(self) -> None:
                grid = m.NumberPlane()
                square = m.Square(color=m.YELLOW, fill_opacity=0.5).shift(m.UR)
                shear = [[1, 1], [0, 1]]
                self.add(grid, square)
                self.play(
                    grid.animate.apply_matrix(shear),
                    square.animate.apply_matrix(shear),
                    run_time=2,
                )
        ```
    """
    if about_point is None and about_edge is None:
        about_point = ORIGIN
    full = np.identity(self.dim)
    m = np.array(matrix)
    full[: m.shape[0], : m.shape[1]] = m
    return self._apply_linear(full, about_point, about_edge)
````

### apply\_function

**Code**

```python
import numpy as np

import manimgx as m

def wave(p: np.ndarray) -> np.ndarray:
    return p + 0.5 * np.array([np.sin(p[1]), np.sin(p[0]), 0])

class MobjectApplyFunctionExample(m.Scene):
    def construct(self) -> None:
        grid = m.NumberPlane()
        grid.prepare_for_nonlinear_transform()
        self.add(grid)
        self.play(grid.animate.apply_function(wave), run_time=2)
```

Move the mobject's whole family through a function, about a point: each drawn member becomes its image under the function.

A path's curves are mapped to the curves of their image. Each curve is mapped to the curve through the images of its ends, along the images of its directions there; where one strays from the true image halfway along it by more than 0.001 scene units (a quarter of a pixel at 4K), every curve of the path is cut into 2, 4, 8, … equal pieces (at most 256 each), and the pieces are mapped instead. Any other kind maps its points. Through animate, each point of the path, cut the same way, moves straight to its image.

```python
mobject.apply_function(function, *, about_point=None, about_edge=None)
```

**`function`**

A function of a point, relative to the fixed point, that returns its new place.

**`about_point`**

The point the function is applied about; with neither this nor `about_edge`, the origin, so the function sees scene coordinates.

**`about_edge`**

The point of the mobject's bounding box it is applied about, named by a direction.

        import numpy as np

        import manimgx as m

        def wave(p: np.ndarray) -> np.ndarray:
            return p + 0.5 * np.array([np.sin(p[1]), np.sin(p[0]), 0])

        class MobjectApplyFunctionExample(m.Scene):
            def construct(self) -> None:
                grid = m.NumberPlane()
                grid.prepare_for_nonlinear_transform()
                self.add(grid)
                self.play(grid.animate.apply_function(wave), run_time=2)
        ```
    """
    # each leaf becomes its image its own way (`_map_points`): a mobject's points
    # map; a path's curves become the curves of their image (`VMobject._map_points`)
    if about_point is None:
        about_point = (
            ORIGIN if about_edge is None else self.get_critical_point(about_edge)
        )
    about = np.array(about_point, dtype=float)
    for mob in self.family_members_with_points():
        mob._map_points(function, about)
    return self
````

### apply\_complex\_function

**Code**

```python
import manimgx as m

class MobjectApplyComplexFunctionExample(m.Scene):
    def construct(self) -> None:
        grid = m.ComplexPlane(x_range=(-4, 4, 0.5), y_range=(-4, 4, 0.5))
        grid.prepare_for_nonlinear_transform()
        self.add(grid)
        self.play(
            grid.animate.apply_complex_function(lambda z: z**2 / 4),
            run_time=2,
        )
```

Move the mobject's whole family through a function of a complex number: the point (x, y, z) is x + iy, and goes where `function` sends it, keeping its z.

A path's curves are mapped as apply\_function maps them.

```python
mobject.apply_complex_function(function, **kwargs)
```

**`function`**

A function of a complex number, returning one.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

        import manimgx as m

        class MobjectApplyComplexFunctionExample(m.Scene):
            def construct(self) -> None:
                grid = m.ComplexPlane(x_range=(-4, 4, 0.5), y_range=(-4, 4, 0.5))
                grid.prepare_for_nonlinear_transform()
                self.add(grid)
                self.play(
                    grid.animate.apply_complex_function(lambda z: z**2 / 4),
                    run_time=2,
                )
        ```
    """

    def r3(point: Point3D) -> Point3D:
        z = function(complex(point[0], point[1]))
        return np.array([z.real, z.imag, point[2]])

    return self.apply_function(r3, **kwargs)
````

### set

Set attributes of the mobject by name: its properties, such as `width`, `height` or `color` (or a text's `font_size`), or any other attribute.

Through animate it animates the change: `mobject.animate.set(width=4)`.

```python
mobject.set(**kwargs)
```

The attributes' names, with their values.
