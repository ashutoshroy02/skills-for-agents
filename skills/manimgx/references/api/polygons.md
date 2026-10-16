# Polygons

**The film's code**

```python
import manimgx as m

class PolygonsHero(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            m.Triangle(color=m.BLUE),
            m.Square(side_length=1.8, color=m.GREEN),
            m.Rectangle(width=2.6, height=1.5, color=m.YELLOW),
            m.RoundedRectangle(width=2.6, height=1.5, corner_radius=0.4, color=m.TEAL),
            m.RegularPolygon(n=6, color=m.RED),
            m.Star(color=m.GOLD),
        )
        names = [
            "Triangle",
            "Square",
            "Rectangle",
            "RoundedRectangle",
            "RegularPolygon",
            "Star",
        ]
        cells = m.VGroup()
        for shape, name in zip(shapes, names, strict=True):
            label = m.Text(name, font="monospace", font_size=26)
            cells.add(m.VGroup(shape, label.next_to(shape, m.DOWN, buff=0.4)))
        cells.arrange_in_grid(rows=2, buff=(1, 0.8))
        self.play(m.LaggedStart(*[m.Create(cell[0]) for cell in cells], lag_ratio=0.15))
        self.play(m.FadeIn(m.VGroup(*[cell[1] for cell in cells])))
        self.wait()
```

A polygon is a shape of straight sides, from each corner to the next and from the last back to the first. Give `m.Polygon` its corners, or take a ready-made one: a triangle, a square, a rectangle, a regular polygon, a star. Every polygon can round its corners.

A polygram is several polygons in one shape; a polygon is a polygram of one.

## Polygon

**Code**

```python
import manimgx as m

class PolygonExample(m.Scene):
    def construct(self) -> None:
        triangle = m.Polygon([-6, -2, 0], [-1.5, -2, 0], [-3.5, 2.5, 0])
        arrowhead = m.Polygon(
            [1, -2.5, 0],
            [6, 0, 0],
            [1, 2.5, 0],
            [2.5, 0, 0],
            color=m.YELLOW,
            fill_opacity=0.5,
        )
        self.play(m.Create(triangle), m.Create(arrowhead))
```

A polygon: straight sides from each vertex to the next, and from the last back to the first; blue unless styled.

```python
m.Polygon(*vertices, **kwargs)
```

**`*vertices`**

The vertices, in order around it.

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

## Polygram

**Code**

```python
import numpy as np

import manimgx as m

class PolygramExample(m.Scene):
    def construct(self) -> None:
        r = np.sqrt(3)
        hexagram = m.Polygram(
            [[0, 2, 0], [-r, -1, 0], [r, -1, 0]],
            [[-r, 1, 0], [0, -2, 0], [r, 1, 0]],
        )
        framed = m.Polygram(
            [[-2, -2, 0], [2, -2, 0], [2, 2, 0], [-2, 2, 0]],
            [[-1, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]],
            color=m.YELLOW,
            fill_opacity=0.5,
        )
        self.play(m.Create(m.VGroup(hexagram, framed).arrange(buff=2)))
```

A shape of straight sides through groups of vertices: each group a closed path, from vertex to vertex and back to its first; blue unless styled.

The groups make one mobject, filled and stroked together. Where they overlap, the fill counts how many times its paths wind around each point: a group inside another that runs the other way around is a hole.

The vertices are taken as they are given: changing their arrays afterwards changes no shape.

```python
m.Polygram(*vertex_groups, **kwargs)
```

**`*vertex_groups`**

The groups of vertices, each in order around its path.

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

### get\_vertices

The polygram's vertices, group after group: where each of its curves starts (the arcs and sides too, once its corners are rounded).

```python
polygon.get_vertices()
```

Returns An (n, 3) array of points, in scene coordinates.

### get\_vertex\_groups

The polygram's vertices, grouped by the closed paths they are on.

```python
polygon.get_vertex_groups()
```

Returns A list of (n, 3) arrays of points, one per closed path.

### round\_corners

**Code**

