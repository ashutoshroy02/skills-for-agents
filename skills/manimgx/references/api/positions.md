# Positions

**The film's code**

```python
import manimgx as m

class PositionsHero(m.Scene):
    def construct(self) -> None:
        plane = m.NumberPlane(
            background_line_style={"stroke_color": m.GREY_D, "stroke_width": 1},
            axis_config={"stroke_color": m.GREY_B, "stroke_width": 2},
        )
        self.add(plane)
        names = ["ORIGIN", "UP", "DOWN", "LEFT", "RIGHT", "UL", "UR", "DL", "DR"]
        points = [m.ORIGIN, m.UP, m.DOWN, m.LEFT, m.RIGHT, m.UL, m.UR, m.DL, m.DR]
        dots = m.VGroup()
        labels = m.VGroup()
        for name, point in zip(names, points, strict=True):
            dot = m.Dot(2.5 * point, radius=0.12, color=m.YELLOW)
            label = m.Text(name, font="monospace", font_size=30)
            label.next_to(dot, m.DOWN, buff=0.2)
            label.add_background_rectangle(opacity=1, buff=0.05)
            dots.add(dot)
            labels.add(label)
        self.play(
            m.LaggedStart(*[m.GrowFromCenter(dot) for dot in dots], lag_ratio=0.1)
        )
        self.play(m.FadeIn(labels))
        self.wait()
```

Every mobject has a place in the frame. A place is a point, three numbers `[x, y, z]`, measured in units from the frame's center. x grows to the right, y grows upward, and z grows out of the screen, toward the viewer. The frame's short side is 8 units: a wide video shows y from −4 to 4, and x from about −7.1 to 7.1.

A mobject's place is its bounding box: the smallest box, along the axes, around what it draws. Its center, its edges and its corners are points of that box. The methods below read those points, and move the mobject so that one of them goes where you say. Each method moves the mobject's parts with it, and gives the mobject back, so that calls chain: `m.Text("Title").scale(1.5).to_edge(m.UP)`.

## Directions

The axis directions are unit vectors; the diagonals are sums of them. Multiply a direction by a number, and add directions together, to make other points: `3 * m.RIGHT + 2 * m.UP` is `[3, 2, 0]`.

### m.ORIGIN

The center of the scene: (0, 0, 0).

### m.UP

One unit up: (0, 1, 0).

### m.DOWN

One unit down: (0, −1, 0).

### m.LEFT

One unit left: (−1, 0, 0).

### m.RIGHT

One unit right: (1, 0, 0).

### m.UL

Up and left, toward the upper left corner: (−1, 1, 0).

### m.UR

Up and right, toward the upper right corner: (1, 1, 0).

### m.DL

Down and left, toward the lower left corner: (−1, −1, 0).

### m.DR

Down and right, toward the lower right corner: (1, −1, 0).

### m.IN

One unit into the screen, away from the viewer: (0, 0, −1).

### m.OUT

One unit out of the screen, toward the viewer: (0, 0, 1).

### m.X\_AXIS

The direction of the x axis: (1, 0, 0).

### m.Y\_AXIS

The direction of the y axis: (0, 1, 0).

### m.Z\_AXIS

The direction of the z axis, out of the screen: (0, 0, 1).

## Where a mobject is

Each of these reads a point of the mobject's bounding box, or one of its coordinates.

### get\_center

The center of the mobject's bounding box.

```python
mobject.get_center()
```

Returns The point, in scene coordinates.

### get\_top

The middle of the top edge of the mobject's bounding box.

```python
mobject.get_top()
```

Returns The point, in scene coordinates.

### get\_bottom

The middle of the bottom edge of the mobject's bounding box.

```python
mobject.get_bottom()
```

Returns The point, in scene coordinates.

### get\_left

The middle of the left edge of the mobject's bounding box.

```python
mobject.get_left()
```

Returns The point, in scene coordinates.

### get\_right

The middle of the right edge of the mobject's bounding box.

```python
mobject.get_right()
```

