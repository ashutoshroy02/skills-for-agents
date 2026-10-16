# Paths

**The film's code**

```python
import manimgx as m

class PathsHero(m.Scene):
    def construct(self) -> None:
        path = m.VMobject(color=m.YELLOW, stroke_width=6)
        path.start_new_path([-5, -1, 0])
        path.add_line_to([-3, 2, 0])
        path.add_smooth_curve_to([0, 0, 0])
        path.add_cubic_bezier_curve_to([1, 3, 0], [3, -3, 0], [5, 1, 0])
        anchors = m.VGroup(
            *[m.Dot(point, color=m.BLUE) for point in path.get_anchors()]
        )
        dot = m.Dot(color=m.RED).move_to(path.get_start())
        self.play(m.Create(path), run_time=2)
        self.play(m.FadeIn(anchors))
        self.play(m.MoveAlongPath(dot, path), run_time=2)
        self.wait()
```

A shape is a path: curves, each from one point to the next. A curve starts at an anchor, bends toward two handles, and ends at the next anchor. The stroke follows the curves, and the fill closes each part of the path back to its start. Circles, polygons, text and graphs are all paths, so all of this works on them too.

To draw a path of your own, make an empty `m.VMobject()`, then give it its points: as corners, as a smooth curve through them, or one line and curve at a time.

## VMobject

**Code**

```python
import manimgx as m

class VMobjectExample(m.Scene):
    def construct(self) -> None:
        path = m.VMobject(color=m.BLUE, fill_opacity=0.5, stroke_width=8)
        path.set_points_as_corners([[-3, -2, 0], [-3, 2, 0], [0, 2, 0]])
        path.add_cubic_bezier_curve_to([3, 2, 0], [3, -2, 0], [0, -2, 0])
        path.close_path()
        self.play(m.Create(path, run_time=2))
```

A path: cubic Bézier curves, stroked in white and unfilled unless styled.

Each curve has four control points: it starts at an anchor, bends toward two handles and ends at the next anchor. The path's points are its curves' control points, four by four, and a new subpath starts wherever a curve does not begin where the one before it ends. The stroke follows the curves; the fill closes each subpath with a straight line back to its start, and where subpaths overlap, a point is filled unless their windings around it cancel: a subpath inside another that runs the other way cuts a hole.

Circles, polygons, text and graphs are all paths. A plain `VMobject` has no points until it is given a shape: set its points as corners, or start it at a point and add lines and curves.

```python
m.VMobject(**kwargs)
```

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

## Draw a path

### set\_points\_as\_corners

**Code**

```python
import manimgx as m

class VMobjectSetPointsAsCornersExample(m.Scene):
    def construct(self) -> None:
        zigzag = m.VMobject(color=m.YELLOW, stroke_width=8)
        zigzag.set_points_as_corners(
            [[-3, -1.5, 0], [-1.5, 1.5, 0], [0, -1.5, 0], [1.5, 1.5, 0]]
        )
        triangle = m.VMobject(color=m.BLUE, fill_opacity=0.5)
        triangle.set_points_as_corners(
            [[-2, -1.5, 0], [0, 2, 0], [2, -1.5, 0], [-2, -1.5, 0]]
        )
        self.add(m.VGroup(zigzag, triangle).arrange(buff=2))
```

Give the path new points, in place of its own: straight lines through the given points in turn.

The path is open: to close it, end with its first point again.

```python
path.set_points_as_corners(points)
```

**`points`**

The corners, in scene coordinates, in order.

        import manimgx as m

        class VMobjectSetPointsAsCornersExample(m.Scene):
            def construct(self) -> None:
                zigzag = m.VMobject(color=m.YELLOW, stroke_width=8)
                zigzag.set_points_as_corners(
                    [[-3, -1.5, 0], [-1.5, 1.5, 0], [0, -1.5, 0], [1.5, 1.5, 0]]
                )
                triangle = m.VMobject(color=m.BLUE, fill_opacity=0.5)
                triangle.set_points_as_corners(
                    [[-2, -1.5, 0], [0, 2, 0], [2, -1.5, 0], [-2, -1.5, 0]]
                )
                self.add(m.VGroup(zigzag, triangle).arrange(buff=2))
        ```
    """
    pts = np.asarray(points, dtype=float)
    if len(pts) == 2:  # a segment: the one segment, placed
        self._geometry = segment(pts[0], pts[1])
        return self
    return self.set_anchors_and_handles(
        *(interpolate(pts[:-1], pts[1:], t) for t in _T_VALUES)
    )
````

### set\_points\_smoothly

**Code**

```python
import manimgx as m

