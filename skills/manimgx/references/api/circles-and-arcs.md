# Circles and arcs

**The film's code**

```python
import manimgx as m

class CirclesAndArcs(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            m.Circle(color=m.BLUE),
            m.Dot(radius=0.3, color=m.YELLOW),
            m.Ellipse(width=2.6, height=1.4, color=m.GREEN),
            m.Arc(radius=1, start_angle=0, angle=3 * m.PI / 2, color=m.RED),
            m.Annulus(inner_radius=0.5, outer_radius=1, color=m.TEAL),
            m.Sector(radius=1.1, angle=2 * m.PI / 3, color=m.GOLD),
        )
        names = ["Circle", "Dot", "Ellipse", "Arc", "Annulus", "Sector"]
        cells = m.VGroup()
        for shape, name in zip(shapes, names, strict=True):
            label = m.Text(name, font="monospace", font_size=30)
            cells.add(m.VGroup(shape, label.next_to(shape, m.DOWN, buff=0.4)))
        cells.arrange_in_grid(rows=2, buff=(1.2, 0.8))
        self.play(m.LaggedStart(*[m.Create(cell[0]) for cell in cells], lag_ratio=0.15))
        self.play(m.FadeIn(m.VGroup(*[cell[1] for cell in cells])))
        self.wait()
```

A circle is an arc that goes all the way around. An arc is a part of a circle: from a start angle, counterclockwise through an angle. A dot is a small filled circle, to mark a point. A ring is the region between two circles, and a slice of it, or of a disc, is a sector.