Returns The point, in scene coordinates.

### get\_corner

A corner of the mobject's bounding box, named by a direction (`get_corner(UR)`): another name for get\_critical\_point.

### get\_critical\_point

A point of the mobject's bounding box, named by a direction: its center, the middle of an edge, or a corner.

Each coordinate is the box's lowest where the direction's is negative, its highest where it is positive, and its middle where it is 0: UR names the top right corner, UP the middle of the top edge, ORIGIN the center. The box is boundary\_box, around what the mobject draws: a path's curves themselves, not their control points.

```python
mobject.get_critical_point(direction)
```

**`direction`**

The direction, such as UP, UR or ORIGIN.

Returns The point, in scene coordinates; the origin if the mobject has no points.

### get\_boundary\_point

The point of the mobject farthest in a direction: of the points it is drawn through, the one farthest along `direction`.

Unlike get\_critical\_point, it is one of those points (for a path, an end of one of its curves), not a point of the mobject's bounding box.

```python
mobject.get_boundary_point(direction)
```

Returns The point, in scene coordinates.

### get\_x

The x coordinate of the mobject's center, or of an edge of its bounding box.

```python
mobject.get_x(direction=ORIGIN)
```

**`direction`**

LEFT for its left edge, RIGHT for its right edge; ORIGIN (default) for its center.

### get\_y

The y coordinate of the mobject's center, or of an edge of its bounding box.

```python
mobject.get_y(direction=ORIGIN)
```

**`direction`**

DOWN for its bottom edge, UP for its top edge; ORIGIN (default) for its center.

### get\_z

The z coordinate of the mobject's center, or of a face of its bounding box.

```python
mobject.get_z(direction=ORIGIN)
```

**`direction`**

IN for its lowest z, OUT for its highest; ORIGIN (default) for its center.

### boundary\_box

The mobject's bounding box: the smallest box, aligned with the axes, around what its family draws.

A path is measured by its curves themselves, not by their control points (a curve bulges past its anchors where it turns, and its handles reach past the curve); any other kind by its points. A stroke's width is not counted. It is the one box every measure reads: width and height, the corners, edges and center (get\_critical\_point), `get_x` and `get_y`, alignment and layout, and the extent of a color gradient. It joins the boxes of the family's members, so a member spans the same in whatever group holds it.

```python
mobject.boundary_box()
```

Returns A 2 × 3 array, the lowest (x, y, z) then the highest; None if the family has no points.

## Move a mobject

### move\_to

**Code**

```python
import manimgx as m

class MobjectMoveToExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot([3, 1.5, 0], radius=0.15, color=m.YELLOW)
        origin = m.Dot(radius=0.15, color=m.RED)
        square = m.Square(color=m.BLUE, fill_opacity=0.5).shift(4 * m.LEFT)
        self.add(dot, origin, square)
        self.play(square.animate.move_to(dot))
        self.play(square.animate.move_to(m.ORIGIN, aligned_edge=m.DL))
```

Move the mobject to a point, or onto another mobject: its center, or the point of its bounding box `aligned_edge` names, goes there.

```python
mobject.move_to(point_or_mobject, aligned_edge=ORIGIN, coor_mask=(1, 1, 1))
```

**`point_or_mobject`**

A point, in scene coordinates, or a mobject: then the point of its bounding box `aligned_edge` names (its center, by default).

**`aligned_edge`**

The point of the mobject that goes there, named by a direction: ORIGIN (default) for its center, DL for its bottom left corner.

**`coor_mask`**