class VMobjectSetPointsSmoothlyExample(m.Scene):
    def construct(self) -> None:
        points = [[-5, -1, 0], [-3, 2, 0], [-1, -2, 0], [1, 2, 0]]
        points += [[3, -1, 0], [5, 1, 0]]
        corners = m.VMobject(color=m.GREY).set_points_as_corners(points)
        curve = m.VMobject(color=m.YELLOW, stroke_width=8)
        curve.set_points_smoothly(points)
        self.add(corners, *(m.Dot(p, radius=0.12) for p in points))
        self.play(m.Create(curve, run_time=2))
```

Give the path new points, in place of its own: a smooth curve through the given points in turn.

The curve passes through each point, bending smoothly there, with no change of curvature (a cubic spline); if the last point is the first, it closes smoothly.

```python
path.set_points_smoothly(points)
```

**`points`**

The points it passes through, in scene coordinates, in order.

        import manimgx as m

        class VMobjectSetPointsSmoothlyExample(m.Scene):
            def construct(self) -> None:
                points = [[-5, -1, 0], [-3, 2, 0], [-1, -2, 0], [1, 2, 0]]
                points += [[3, -1, 0], [5, 1, 0]]
                corners = m.VMobject(color=m.GREY).set_points_as_corners(points)
                curve = m.VMobject(color=m.YELLOW, stroke_width=8)
                curve.set_points_smoothly(points)
                self.add(corners, *(m.Dot(p, radius=0.12) for p in points))
                self.play(m.Create(curve, run_time=2))
        ```
    """
    self.set_points_as_corners(points)
    return self.make_smooth()
````

### start\_new\_path

Start a new subpath at a point: the next curve added begins there, not where the path ends.

A curve left unfinished (a subpath started and given no curve yet) is completed with copies of its first point, as a curve of no length. Started where the path ends, the subpath just goes on.

```python
path.start_new_path(point)
```

**`point`**

Where the new subpath starts, in scene coordinates.

### add\_line\_to

**Code**

```python
import manimgx as m

class VMobjectAddLineToExample(m.Scene):
    def construct(self) -> None:
        stairs = m.VMobject(color=m.BLUE, stroke_width=8)
        stairs.start_new_path([-5, -3, 0])
        for _ in range(5):
            stairs.add_line_to(stairs.get_end() + 1.2 * m.UP)
            stairs.add_line_to(stairs.get_end() + 2 * m.RIGHT)
        self.play(m.Create(stairs, run_time=3))
```

Add a straight line from where the path ends to a point.

The path must have a point to start from.

```python
path.add_line_to(point)
```

**`point`**

Where the line ends, in scene coordinates.

        import manimgx as m

        class VMobjectAddLineToExample(m.Scene):
            def construct(self) -> None:
                stairs = m.VMobject(color=m.BLUE, stroke_width=8)
                stairs.start_new_path([-5, -3, 0])
                for _ in range(5):
                    stairs.add_line_to(stairs.get_end() + 1.2 * m.UP)
                    stairs.add_line_to(stairs.get_end() + 2 * m.RIGHT)
                self.play(m.Create(stairs, run_time=3))
        ```
    """
    last = self.get_last_point()
    p = np.asarray(point, dtype=float)
    return self.add_cubic_bezier_curve_to(
        *(interpolate(last, p, t) for t in _T_VALUES[1:])
    )
````

### add\_points\_as\_corners

Add straight lines from where the path ends through each point in turn.

The path must have a point to start from.

```python
path.add_points_as_corners(points)
```

**`points`**

The corners, in scene coordinates, in order: the path then ends at the last.

