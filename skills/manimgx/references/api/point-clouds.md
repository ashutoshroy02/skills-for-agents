# Point clouds

**The film's code**

```python
import manimgx as m
import numpy as np

class PointCloudsHero(m.Scene):
    def construct(self) -> None:
        rng = np.random.default_rng(3)
        angles = rng.uniform(0, 2 * np.pi, 2000)
        radii = 3 * np.sqrt(rng.uniform(0, 1, 2000))
        points = np.stack(
            [radii * np.cos(angles), radii * np.sin(angles), np.zeros(2000)], axis=1
        )
        rgbas = np.array(
            [m.interpolate_color(m.BLUE, m.YELLOW, r / 3).to_rgba() for r in radii]
        )
        cloud = m.PMobject(stroke_width=6).add_points(points, rgbas)
        self.play(m.FadeIn(cloud))
        self.play(m.Rotate(cloud, m.PI / 2), run_time=2)
        self.wait()
```

A point cloud is a mobject drawn as points: each point a dot of its own color, as wide as the cloud's stroke. Clouds suit what is many and small: dust, stars, samples.

## PMobject

**Code**

```python
import numpy as np

import manimgx as m

class PMobjectExample(m.Scene):
    def construct(self) -> None:
        t = np.linspace(0, 1, 300)
        spiral = np.column_stack(
            [3.5 * t * np.cos(20 * t), 3.5 * t * np.sin(20 * t), 0 * t]
        )
        colors = m.color_gradient([m.BLUE, m.GREEN, m.YELLOW], len(t))
        rgbas = np.array([color.to_rgba() for color in colors])
        cloud = m.PMobject(stroke_width=15).add_points(spiral, rgbas=rgbas)
        self.add(cloud)
```

A point cloud: a mobject drawn as points, each a dot of its own color.

Points are added with add\_points, each with a color; the style methods color them all. Each point is a disk as wide as a stroke of its `stroke_width`, a hundredth of a scene unit for each unit of width: at the default width, 4, about 4 pixels of a 720p frame.

```python
m.PMobject(**kwargs)
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

### add\_points

Add points to the cloud, after its own, with their colors.

```python
pmobject.add_points(points, rgbas=None, color=None, alpha=1.0)
```

**`points`**

The points, in scene coordinates: an (n, 3) array.

**`rgbas`**

Their colors, one row of red, green, blue and opacity (from 0 to 1) per point; None to give them all `color`.

**`color`**

Their color, when `rgbas` is None; None for the cloud's (its `color` style keyword, white unless given).

**`alpha`**

Their opacity, from 0 to 1, when `rgbas` is None.

### thin\_out

Keep one point in every `factor` of each cloud in the family, from its first.

```python
pmobject.thin_out(factor=5)
```

**`factor`**

One point is kept in this many; must be positive.

## PointCloudDot

**Code**

```python
import manimgx as m

class PointCloudDotExample(m.Scene):
    def construct(self) -> None:
        clouds = m.Group(
            m.PointCloudDot(),
            m.PointCloudDot(density=5, stroke_width=8, color=m.BLUE),
            m.PointCloudDot(density=15, stroke_width=4, color=m.RED),
        ).arrange(buff=0.6)
        self.add(clouds)
```

A disk of points: rings of points around a center, pure yellow unless styled.

The rings are 1/`density` scene units apart, from that far from the center out to just inside `radius`, and the points along each ring about as far apart. Its points are small: `stroke_width` 2.

```python
m.PointCloudDot(center=ORIGIN, radius=2.0, *, density=DEFAULT_POINT_DENSITY_1D, **kwargs)
```

**`center`**

Where its center is, in scene coordinates.

**`radius`**

How far out its points reach, in scene units.

**`density`**

How many rings, and points along a ring, per scene unit.

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