Arcs end in tips as lines do: see [Lines and arrows](<https://manimgx.academa.ai/reference/mobjects/shapes/lines-and-arrows/#tips>).

## Circle

**Code**

```python
import manimgx as m

class CircleExample(m.Scene):
    def construct(self) -> None:
        circles = m.VGroup(
            m.Circle(color=m.BLUE),
            m.Circle(radius=1.5, color=m.GREEN, fill_opacity=0.5),
            m.Circle(radius=2, color=m.YELLOW, stroke_width=12),
        ).arrange(buff=1)
        self.play(m.Create(circles))
```

A circle: drawn counterclockwise from its rightmost point, red unless styled.

```python
m.Circle(radius=None, color=None, *, num_components=9, arc_center=ORIGIN, **kwargs)
```

**`radius`**

The radius, in scene units; None for 1.

**`color`**

The color, which may be given by position (`Circle(1, BLUE)`); None for red.

**`num_components`**

How many anchor points it is drawn through: the circle is one fewer cubic Bézier arcs.

**`arc_center`**

Where its center goes.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

It also takes the tip keywords.

### surround

**Code**

```python
import manimgx as m

class CircleSurroundExample(m.Scene):
    def construct(self) -> None:
        word = m.Text("manimgx", font_size=120)
        ring = m.Circle(color=m.YELLOW).surround(word)
        self.add(word)
        self.play(m.Create(ring))
```

Fit the circle around a mobject: through the corners of its bounding box, enlarged by `buffer_factor`, then `buff` farther out.

```python
circle.surround(mobject, dim_to_match=0, stretch=False, buff=0, *, buffer_factor=1.2)
```

**`mobject`**

The mobject to surround.

**`dim_to_match`**

The dimension (0, 1 or 2) of `mobject` the circle is first fitted to, before it grows to the corners.

**`stretch`**

Whether that first fit stretches the circle into an ellipse matching the bounding box.

**`buff`**

How much farther out the circle goes, in scene units.

**`buffer_factor`**

How much larger than through the corners the circle is.

        import manimgx as m

        class CircleSurroundExample(m.Scene):
            def construct(self) -> None:
                word = m.Text("manimgx", font_size=120)
                ring = m.Circle(color=m.YELLOW).surround(word)
                self.add(word)
                self.play(m.Create(ring))
        ```
    """
    self.replace(mobject, dim_to_match, stretch)
    self.width = np.sqrt(mobject.width**2 + mobject.height**2)
    self.scale(buffer_factor)
    return self.scale((self.width / 2 + buff) / (self.width / 2)) if buff else self
````

### point\_at\_angle

The point of the circle at an angle from its start, its rightmost point.

```python
circle.point_at_angle(angle)
```

**`angle`**

The angle, in radians, counterclockwise; any angle wraps around.

Returns The point, in scene coordinates.

### from\_three\_points

The circle through three points.

```python
Circle.from_three_points(p1, p2, p3, **kwargs)
```

**`p1`**

A point on the circle.

**`p2`**

A second point on it.

**`p3`**

A third point on it, not on the line through the other two.

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

It also takes the tip keywords.

Returns A new circle.

## Dot

**Code**

```python
import manimgx as m

class DotExample(m.Scene):
    def construct(self) -> None:
        self.add(
            m.Dot([-5, 0, 0]),
            m.Dot([-3.5, 0, 0], radius=0.2, color=m.BLUE),
            m.Dot([-1, 0, 0], radius=0.6, color=m.YELLOW),
            m.Dot([3, 0, 0], radius=1.5, color=m.GREEN, fill_opacity=0.5),
        )
```

A dot: a small filled disc, white and without an outline unless styled.

```python
m.Dot(point=ORIGIN, radius=DEFAULT_DOT_RADIUS, **kwargs)
```

**`point`**

Where its center goes.

**`radius`**

Its radius, in scene units (default 0.08).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

It also takes the tip keywords.

## Ellipse

**Code**

```python
import manimgx as m

class EllipseExample(m.Scene):
    def construct(self) -> None:
        ellipses = m.VGroup(
            m.Ellipse(),
            m.Ellipse(width=2, height=4, color=m.BLUE),
            m.Ellipse(width=5, height=2, color=m.YELLOW, fill_opacity=0.5),
        ).arrange(buff=1)
        self.add(ellipses)
```

An ellipse: a circle stretched to a width and a height, red unless styled.

Like a circle, it is drawn counterclockwise from its rightmost point.

```python
m.Ellipse(width=2, height=1, **kwargs)
```

**`width`**

Its width, in scene units: its extent along x.

**`height`**

Its height, in scene units: its extent along y.

**`num_components`**

How many anchor points the arc is drawn through: it is one fewer cubic Bézier curves (default 9).

**`arc_center`**

Where the center of the arc's circle goes, in scene coordinates (default ORIGIN).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

## Arc

**Code**

```python
import manimgx as m

class ArcExample(m.Scene):
    def construct(self) -> None:
        arcs = m.VGroup(
            m.Arc(radius=1.5, angle=m.PI, color=m.BLUE),
            m.Arc(radius=1.5, start_angle=m.PI / 2, angle=3 * m.PI / 2),
            m.Arc(radius=1.5, angle=-m.PI / 2, color=m.YELLOW),
        ).arrange(buff=1.5)
        labels = ("angle=PI", "start_angle=PI/2\nangle=3*PI/2", "angle=-PI/2")
        for arc, label in zip(arcs, labels):
            self.add(m.Text(label, font_size=28).next_to(arc, m.DOWN))
        self.play(m.Create(arcs, run_time=3))
```

An arc of a circle: from the angle `start_angle` through `angle`, counterclockwise if `angle` is positive; white unless styled.

Angles are in radians, about the arc's center, counterclockwise from the positive x-axis. The arc is drawn through `num_components` points spaced evenly along it, joined by cubic Bézier curves.

```python
m.Arc(radius=1.0, start_angle=0, angle=TAU / 4, num_components=9, arc_center=ORIGIN, **kwargs)
```

**`radius`**

The radius, in scene units; None for 1.

**`start_angle`**

The angle of the arc's first point.

**`angle`**

How far the arc goes: counterclockwise if positive, clockwise if negative; TAU for a whole circle.

**`num_components`**

How many anchor points it is drawn through: the arc is one fewer cubic Bézier curves.

**`arc_center`**

Where the center of its circle goes.

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

It also takes the tip keywords.

### get\_arc\_center

The center of the arc's circle, where it is now, in whatever plane it lies: the center of the circle through its first curve's ends and middle.

If there is none (a straight path), it is the origin, with a warning.

```python
arc.get_arc_center(warning=True)
```

**`warning`**

Whether to warn when the center cannot be found.

Returns The point, in scene coordinates.

### move\_arc\_center\_to

Move the arc so the center of its circle is at a point.

```python
arc.move_arc_center_to(point)
```

**`point`**

Where the center goes, in scene coordinates.

### stop\_angle

The angle at which the arc ends: the angle of its last point about its center.

```python
arc.stop_angle()
```

Returns The angle, in radians, counterclockwise from the positive x-axis, from 0 up to TAU.

## ArcBetweenPoints

**Code**

```python
import manimgx as m

class ArcBetweenPointsExample(m.Scene):
    def construct(self) -> None:
        start, end = 3 * m.LEFT + m.DOWN, 3 * m.RIGHT + m.DOWN
        arcs = m.VGroup(
            m.ArcBetweenPoints(start, end, color=m.BLUE),
            m.ArcBetweenPoints(start, end, radius=-4, color=m.GREEN),
            m.ArcBetweenPoints(start, end, angle=-m.PI, color=m.YELLOW),
        )
        self.add(m.Dot(start, radius=0.12), m.Dot(end, radius=0.12))
        self.play(m.Create(arcs, run_time=3))
```

An arc from one point to another, through an angle or of a radius; white unless styled.

Going from `start` to `end`, a positive angle turns counterclockwise, bending the arc to the right of the straight way; a negative angle bends it to the left, and 0 makes it a straight segment.

```python
m.ArcBetweenPoints(start, end, angle=TAU / 4, radius=None, **kwargs)
```

**`start`**

Where the arc starts.

**`end`**

Where it ends.

**`angle`**

The angle it turns through on its way, in radians.

**`radius`**

The radius of its circle, in scene units, in place of `angle`: the shorter arc of that radius, bending right, or left if negative. It must be at least half the distance between the ends. None to use `angle`.

**`num_components`**

How many anchor points the arc is drawn through: it is one fewer cubic Bézier curves (default 9).

**`arc_center`**

Where the center of the arc's circle goes, in scene coordinates (default ORIGIN).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

## Annulus

**Code**

```python
import manimgx as m

class AnnulusExample(m.Scene):
    def construct(self) -> None:
        rings = m.VGroup(
            m.Annulus(),
            m.Annulus(inner_radius=1.5, outer_radius=2, color=m.BLUE),
            m.Annulus(inner_radius=0.5, outer_radius=1.5, color=m.YELLOW),
        ).arrange(buff=1)
        self.add(rings)
```

A ring: the region between two circles of one center; white and filled, without an outline, unless styled.

The inner circle runs clockwise, the other way around from the outer one, so it is a hole in the fill.

```python
m.Annulus(inner_radius=1, outer_radius=2, mark_paths_closed=False, **kwargs)
```

**`inner_radius`**

The inner circle's radius, in scene units.

**`outer_radius`**

The outer circle's radius, in scene units.

**`mark_paths_closed`**

Accepted for Manim compatibility; ignored.

**`num_components`**

How many anchor points the arc is drawn through: it is one fewer cubic Bézier curves (default 9).

**`arc_center`**

Where the center of the arc's circle goes, in scene coordinates (default ORIGIN).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

## AnnularSector

**Code**

```python
import manimgx as m

class AnnularSectorExample(m.Scene):
    def construct(self) -> None:
        sectors = m.VGroup(
            m.AnnularSector(),
            m.AnnularSector(1.5, 2, angle=m.PI, color=m.BLUE),
            m.AnnularSector(
                0.5, 2, angle=-3 * m.PI / 2, start_angle=m.PI, color=m.YELLOW
            ),
        ).arrange(buff=1)
        self.add(sectors)
```

A sector of a ring: the region between two arcs of one center, over one angle; white and filled, without an outline, unless styled.

```python
m.AnnularSector(inner_radius=1, outer_radius=2, angle=TAU / 4, start_angle=0, **kwargs)
```

**`inner_radius`**

The inner arc's radius, in scene units.

**`outer_radius`**

The outer arc's radius, in scene units.

**`angle`**

The angle it spans, in radians: counterclockwise from `start_angle`, or clockwise if negative.

**`start_angle`**

The angle of its first edge, in radians, counterclockwise from the positive x-axis.

**`num_components`**

How many anchor points the arc is drawn through: it is one fewer cubic Bézier curves (default 9).

**`arc_center`**

Where the center of the arc's circle goes, in scene coordinates (default ORIGIN).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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

## Sector

**Code**

```python
import manimgx as m

class SectorExample(m.Scene):
    def construct(self) -> None:
        sectors = m.VGroup(
            m.Sector(radius=2),
            m.Sector(radius=2, angle=m.PI / 3, start_angle=m.PI, color=m.BLUE),
            m.Sector(radius=2, angle=-5 * m.PI / 3, color=m.YELLOW),
        ).arrange(buff=1)
        self.add(sectors)
```

A sector of a disc, a slice of pie: the region between two radii and the arc joining them; white and filled, without an outline, unless styled.

```python
m.Sector(radius=1, **kwargs)
```

**`radius`**

Its radius, in scene units.

**`angle`**

The angle the sector spans, in radians: counterclockwise from `start_angle`, or clockwise if negative (default TAU / 4: a quarter turn).

**`start_angle`**

The angle of its first edge, in radians, counterclockwise from the positive x-axis (default 0).

**`num_components`**

How many anchor points the arc is drawn through: it is one fewer cubic Bézier curves (default 9).

**`arc_center`**

Where the center of the arc's circle goes, in scene coordinates (default ORIGIN).

**`color`**

The color of both fill and stroke (default white; a Circle's is red); None for the class's default.

**`tip_length`**

The length of the tips add\_tip makes, in scene units (default 0.35; an Arrow's may be shorter).

**`normal_vector`**

The normal of the plane the path lies in (default OUT). Accepted for Manim compatibility; ignored and not retained.

**`tip_style`**

Style keywords for the tips the path makes (default None: none). A tip's `fill_color` and `stroke_color` are the path's color unless given here.

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