### add\_smooth\_curve\_to

**Code**

```python
import manimgx as m

class VMobjectAddSmoothCurveToExample(m.Scene):
    def construct(self) -> None:
        wave = m.VMobject(color=m.YELLOW, stroke_width=8)
        wave.start_new_path([-6, 0, 0])
        wave.add_cubic_bezier_curve_to([-6, 2, 0], [-4, 2, 0], [-4, 0, 0])
        for x in (-2, 0, 2, 4, 6):
            wave.add_smooth_curve_to([x, 0, 0])
        self.play(m.Create(wave, run_time=3))
```

Add a curve that continues the path smoothly: it leaves where the path ends in the direction the path arrives there.

Its first handle is the path's last handle mirrored through the path's end. Given only the anchor, the curve arrives there as the mirror image of how it leaves (mirrored across the perpendicular bisector of the line between its ends); given a second handle first, it arrives heading away from that. With no curve to continue, after start\_new\_path, it is a straight line to the anchor.

```python
path.add_smooth_curve_to(*points)
```

**`*points`**

The anchor where the curve ends, or the second handle and then the anchor, in scene coordinates.

        import manimgx as m

        class VMobjectAddSmoothCurveToExample(m.Scene):
            def construct(self) -> None:
                wave = m.VMobject(color=m.YELLOW, stroke_width=8)
                wave.start_new_path([-6, 0, 0])
                wave.add_cubic_bezier_curve_to([-6, 2, 0], [-4, 2, 0], [-4, 0, 0])
                for x in (-2, 0, 2, 4, 6):
                    wave.add_smooth_curve_to([x, 0, 0])
                self.play(m.Create(wave, run_time=3))
        ```
    """
    if len(points) == 1:
        handle2, new_anchor = None, np.asarray(points[0])
    elif len(points) == 2:
        handle2, new_anchor = np.asarray(points[0]), np.asarray(points[1])
    else:
        raise ValueError("Only call add_smooth_curve_to with 1 or 2 points")
    if self.has_new_path_started():
        return self.add_line_to(new_anchor)
    last_h2, last_a2 = self.points[-2:]
    tangent = last_a2 - last_h2
    handle1 = last_a2 + tangent
    if handle2 is None:  # the tangent mirrored across the ends' bisector
        chord = normalize(new_anchor - last_a2)
        handle2 = new_anchor + tangent - 2 * (tangent @ chord) * chord
    return self.append_points([last_a2, handle1, handle2, new_anchor])
````

### add\_cubic\_bezier\_curve\_to

**Code**

```python
import manimgx as m

class VMobjectAddCubicBezierCurveToExample(m.Scene):
    def construct(self) -> None:
        start, h1, h2, end = [-4, -2, 0], [-2, 3, 0], [2, 3, 0], [4, -2, 0]
        path = m.VMobject(color=m.YELLOW, stroke_width=8)
        path.start_new_path(start).add_cubic_bezier_curve_to(h1, h2, end)
        handles = m.VGroup(m.Line(start, h1), m.Line(h2, end))
        dots = [m.Dot(p, radius=0.12) for p in (start, h1, h2, end)]
        self.add(handles.set_color(m.GREY), *dots)
        self.play(m.Create(path, run_time=2))