```python
import manimgx as m

class PolygramRoundCornersExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(2.8, color=m.YELLOW)
        shapes = m.VGroup(
            m.Star(outer_radius=1.5),
            m.Star(outer_radius=1.5).round_corners(0.25),
            square.round_corners([0.1, 0.4, 0.8, 1.2]),
            m.Triangle(radius=1.6, color=m.GREEN).round_corners(-0.5),
        ).arrange(buff=0.5)
        self.add(shapes)
```

Round the polygram's corners: replace each with an arc of `radius` tangent to its two sides.

An arc touches each side at most halfway along it: a radius too large for a corner is made smaller. A negative radius rounds a corner the other way, cutting a concave arc into it.

```python
polygon.round_corners(radius=0.5, evenly_distribute_anchors=False, components_per_rounded_corner=2)
```

**`radius`**

The arcs' radius, in scene units; or a list of radii, one per corner of each group, from its second vertex's on (its first vertex's last), repeated over the corners: its length must divide their number.

**`evenly_distribute_anchors`**

Whether to divide the straight sides into curves about as long as the arcs' curves, so the outline's points are spread evenly along it (a transform then moves them more evenly).

**`components_per_rounded_corner`**

How many anchor points each arc is drawn through: 2 for one cubic Bézier curve.

        import manimgx as m

        class PolygramRoundCornersExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(2.8, color=m.YELLOW)
                shapes = m.VGroup(
                    m.Star(outer_radius=1.5),
                    m.Star(outer_radius=1.5).round_corners(0.25),
                    square.round_corners([0.1, 0.4, 0.8, 1.2]),
                    m.Triangle(radius=1.6, color=m.GREEN).round_corners(-0.5),
                ).arrange(buff=0.5)
                self.add(shapes)
        ```
    """
    if radius == 0:
        return self
    new_points: list[Point3D_Array] = []
    for vertex_group in self.get_vertex_groups():
        arcs = []
        if isinstance(radius, (int, float)):
            radius_list = [radius] * len(vertex_group)
        else:
            radius_list = radius * ceil(len(vertex_group) / len(radius))
        for current_radius, (v1, v2, v3) in zip(
            radius_list, adjacent_n_tuples(list(vertex_group), 3), strict=True
        ):
            vect1 = v2 - v1
            vect2 = v3 - v2
            unit_vect1 = normalize(vect1)
            unit_vect2 = normalize(vect2)
            angle = angle_between_vectors(vect1, vect2)
            angle *= np.sign(current_radius)
            cut_off_length = current_radius * np.tan(angle / 2)
            max_cut_off = min(np.linalg.norm(vect1), np.linalg.norm(vect2)) / 2
            cut_off_length = np.clip(cut_off_length, -max_cut_off, max_cut_off)
            sign = np.sign(np.cross(vect1, vect2)[2])
            arc = ArcBetweenPoints(
                v2 - unit_vect1 * cut_off_length,
                v2 + unit_vect2 * cut_off_length,
                angle=sign * angle,
                num_components=components_per_rounded_corner,
            )
            arcs.append(arc)
        average_arc_length = 1.0
        if evenly_distribute_anchors:
            nonzero_length_arcs = [arc for arc in arcs if len(arc.points) > 4]
            if len(nonzero_length_arcs) > 0:
                total_arc_length = sum(
                    [arc.get_arc_length() for arc in nonzero_length_arcs]
                )
                num_curves = (
                    sum([len(arc.points) for arc in nonzero_length_arcs]) / 4
                )
                average_arc_length = total_arc_length / num_curves
        arcs = [arcs[-1], *arcs[:-1]]

        for arc1, arc2 in adjacent_pairs(arcs):
            new_points.append(arc1.points)
            line = Line(arc1.get_end(), arc2.get_start())
            if evenly_distribute_anchors:
                line.insert_n_curves(ceil(line.get_length() / average_arc_length))
            new_points.append(line.points)
    self.set_points(np.concatenate(new_points) if new_points else np.array([]))
    return self
````

## Triangle

**Code**

```python
import manimgx as m

class TriangleExample(m.Scene):
    def construct(self) -> None:
        triangles = m.VGroup(
            m.Triangle(),
            m.Triangle(radius=2, color=m.YELLOW, fill_opacity=0.5),
            m.Triangle(radius=2, start_angle=-m.PI / 2, color=m.GREEN),
        ).arrange(buff=1)
        self.add(triangles)
```

An equilateral triangle, pointing up, its vertices on a circle of radius 1 unless given another; blue unless styled.

```python
m.Triangle(**kwargs)
```

It also takes the `RegularPolygon` keywords.

## Square

**Code**

```python
import manimgx as m

class SquareExample(m.Scene):
    def construct(self) -> None:
        squares = m.VGroup(
            m.Square(),
            m.Square(3, color=m.BLUE, fill_opacity=0.5),
            m.Square(4, color=m.YELLOW, grid_xstep=1, grid_ystep=1),
        ).arrange(buff=1)
        self.add(squares)
```

A square, 2 on a side unless sized, centered at the origin; white unless styled.

```python
m.Square(side_length=2.0, **kwargs)
```

**`side_length`**

The length of its sides, in scene units.

**`grid_xstep`**

The distance between the vertical lines of its grid, from its left edge, in scene units (default None: no vertical lines).

**`grid_ystep`**

The distance between the horizontal lines of its grid, from its top edge, in scene units (default None: no horizontal lines).

**`mark_paths_closed`**

Accepted for Manim compatibility; ignored.

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

### side\_length

The length of the square's sides, in scene units: the distance between its first two vertices. Set it to scale the square to that side, about its center.

```python
square.side_length
```

## Rectangle

**Code**

```python
import manimgx as m

class RectangleExample(m.Scene):
    def construct(self) -> None:
        grid = m.Rectangle(
            m.YELLOW, height=3, width=4, grid_xstep=1, grid_ystep=0.5
        )
        rectangles = m.VGroup(
            m.Rectangle(),
            m.Rectangle(m.BLUE, height=4, width=1.5, fill_opacity=0.5),
            grid,
        ).arrange(buff=1)
        self.add(rectangles)
```

A rectangle, 4 wide and 2 tall unless sized, centered at the origin; white unless styled.

Its vertices run counterclockwise from its top right corner. With `grid_xstep` or `grid_ystep` it is ruled into a grid: lines across it, its grid\_lines, in its `color`.

```python
m.Rectangle(color=None, height=2.0, width=4.0, grid_xstep=None, grid_ystep=None, mark_paths_closed=False, **kwargs)
```

**`color`**

Its color, which may be given by position (`Rectangle(BLUE)`); None for white.

**`height`**

Its height, in scene units.

**`width`**

Its width, in scene units.

**`grid_xstep`**

The distance between the vertical lines of its grid, from its left edge, in scene units; None for none.

**`grid_ystep`**

The distance between the horizontal lines of its grid, from its top edge, in scene units; None for none.

**`mark_paths_closed`**

Accepted for Manim compatibility; ignored.

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

### grid\_lines

The lines of its grid: a group of the vertical lines, then one of the horizontal lines, those it has; a submobject, unless it is empty (without a grid).

## RoundedRectangle

**Code**

```python
import manimgx as m

class RoundedRectangleExample(m.Scene):
    def construct(self) -> None:
        leaf = m.RoundedRectangle([0, 1.2, 0, 1.2], height=3, width=3)
        rectangles = m.VGroup(
            m.RoundedRectangle(),
            m.RoundedRectangle(1.5, height=4, width=4, color=m.BLUE),
            leaf.set_color(m.YELLOW),
        ).arrange(buff=1)
        self.add(rectangles)
```

A rectangle with rounded corners, 4 wide and 2 tall unless sized; white unless styled.

```python
m.RoundedRectangle(corner_radius=0.5, **kwargs)
```

**`corner_radius`**

The radius of its corners, in scene units; or a list of radii for its top left, bottom left, bottom right and top right corners, in that order, repeated if there are one or two (see round\_corners).

It also takes the `Rectangle` keywords.

## RegularPolygon

**Code**

```python
import manimgx as m

class RegularPolygonExample(m.Scene):
    def construct(self) -> None:
        polygons = m.VGroup(
            m.RegularPolygon(radius=1.5),
            m.RegularPolygon(radius=1.5, start_angle=m.PI / 6, color=m.GREEN),
            m.RegularPolygon(5, radius=1.5, color=m.YELLOW),
            m.RegularPolygon(10, radius=1.5, color=m.RED),
        ).arrange(buff=0.5)
        self.add(polygons)
```

A regular polygon: `n` vertices evenly spaced on a circle, joined in turn; blue unless styled.

```python
m.RegularPolygon(n=6, **kwargs)
```

**`n`**

How many vertices, and sides, it has.

**`radius`**

The radius of the circle its vertices are on, in scene units (default 1).

**`start_angle`**

The angle of its first vertex, in radians, counterclockwise from the positive x-axis (default None: a vertex straight up if their number is odd, to the right if it is even).

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

## RegularPolygram

**Code**

```python
import manimgx as m

class RegularPolygramExample(m.Scene):
    def construct(self) -> None:
        polygrams = m.VGroup(
            m.RegularPolygram(5, radius=2),
            m.RegularPolygram(7, density=3, radius=2, color=m.YELLOW),
            m.RegularPolygram(6, radius=2, color=m.GREEN),
        ).arrange(buff=1)
        self.play(m.Create(polygrams, run_time=3))
```

A regular star polygon: points evenly spaced on a circle, each joined to the one `density` steps on; blue unless styled.

With a density of 1 it is a regular polygon; five points at density 2 make a pentagram. When the number of points and the density share a factor, the points make that many polygrams, each turned from the last: six points at density 2 make two triangles, a hexagram.

```python
m.RegularPolygram(num_vertices, *, density=2, radius=1, start_angle=None, **kwargs)
```

**`num_vertices`**

How many points there are on the circle.

**`density`**

How many steps on each point is joined to: 1 for a polygon.

**`radius`**

The radius of the circle, in scene units.

**`start_angle`**

The angle of the first point, in radians, counterclockwise from the positive x-axis; None for a point straight up if each polygram has an odd number of points, to the right if even.

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

## Star

**Code**

```python
import manimgx as m

class StarExample(m.Scene):
    def construct(self) -> None:
        stars = m.VGroup(
            m.Star(outer_radius=1.5),
            m.Star(7, outer_radius=1.5, color=m.YELLOW),
            m.Star(7, outer_radius=1.5, density=3, color=m.RED),
            m.Star(12, outer_radius=1.5, inner_radius=1, color=m.GREEN),
        ).arrange(buff=0.5)
        self.play(m.Create(stars, run_time=3))
```

A star: `n` points on a circle, and between each two a vertex on a smaller circle; blue unless styled.

Unless given, the inner radius is the one that makes the star the outline of the RegularPolygram of its `n` points at `density`: its edges lie along the polygram's lines.

```python
m.Star(n=5, *, outer_radius=1, inner_radius=None, density=2, start_angle=TAU / 4, **kwargs)
```

**`n`**

How many points it has.

**`outer_radius`**

The radius of the circle its points are on, in scene units.

**`inner_radius`**

The radius of the circle its inner vertices are on, in scene units; None to set it by `density`.

**`density`**

Without `inner_radius`, the density of the polygram whose outline it is: the higher, the thinner its points. It must be above 0 and below `n / 2`.

**`start_angle`**

The angle of its first point, in radians, counterclockwise from the positive x-axis (default a quarter turn: straight up); None for a point straight up if `n` is odd, to the right if even.

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

## ArcPolygon

**Code**

```python
import manimgx as m

class ArcPolygonExample(m.Scene):
    def construct(self) -> None:
        a, b, c = [0, 0, 0], [2.5, 0, 0], [0, 2.5, 0]
        sides = [{"radius": 2, "color": m.RED}, {"angle": 0}, {"angle": 1}]
        shapes = m.VGroup(
            m.ArcPolygon(a, b, c),
            m.ArcPolygon(a, b, c, radius=2, fill_opacity=0.5).set_color(m.BLUE),
            m.ArcPolygon(a, b, c, angle=-m.PI / 3).set_color(m.GREEN),
            m.ArcPolygon(a, b, c, arc_config=sides),
        ).arrange(buff=0.6)
        self.play(m.Create(shapes, run_time=4))
```

A polygon whose sides are arcs: an ArcBetweenPoints from each vertex to the next, and from the last back to the first; white unless styled.

Going around the vertices counterclockwise, arcs of a positive angle bulge out, and arcs of a negative one bend in. Its outline runs along the arcs, and is filled and stroked in its style. The arcs are also its submobjects, its arcs, drawn over its outline in their own style (white unless `arc_config` styles them): to color the whole, style them too, as a family method such as set\_color does.

```python
m.ArcPolygon(*vertices, angle=PI / 4, radius=None, arc_config=None, **kwargs)
```

**`*vertices`**

The vertices, in order around it.

**`angle`**

The angle every arc turns through, in radians, unless `radius` or `arc_config` is given.

**`radius`**

The radius of every arc, in scene units, in place of `angle`, unless `arc_config` is given; None (or 0) to use `angle`.

**`arc_config`**

The arcs' ArcBetweenPoints keywords, in place of `angle` and `radius`: one set for every arc, or a list of one per side, the first vertex's side first.

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

### arcs

The arcs, one per side, the first vertex's side first; they are also its submobjects.

## ArcPolygonFromArcs

**Code**

```python
import manimgx as m

class ArcPolygonFromArcsExample(m.Scene):
    def construct(self) -> None:
        a, b, c = [-5.5, -1.3, 0], [-2.5, -1.3, 0], [-4, 1.3, 0]
        pairs = (a, b), (b, c), (c, a)
        sides = [m.ArcBetweenPoints(p, q, radius=3) for p, q in pairs]
        reuleaux = m.ArcPolygonFromArcs(*sides, fill_opacity=0.5)
        left = m.Arc(start_angle=m.PI / 2, angle=m.PI).shift(1.5 * m.RIGHT)
        right = m.Arc(start_angle=-m.PI / 2, angle=m.PI).shift(4.5 * m.RIGHT)
        stadium = m.ArcPolygonFromArcs(left, right, fill_opacity=0.5)
        reuleaux.set_color(m.BLUE)
        stadium.set_color(m.GREEN)
        self.play(m.Create(reuleaux), m.Create(stadium))
```

A closed shape made of arcs: each arc in turn, joined to the next by a straight line where they do not meet, and the last to the first; white unless styled.

Its outline is filled and stroked in its style. The arcs are also its submobjects, its arcs, drawn over its outline in their own style: to color the whole, style them too, as a family method such as set\_color does.

```python
m.ArcPolygonFromArcs(*arcs, **kwargs)
```

**`*arcs`**

The arcs, in order around it: Arcs, or ArcBetweenPoints.

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

### arcs

The arcs, in order; they are also its submobjects.

## The screen's shape

### ScreenRectangle

**Code**

```python
import manimgx as m

class ScreenRectangleExample(m.Scene):
    def construct(self) -> None:
        screens = m.VGroup(
            m.ScreenRectangle(),
            m.ScreenRectangle(aspect_ratio=4 / 3, height=3, color=m.BLUE),
        ).arrange(buff=1)
        self.add(screens)
```

A rectangle with a screen's proportions, 16:9 and 4 tall unless given others, centered at the origin; white unless styled.

```python
m.ScreenRectangle(aspect_ratio=16.0 / 9.0, height=4, **kwargs)
```

**`aspect_ratio`**

Its width over its height.

**`height`**

Its height, in scene units.

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

#### aspect\_ratio

The rectangle's width over its height. Set it to stretch the rectangle's width to that proportion, about its center; its height stays.

```python
screen_rectangle.aspect_ratio
```

### FullScreenRectangle

**Code**

```python
import manimgx as m

class FullScreenRectangleExample(m.Scene):
    def construct(self) -> None:
        backdrop = m.FullScreenRectangle(
            fill_color=m.DARK_BLUE, fill_opacity=1, stroke_color=m.YELLOW
        )
        self.add(backdrop, m.Text("A backdrop", font_size=96))
```

A screen rectangle as tall as the frame, centered at the origin: with the 16:9 proportions it has unless given others, the frame's own outline; white unless styled.

Its height is the frame's (8 units unless configured otherwise), whatever `height` is given.

```python
m.FullScreenRectangle(**kwargs)
```

It also takes the `ScreenRectangle` keywords.