Which coordinates change: 1 for each axis the mobject moves along, 0 for one it keeps (`(1, 0, 0)` moves it horizontally only).

        import manimgx as m

        class MobjectMoveToExample(m.Scene):
            def construct(self) -> None:
                dot = m.Dot([3, 1.5, 0], radius=0.15, color=m.YELLOW)
                origin = m.Dot(radius=0.15, color=m.RED)
                square = m.Square(color=m.BLUE, fill_opacity=0.5).shift(4 * m.LEFT)
                self.add(dot, origin, square)
                self.play(square.animate.move_to(dot))
                self.play(square.animate.move_to(m.ORIGIN, aligned_edge=m.DL))
        ```
    """
    if isinstance(point_or_mobject, Mobject):
        target = point_or_mobject.get_critical_point(aligned_edge)
    else:
        target = np.asarray(point_or_mobject, dtype=float)
    return self.shift(
        (target - self.get_critical_point(aligned_edge)) * np.asarray(coor_mask)
    )
````

### shift

**Code**

```python
import manimgx as m

class MobjectShiftExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        self.add(square)
        self.play(square.animate.shift(4 * m.LEFT))
        self.play(square.animate.shift(2 * m.UP, 8 * m.RIGHT))
```

Move the mobject and its whole family by a vector.

```python
mobject.shift(*vectors)
```

**`*vectors`**

The vector, in scene units (`2 * RIGHT` moves it two units right); several are added into one.

        import manimgx as m

        class MobjectShiftExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(color=m.BLUE, fill_opacity=0.5)
                self.add(square)
                self.play(square.animate.shift(4 * m.LEFT))
                self.play(square.animate.shift(2 * m.UP, 8 * m.RIGHT))
        ```
    """
    # one vector (a (1, 3) array too, as CE takes it)
    vector = vectors[0] if len(vectors) == 1 else reduce(np.add, vectors)
    total = np.asarray(vector, dtype=float).reshape(-1)
    for mob in self.family_members_with_points():
        mob._geometry = mob._geometry.translated(total)
    return self
````

### center

Move the mobject so the center of its bounding box is at the origin.

```python
mobject.center()
```

### set\_x

Move the mobject left or right so its center, or an edge of its bounding box, is at `x`.

```python
mobject.set_x(x, direction=ORIGIN)
```

**`x`**

The x coordinate, in scene units.

**`direction`**

LEFT to place its left edge, RIGHT its right edge; ORIGIN (default) its center.

### set\_y

Move the mobject up or down so its center, or an edge of its bounding box, is at `y`.

```python
mobject.set_y(y, direction=ORIGIN)
```

**`y`**

The y coordinate, in scene units.

**`direction`**

DOWN to place its bottom edge, UP its top edge; ORIGIN (default) its center.

### set\_z

Move the mobject in or out so its center, or a face of its bounding box, is at `z`.

```python
mobject.set_z(z, direction=ORIGIN)
```

**`z`**

The z coordinate, in scene units.

**`direction`**

IN to place its lowest z, OUT its highest; ORIGIN (default) its center.

## Place a mobject by another

A gap between two mobjects is a buff. These are its usual sizes.

### m.SMALL\_BUFF

A small gap, in scene units: 0.1.

### m.MED\_SMALL\_BUFF

A medium-small gap, in scene units: 0.25, the default between mobjects placed next to each other.

### m.MED\_LARGE\_BUFF

A medium-large gap, in scene units: 0.5, the default between a mobject and the frame's edge.

### m.LARGE\_BUFF

A large gap, in scene units: 1.

### m.DEFAULT\_MOBJECT\_TO\_MOBJECT\_BUFFER

The gap between mobjects placed next to each other by default, in scene units: 0.25 (`next_to`, `arrange`).

### m.DEFAULT\_MOBJECT\_TO\_EDGE\_BUFFER

The gap a mobject keeps from the frame's edge by default, in scene units: 0.5 (`to_edge`, `to_corner`).

### next\_to

**Code**

```python
import manimgx as m

class MobjectNextToExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        right = m.Text("RIGHT").next_to(square, m.RIGHT)
        up = m.Text("UP, aligned LEFT").next_to(
            square, m.UP, aligned_edge=m.LEFT
        )
        down = m.Text("DOWN, buff=1").next_to(square, m.DOWN, buff=1)
        dot = m.Dot(radius=0.2, color=m.YELLOW)
        dot.next_to(square, m.UL, buff=0)
        self.add(square, right, up, down, dot)
```

Put the mobject beside another, or beside a point, `buff` away in a direction.

The side of the mobject facing back along `direction` goes to the other's side facing along it, `buff` farther on: with RIGHT, the middle of its left edge goes `buff` to the right of the middle of the other's right edge. A diagonal direction (UR) puts corner to corner.

```python
mobject.next_to(mobject_or_point, direction=RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, aligned_edge=ORIGIN, submobject_to_align=None, index_of_submobject_to_align=None, coor_mask=(1, 1, 1))
```

**`mobject_or_point`**

The mobject (its bounding box) or the point to put it beside.

**`direction`**

The side: RIGHT (default), UP, DL, …

**`buff`**

The gap, in scene units, along `direction` (default 0.25).

**`aligned_edge`**

The edge along which the two line up besides the side they meet at, named by a direction: with the direction RIGHT and UP here, their tops line up (default ORIGIN: centered).

**`submobject_to_align`**

A part of the mobject to put beside the other in its place; the rest moves with it.

**`index_of_submobject_to_align`**

The index of the part of each mobject to line up: this one's part goes beside the other's.

**`coor_mask`**

Which coordinates change: 1 for each axis the mobject moves along, 0 for one it keeps.

        import manimgx as m

        class MobjectNextToExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
                right = m.Text("RIGHT").next_to(square, m.RIGHT)
                up = m.Text("UP, aligned LEFT").next_to(
                    square, m.UP, aligned_edge=m.LEFT
                )
                down = m.Text("DOWN, buff=1").next_to(square, m.DOWN, buff=1)
                dot = m.Dot(radius=0.2, color=m.YELLOW)
                dot.next_to(square, m.UL, buff=0)
                self.add(square, right, up, down, dot)
        ```
    """
    d, edge = (
        np.asarray(direction, dtype=float),
        np.asarray(aligned_edge, dtype=float),
    )
    if isinstance(mobject_or_point, Mobject):
        target_aligner = (
            mobject_or_point
            if index_of_submobject_to_align is None
            else mobject_or_point[index_of_submobject_to_align]
        )
        target = target_aligner.get_critical_point(edge + d)
    else:
        target = np.asarray(mobject_or_point, dtype=float)
    if submobject_to_align is not None:
        aligner: Mobject = submobject_to_align
    elif index_of_submobject_to_align is not None:
        aligner = self[index_of_submobject_to_align]
    else:
        aligner = self
    point_to_align = aligner.get_critical_point(edge - d)
    return self.shift((target - point_to_align + buff * d) * np.asarray(coor_mask))