```

Add a curve from where the path ends to `anchor`, bending toward two handles.

The curve leaves the path's last point heading toward `handle1`, and arrives at `anchor` heading away from `handle2`. The path must have a point to start from.

```python
path.add_cubic_bezier_curve_to(handle1, handle2, anchor)
```

**`handle1`**

The first handle, in scene coordinates.

**`handle2`**

The second handle.

**`anchor`**

Where the curve ends.

        import manimgx as m

        class VMobjectAddCubicBezierCurveToExample(m.Scene):
            def construct(self) -> None:
                start, h1, h2, end = [-4, -2, 0], [-2, 3, 0], [2, 3, 0], [4, -2, 0]
                path = m.VMobject(color=m.YELLOW, stroke_width=8)
                path.start_new_path(start).add_cubic_bezier_curve_to(h1, h2, end)
                handles = m.VGroup(m.Line(start, h1), m.Line(h2, end))
                dots = [m.Dot(p, radius=0.12) for p in (start, h1, h2, end)]
                self.add(handles.set_color(m.GREY), *dots)
                self.play(m.Create(path, run_time=2))
        ```
    """
    self._require_points()
    new = [handle1, handle2, anchor]
    return self.append_points(
        new if self.has_new_path_started() else [self.get_last_point(), *new]
    )
````

### add\_quadratic\_bezier\_curve\_to

**Code**

```python
import manimgx as m

class VMobjectAddQuadraticBezierCurveToExample(m.Scene):
    def construct(self) -> None:
        start, handle, end = [-4, -2, 0], [0, 3, 0], [4, -2, 0]
        path = m.VMobject(color=m.TEAL, stroke_width=8)
        path.start_new_path(start)
        path.add_quadratic_bezier_curve_to(handle, end)
        handles = m.VGroup(m.Line(start, handle), m.Line(handle, end))
        dots = [m.Dot(p, radius=0.12) for p in (start, handle, end)]
        self.add(handles.set_color(m.GREY), *dots)
        self.play(m.Create(path, run_time=2))
```

Add a quadratic Bézier curve from where the path ends to `anchor`, bending toward one handle.

It is added as the cubic curve of the same shape. The path must have a point to start from.

```python
path.add_quadratic_bezier_curve_to(handle, anchor)
```

**`handle`**

The handle, in scene coordinates: the curve leaves the path's last point heading toward it, and arrives at `anchor` heading away from it.

**`anchor`**

Where the curve ends.

        import manimgx as m

        class VMobjectAddQuadraticBezierCurveToExample(m.Scene):
            def construct(self) -> None:
                start, handle, end = [-4, -2, 0], [0, 3, 0], [4, -2, 0]
                path = m.VMobject(color=m.TEAL, stroke_width=8)
                path.start_new_path(start)
                path.add_quadratic_bezier_curve_to(handle, end)
                handles = m.VGroup(m.Line(start, handle), m.Line(handle, end))
                dots = [m.Dot(p, radius=0.12) for p in (start, handle, end)]
                self.add(handles.set_color(m.GREY), *dots)
                self.play(m.Create(path, run_time=2))
        ```
    """
    h, a, last = np.asarray(handle), np.asarray(anchor), self.get_last_point()
    return self.add_cubic_bezier_curve_to(
        2 / 3 * h + 1 / 3 * last, 2 / 3 * h + 1 / 3 * a, a
    )
````

### add\_cubic\_bezier\_curve

Add a curve from `anchor1` to `anchor2`, bending toward two handles: a new subpath, unless `anchor1` is where the path ends.

Its four points are appended as they are, so the path's curves must all be whole: after start\_new\_path, use add\_cubic\_bezier\_curve\_to.

```python
path.add_cubic_bezier_curve(anchor1, handle1, handle2, anchor2)
```

**`anchor1`**

Where the curve starts, in scene coordinates.

**`handle1`**

The handle it leaves `anchor1` heading toward.

**`handle2`**

The handle it arrives at `anchor2` heading away from.

**`anchor2`**

Where it ends.

### add\_cubic\_bezier\_curves

Add curves after the path's own, given by their control points, four per curve: anchor, handle, handle, anchor.

```python
path.add_cubic_bezier_curves(curves)
```

**`curves`**

The curves' control points, in scene coordinates: an (n, 4, 3) array, or the points one after another.

### add\_subpath

Add curves after the path's own, by their control points, four per curve: a new subpath, unless they start where the path ends.

```python
path.add_subpath(points)
```

**`points`**

The curves' control points, in scene coordinates.

### append\_vectorized\_mobject

Add another path's curves after this path's own: its points, not its submobjects.

A subpath just started and given no curve yet (see start\_new\_path) is dropped for them.

```python
path.append_vectorized_mobject(vmobject)
```

**`vmobject`**

The path whose points to add.

### close\_path

**Code**