````

### align\_to

**Code**

```python
import manimgx as m

class MobjectAlignToExample(m.Scene):
    def construct(self) -> None:
        floor = m.Line(6 * m.LEFT, 6 * m.RIGHT).shift(3 * m.DOWN)
        shapes = m.VGroup(
            m.Circle(color=m.BLUE),
            m.Square(side_length=3, color=m.GREEN),
            m.Triangle(color=m.YELLOW),
            m.Star(color=m.RED),
        ).arrange(buff=1)
        self.add(floor, shapes)
        self.play(*(s.animate.align_to(floor, m.DOWN) for s in shapes))
```

Move the mobject so a side of it lines up with another's: along each axis on which `direction` is not 0, the side of its bounding box in that direction goes where the other's is.

`align_to(other, UP)` puts its top at the height of the other's top, moving it up or down only; `align_to(other, UL)` lines up both tops and both left sides. With the default ORIGIN, nothing moves.

```python
mobject.align_to(mobject_or_point, direction=ORIGIN)
```

**`mobject_or_point`**

The mobject to line up with (the side of its bounding box `direction` names), or a point.

**`direction`**

The side, named by a direction: UP, DL, …

        import manimgx as m

        class MobjectAlignToExample(m.Scene):
            def construct(self) -> None:
                floor = m.Line(6 * m.LEFT, 6 * m.RIGHT).shift(3 * m.DOWN)
                shapes = m.VGroup(
                    m.Circle(color=m.BLUE),
                    m.Square(side_length=3, color=m.GREEN),
                    m.Triangle(color=m.YELLOW),
                    m.Star(color=m.RED),
                ).arrange(buff=1)
                self.add(floor, shapes)
                self.play(*(s.animate.align_to(floor, m.DOWN) for s in shapes))
        ```
    """
    point = (
        mobject_or_point.get_critical_point(direction)
        if isinstance(mobject_or_point, Mobject)
        else np.asarray(mobject_or_point)
    )
    for dim in range(self.dim):
        if direction[dim] != 0:
            self.set_coord(point[dim], dim, direction)
    return self
````

### match\_x

Move the mobject left or right to another's x: centers, or left or right edges, lined up.

```python
mobject.match_x(mobject, direction=ORIGIN)
```

**`mobject`**

The mobject to match.

**`direction`**

LEFT to line up the left edges, RIGHT the right ones; ORIGIN (default) the centers.

### match\_y

Move the mobject up or down to another's y: centers, or top or bottom edges, lined up.

```python
mobject.match_y(mobject, direction=ORIGIN)
```

**`mobject`**

The mobject to match.

**`direction`**

DOWN to line up the bottom edges, UP the top ones; ORIGIN (default) the centers.

### match\_z

Move the mobject in or out to another's z: centers, or faces, lined up.

```python
mobject.match_z(mobject, direction=ORIGIN)
```

**`mobject`**

The mobject to match.

**`direction`**

IN to line up the lowest z, OUT the highest; ORIGIN (default) the centers.

## Place a mobject in the frame

### to\_edge

**Code**

```python
import manimgx as m