```python
import manimgx as m

class VMobjectClosePathExample(m.Scene):
    def construct(self) -> None:
        corners = [[-2, -1.5, 0], [0, 1.5, 0], [2, -1.5, 0]]
        style = {"fill_opacity": 0.5, "stroke_width": 8}
        open_path = m.VMobject(color=m.GREEN, **style)
        closed_path = m.VMobject(color=m.YELLOW, **style)
        open_path.set_points_as_corners(corners)
        closed_path.set_points_as_corners(corners).close_path()
        self.add(m.VGroup(open_path, closed_path).arrange(buff=2))
```

Close the path: add a straight line from where it ends back to where its last subpath starts, unless it ends where it starts.

The fill closes every subpath anyway; closing one makes its stroke go all the way around.

```python
path.close_path()
```

        import manimgx as m

        class VMobjectClosePathExample(m.Scene):
            def construct(self) -> None:
                corners = [[-2, -1.5, 0], [0, 1.5, 0], [2, -1.5, 0]]
                style = {"fill_opacity": 0.5, "stroke_width": 8}
                open_path = m.VMobject(color=m.GREEN, **style)
                closed_path = m.VMobject(color=m.YELLOW, **style)
                open_path.set_points_as_corners(corners)
                closed_path.set_points_as_corners(corners).close_path()
                self.add(m.VGroup(open_path, closed_path).arrange(buff=2))
        ```
    """
    if not self.is_closed():
        self.add_line_to(self.get_subpaths()[-1][0])
    return self
````

### is\_closed

Whether the path ends where it starts: its first and last points coincide, within a millionth of a unit.

```python
path.is_closed()
```

## Smooth or sharp

### make\_smooth

**Code**

```python
import manimgx as m

class VMobjectMakeSmoothExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=4, color=m.BLUE, stroke_width=8)
        self.add(square.copy().set_stroke(m.GREY, 3))
        self.play(square.animate.make_smooth(), run_time=2)
```

Make every subpath in the family a smooth curve through its anchors, with no change of curvature at any (a cubic spline); a closed subpath closes smoothly.

The anchors stay and the handles move: a polygon becomes a rounded loop through its corners.

```python
path.make_smooth()
```

        import manimgx as m

        class VMobjectMakeSmoothExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=4, color=m.BLUE, stroke_width=8)
                self.add(square.copy().set_stroke(m.GREY, 3))
                self.play(square.animate.make_smooth(), run_time=2)
        ```
    """
    return self.change_anchor_mode("smooth")
````

### make\_jagged

Make every subpath in the family straight lines between its anchors: a curve through points becomes the polygon through them.

```python
path.make_jagged()
```

### insert\_n\_curves

Divide the path's curves into more curves, its shape unchanged.

Each curve is split into equal stretches of its parameter, the new curves spread among the curves as evenly as can be (curve i of m gets the new curves j of n with j·m // n = i): the way a transform gives two paths as many curves as each other.

```python
path.insert_n_curves(n)
```

**`n`**

How many curves to add.

## Along a path

### get\_start

The mobject's first point: where a path starts.

Raises an exception if the mobject has no points of its own.

```python
mobject.get_start()
```

Returns The point, in scene coordinates.

### get\_end

The mobject's last point: where a path ends.

Raises an exception if the mobject has no points of its own.

```python
mobject.get_end()
```

Returns The point, in scene coordinates.

### get\_midpoint

The point halfway along the mobject: for a path, half its length from its start.

```python
mobject.get_midpoint()
```

Returns The point, in scene coordinates.

### point\_from\_proportion

**Code**

```python
import manimgx as m

class VMobjectPointFromProportionExample(m.Scene):
    def construct(self) -> None:
        points = [[-5, -2, 0], [-2, 2, 0], [1, -1, 0], [5, 2, 0]]
        curve = m.VMobject(color=m.BLUE, stroke_width=6)
        curve.set_points_smoothly(points)
        self.add(curve)
        for alpha in (0, 0.25, 0.5, 0.75, 1):
            point = curve.point_from_proportion(alpha)
            dot = m.Dot(point, radius=0.15, color=m.YELLOW)
            label = m.Text(str(alpha), font_size=32).next_to(dot, m.DOWN)
            self.add(dot, label)
```

The point a proportion of the way along the path, by length: 0 is its start, 1 its end.

The length is the path's own measure, the one a reveal draws by (nine straight pieces per curve), so it is where a Create at that proportion has drawn to, and a MoveAlongPath moves at a steady speed. Raises an exception if `alpha` is outside \[0, 1\] or the path has no points.

```python
path.point_from_proportion(alpha)
```

**`alpha`**

The proportion, from 0 to 1.

Returns The point, in scene coordinates.

        import manimgx as m

        class VMobjectPointFromProportionExample(m.Scene):
            def construct(self) -> None:
                points = [[-5, -2, 0], [-2, 2, 0], [1, -1, 0], [5, 2, 0]]
                curve = m.VMobject(color=m.BLUE, stroke_width=6)
                curve.set_points_smoothly(points)
                self.add(curve)
                for alpha in (0, 0.25, 0.5, 0.75, 1):
                    point = curve.point_from_proportion(alpha)
                    dot = m.Dot(point, radius=0.15, color=m.YELLOW)
                    label = m.Text(str(alpha), font_size=32).next_to(dot, m.DOWN)
                    self.add(dot, label)
        ```
    """
    if alpha < 0 or alpha > 1:
        raise ValueError(f"Alpha {alpha} not between 0 and 1.")
    self._require_points()
    curves = self.get_num_curves()
    if curves == 0:  # a point, or a subpath just started
        return self.points[-1]
    at = self._geometry.parameter_at(alpha)
    n = min(int(at), curves - 1)
    return self.get_nth_curve_function(n)(at - n)