class MobjectToEdgeExample(m.Scene):
    def construct(self) -> None:
        top = m.Text("to_edge(UP)").to_edge(m.UP)
        left = m.Text("to_edge(LEFT)").to_edge(m.LEFT)
        circle = m.Circle(color=m.BLUE).shift(2 * m.DOWN)
        circle.to_edge(m.RIGHT, buff=0)
        self.add(top, left, circle)
```

Move the mobject to an edge of the frame, `buff` in from it; along the edge, it stays where it is.

The frame is the configured one, centered on the origin, wherever the camera looks.

```python
mobject.to_edge(edge=LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
```

**`edge`**

The edge: UP, DOWN, LEFT (default) or RIGHT.

**`buff`**

The margin between the mobject and the edge, in scene units (default 0.5).

        import manimgx as m

        class MobjectToEdgeExample(m.Scene):
            def construct(self) -> None:
                top = m.Text("to_edge(UP)").to_edge(m.UP)
                left = m.Text("to_edge(LEFT)").to_edge(m.LEFT)
                circle = m.Circle(color=m.BLUE).shift(2 * m.DOWN)
                circle.to_edge(m.RIGHT, buff=0)
                self.add(top, left, circle)
        ```
    """
    return self.align_on_border(edge, buff)
````

### to\_corner

**Code**

```python
import manimgx as m

class MobjectToCornerExample(m.Scene):
    def construct(self) -> None:
        self.add(m.Text("UL").to_corner(m.UL))
        self.add(m.Text("UR, buff=0").to_corner(m.UR, buff=0))
        self.add(m.Circle(color=m.BLUE).to_corner(m.DL))
        self.add(m.Square(color=m.YELLOW).to_corner(m.DR, buff=1))
```

Move the mobject into a corner of the frame, `buff` in from both its edges.

The frame is the configured one, centered on the origin, wherever the camera looks.

```python
mobject.to_corner(corner=DL, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
```

**`corner`**

The corner: UL, UR, DL (default) or DR.

**`buff`**

The margin between the mobject and each edge of the frame, in scene units (default 0.5).

        import manimgx as m

        class MobjectToCornerExample(m.Scene):
            def construct(self) -> None:
                self.add(m.Text("UL").to_corner(m.UL))
                self.add(m.Text("UR, buff=0").to_corner(m.UR, buff=0))
                self.add(m.Circle(color=m.BLUE).to_corner(m.DL))
                self.add(m.Square(color=m.YELLOW).to_corner(m.DR, buff=1))
        ```
    """
    return self.align_on_border(corner, buff)
````

### shift\_onto\_screen

Move the mobject back into the frame where it reaches past an edge, or nearer to it than `buff`: to that edge, `buff` in (see to\_edge).

```python
mobject.shift_onto_screen(buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
```

**`buff`**

The margin to keep from the frame's edges, in scene units (default 0.5).

### is\_off\_screen

Whether the mobject is wholly outside the frame: the configured one, centered on the origin.

```python
mobject.is_off_screen()
```

Returns True if its bounding box lies wholly past an edge of the frame.

## Compute a point

Points are NumPy arrays, so NumPy computes with them. These functions do what a scene often needs.

### interpolate

The value a fraction of the way from one value to another: (1 − alpha)·start + alpha·end.

```python
m.interpolate(start, end, alpha)
```

**`start`**

The value at 0: a number or an array.

**`end`**

The value at 1, of the same kind.

**`alpha`**

How far from `start` to `end`: 0 gives `start`, 1 `end`, and beyond them it goes on along the line; an array gives one value per entry.

Returns The value between.

### midpoint

The point halfway between two points.

```python
m.midpoint(p1, p2)
```

**`p1`**

A point.

**`p2`**

Another point.

Returns The point between them.

### normalize

The unit vector in a vector's direction.

```python
m.normalize(vect)
```

**`vect`**

The vector.

Returns The vector divided by its length; the zero vector stays zero.

### rotate\_vector

A vector rotated about an axis through the origin.

```python
m.rotate_vector(vector, angle, axis=_OUT)
```

**`vector`**

The vector; a two-dimensional one gets a z of 0.

**`angle`**

The angle, in radians, counterclockwise as seen from the tip of `axis`.

**`axis`**

The axis's direction.

Returns The rotated vector.

### angle\_of\_vector

The angle of a vector in the xy plane, counterclockwise from the x axis (its z is ignored).

```python
m.angle_of_vector(vector)
```

Returns The angle, in radians, from −π to π.

### angle\_between\_vectors

The angle between two vectors.

```python
m.angle_between_vectors(v1, v2)
```

**`v1`**

A vector.

**`v2`**

Another vector.

Returns The angle, in radians, from 0 to π.

### line\_intersection

Where two lines in the xy plane cross, each line through two points (their z is ignored).

Raises an exception if the lines are parallel.

```python
m.line_intersection(line1, line2)
```

**`line1`**

Two points on the first line.

**`line2`**

Two points on the second line.

Returns The point, with a z of 0.

### perpendicular\_bisector

Two points on the perpendicular bisector of a segment, in the plane perpendicular to a vector.

```python
m.perpendicular_bisector(line, norm_vector=_OUT)
```

**`line`**

The segment's two ends.

**`norm_vector`**

The normal of the plane the bisector lies in.

Returns The segment's midpoint plus and minus its direction crossed with `norm_vector`; for a unit normal, each a segment's length from the midpoint.

### polylabel

The pole of inaccessibility of a polygon: the point inside it farthest from its edges, where a label fits best.

```python
m.polylabel(rings, precision=0.01)
```

**`rings`**

The polygon's rings, each closed (its first vertex repeated at its end): the outline, then any holes. Their x and y count.

**`precision`**

How far, at most, the point found may be from the best, in its distance from the edges, in scene units.

Returns The cell found, whose `c` is the point (x and y) and `d` its distance from the nearest edge.

### inverse\_interpolate

How far a value is from one value to another: the inverse of interpolate.

```python
m.inverse_interpolate(start, end, value)
```

**`start`**

The value at 0.

**`end`**

The value at 1.

Returns The fraction, (value − start) / (end − start).