````

### proportion\_from\_point

How far along the path a point on it lies, by length: the inverse of point\_from\_proportion.

The first curve the point lies on counts. Raises an exception if the point is not on the path.

```python
path.proportion_from_point(point, tolerance=1e-06)
```

**`point`**

The point, in scene coordinates.

**`tolerance`**

How near the path the point must be: within 100 times this, in scene units, along each axis.

Returns The proportion, from 0 (the path's start) to 1 (its end).

### get\_arc\_length

The path's length: the sum of its curves' lengths, each measured along straight pieces between points on it.

```python
path.get_arc_length(sample_points_per_curve=None)
```

**`sample_points_per_curve`**

How many points each curve is measured through, its ends included; None for 10, the path's own measure.

Returns The length, in scene units.

### get\_subcurve

**Code**

```python
import manimgx as m

class VMobjectGetSubcurveExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=2.5, color=m.GREY)
        half = circle.get_subcurve(0.25, 0.75).set_stroke(m.YELLOW, 12)
        self.add(circle)
        self.play(m.Create(half))
```

A copy of the path cut down to its part from proportion `a` of the way along it to proportion `b`.

The proportions go by the path's curves, each an equal share whatever its length, and along each curve by its parameter (point\_from\_proportion goes by length). The copy's submobjects are copied whole.

```python
path.get_subcurve(a, b)
```

**`a`**

Where the part starts, from 0 to 1.

**`b`**

Where it ends, from `a` to 1.

Returns A new path.

        import manimgx as m

        class VMobjectGetSubcurveExample(m.Scene):
            def construct(self) -> None:
                circle = m.Circle(radius=2.5, color=m.GREY)
                half = circle.get_subcurve(0.25, 0.75).set_stroke(m.YELLOW, 12)
                self.add(circle)
                self.play(m.Create(half))
        ```
    """
    return self.copy().pointwise_become_partial(self, a, b)
````

## Which way it runs

### get\_direction

Which way the path turns: "CW" (clockwise) or "CCW" (counterclockwise), by the sign of the area its curves' start anchors enclose.

```python
path.get_direction()
```

Returns "CW" or "CCW".

### reverse\_direction

**Code**

```python
import manimgx as m

class VMobjectReverseDirectionExample(m.Scene):
    def construct(self) -> None:
        outer, inner = m.Square(side_length=4), m.Square(side_length=2)
        same = m.VMobject(color=m.BLUE, fill_opacity=0.8)
        same.append_vectorized_mobject(outer)
        same.append_vectorized_mobject(inner)
        opposite = m.VMobject(color=m.YELLOW, fill_opacity=0.8)
        opposite.append_vectorized_mobject(outer)
        opposite.append_vectorized_mobject(inner.reverse_direction())
        self.add(m.VGroup(same, opposite).arrange(buff=2))
```

Reverse the order of the path's own points, so it runs the other way: from its end to its start.

Its submobjects stay as they are. A drawing animation then draws it the other way, and a subpath inside another cuts a hole in the fill only if the two run opposite ways.

```python
path.reverse_direction()
```

        import manimgx as m

        class VMobjectReverseDirectionExample(m.Scene):
            def construct(self) -> None:
                outer, inner = m.Square(side_length=4), m.Square(side_length=2)
                same = m.VMobject(color=m.BLUE, fill_opacity=0.8)
                same.append_vectorized_mobject(outer)
                same.append_vectorized_mobject(inner)
                opposite = m.VMobject(color=m.YELLOW, fill_opacity=0.8)
                opposite.append_vectorized_mobject(outer)
                opposite.append_vectorized_mobject(inner.reverse_direction())
                self.add(m.VGroup(same, opposite).arrange(buff=2))
        ```
    """
    self.points = self.points[::-1].copy()
    return self
````

### force\_direction

Make the path run clockwise or counterclockwise: reverse it if it runs the other way (see get\_direction).

```python
path.force_direction(target_direction)
```

**`target_direction`**

"CW" for clockwise, "CCW" for counterclockwise.

## Its points

### points

The mobject's own points, in scene coordinates: an (n, 3) array, read-only.

A path's are the control points of its cubic Bézier curves, four per curve. Assign an array to reshape the mobject; its submobjects keep theirs. Assigning the points it has changes nothing (it keeps its geometry, and all that was derived from it), unless they are a blend of shapes, as mid-morph, which become one; assigning them with more after them grows it.

```python
mobject.points
```

### set\_points

Give the mobject new points of its own, in place of its present ones.

```python
mobject.set_points(points)
```

**`points`**

The points, in scene coordinates: an (n, 3) array.

### reset\_points

Remove the mobject's own points; its submobjects keep theirs.

```python
mobject.reset_points()
```

### has\_points

Whether the mobject has points of its own (a group has none: its members do).

```python
mobject.has_points()
```

### append\_points

Add control points after the path's own: taken four by four, the path's points are its curves.

```python
path.append_points(new_points)
```

**`new_points`**

The points, in scene coordinates: an (n, 3) array.

### get\_anchors

The path's anchors, curve by curve: each curve's start, then its end, so an anchor two curves share is listed twice.

```python
path.get_anchors()
```

Returns An array of points, in scene coordinates; for a path of one point, that point.

### get\_subpaths

The path's subpaths: a subpath starts wherever a curve does not begin where the one before it ends.

```python
path.get_subpaths()
```

Returns The subpaths, each an array of its control points, four per curve.

### get\_num\_curves

How many curves the path has: its points, four per curve.

```python
path.get_num_curves()
```

Returns The number of curves.

### bezier

A cubic Bézier curve as a function: from its first control point at 0 to its last at 1.

```python
m.bezier(points)
```

**`points`**

Its four control points: anchor, handle, handle, anchor.

Returns A function of the curve's parameter, from 0 to 1, giving its point there.

## Paths made from paths

### CubicBezier

**Code**

```python
import manimgx as m

class CubicBezierExample(m.Scene):
    def construct(self) -> None:
        start, end = [-5, -2, 0], [5, -2, 0]
        handle1, handle2 = [-3, 3, 0], [6, 3, 0]
        curve = m.CubicBezier(start, handle1, handle2, end, color=m.YELLOW)
        levers = m.VGroup(m.Line(start, handle1), m.Line(end, handle2))
        levers.set_stroke(m.GREY, width=2)
        anchors = m.VGroup(m.Dot(start), m.Dot(end)).set_color(m.BLUE)
        handles = m.VGroup(m.Dot(handle1), m.Dot(handle2)).set_color(m.RED)
        self.add(levers, anchors, handles)
        self.play(m.Create(curve, run_time=2))
```

A cubic Bézier curve: from one anchor to another, pulled toward two handles; white unless styled.

The curve leaves its start heading toward `start_handle` and comes into its end from the direction of `end_handle`; the farther a handle, the longer the curve keeps to its direction. It passes through neither handle.

```python
m.CubicBezier(start_anchor, start_handle, end_handle, end_anchor, **kwargs)
```

**`start_anchor`**

Where the curve starts.

**`start_handle`**

The handle of its start.

**`end_handle`**

The handle of its end.

**`end_anchor`**

Where the curve ends.

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

### DashedVMobject

**Code**

```python
import manimgx as m

class DashedVMobjectExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=1.5, color=m.BLUE, stroke_width=6)
        square = m.Square(side_length=3, color=m.GREEN, stroke_width=6)
        arc = m.Arc(radius=2, angle=m.PI, color=m.YELLOW, stroke_width=6)
        shapes = m.VGroup(
            m.DashedVMobject(circle, num_dashes=12),
            m.DashedVMobject(square, num_dashes=16, dashed_ratio=0.7),
            m.DashedVMobject(arc, num_dashes=7, dashed_ratio=0.3),
        ).arrange(buff=1)
        self.play(m.Create(shapes, run_time=2))
```

A path drawn in dashes: evenly spaced dashes along another path, in its style.

An open path starts and ends with a dash; a closed one has as many gaps as dashes, all the way around. Each dash ends as the path's `cap_style` says, and an arrow's tips are drawn whole.

```python
m.DashedVMobject(vmobject, num_dashes=15, dashed_ratio=0.5, dash_offset=0, equal_lengths=True, **kwargs)
```

**`vmobject`**

The path to draw in dashes.

**`num_dashes`**

How many dashes; 0 draws none.

**`dashed_ratio`**

The fraction of the path the dashes cover, from 0 to 1; the gaps take the rest.

**`dash_offset`**

How far the dashes are moved along the path, toward its end, as a fraction of a dash and the gap after it.

**`equal_lengths`**

Whether the dashes are equally long; if False they are equal stretches of the path's parameter, longer where the path runs faster.

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

### CurvesAsSubmobjects

**Code**

```python
import numpy as np

import manimgx as m

class CurvesAsSubmobjectsExample(m.Scene):
    def construct(self) -> None:
        curve = m.ParametricFunction(
            lambda t: [2 * t, 2 * np.sin(t), 0], t_range=(-3, 3, 0.1)
        )
        parts = m.CurvesAsSubmobjects(curve.set_stroke(width=12))
        parts.set_color_by_gradient(m.BLUE, m.YELLOW, m.RED)
        self.play(m.Create(parts, run_time=2))
```

A path split into its curves: a group of one path per curve, each styled as the path is.

Each part can then be styled or animated on its own: a gradient across the parts colors the path along its length. Only the path's own curves are taken, not its submobjects'.

```python
m.CurvesAsSubmobjects(vmobject, **kwargs)
```

**`vmobject`**

The path to split.

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

### VectorizedPoint

**Code**

```python
import manimgx as m

class VectorizedPointExample(m.Scene):
    def construct(self) -> None:
        point = m.VectorizedPoint(4 * m.LEFT)
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        self.play(m.ReplacementTransform(point, square.shift(2 * m.RIGHT)))
```

A path of one point: unseen, a place to put things by, or to grow them from.

It is black, with no stroke and no fill. Its width and height are numbers of its own, not measured from its point.

```python
m.VectorizedPoint(location=ORIGIN, artificial_width=0.01, artificial_height=0.01, **kwargs)
```

**`location`**

Where the point is, in scene coordinates.

**`artificial_width`**

The width it reports, in scene units.

**`artificial_height`**

The height it reports, in scene units.

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

#### width

The point's width, in scene units: its `artificial_width`, not measured. Setting it changes that number and nothing else.

```python
vectorized_point.width
```

#### height

The point's height, in scene units: its `artificial_height`, not measured. Setting it changes that number and nothing else.

```python
vectorized_point.height
```
