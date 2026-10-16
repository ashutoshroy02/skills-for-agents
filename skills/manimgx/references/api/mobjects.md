# Mobjects

**The film's code**

```python
import manimgx as m

class MobjectsHero(m.Scene):
    def construct(self) -> None:
        def curve(x: float) -> float:
            return 0.5 * x**2

        axes = m.Axes(x_range=[-2, 2, 1], y_range=[0, 2, 1], x_length=3.2, y_length=2.2)
        graph = axes.plot(curve, color=m.BLUE)
        kinds = m.VGroup(
            m.Square(color=m.BLUE, fill_opacity=0.5),
            m.Star(color=m.YELLOW, fill_opacity=0.5),
            m.Arrow(m.LEFT, m.RIGHT, color=m.GREEN),
            m.Text("Text", font_size=64),
            m.MathTex(r"e^{i\pi} + 1 = 0", font_size=56),
            m.VGroup(axes, graph),
        )
        kinds.arrange_in_grid(rows=2, buff=(1.2, 1))
        self.play(
            m.LaggedStart(
                *[m.FadeIn(kind, shift=0.3 * m.UP) for kind in kinds], lag_ratio=0.15
            )
        )
        self.wait()
```

A mobject is anything a video shows: a shape, a text, a formula, a graph. Making a mobject doesn't show it: add it to the scene, or play an animation that brings it in.

Every mobject has three things:

- **Points**, which give its place and its shape. They are in units: the frame's short side is 8 units, and its center is the point `[0, 0, 0]`.
- **A style**: the color and opacity of its stroke and of its fill.
- **Parts**, which are mobjects too: a group's members, a formula's terms, a graph's axes. What you do to a mobject, you do to all its parts.

Every mobject can do what the first pages tell, whatever its kind: be placed, sized and turned, styled, grouped and copied. The pages after them tell each kind of mobject.

## What every mobject can do

- [**Positions**](<https://manimgx.academa.ai/reference/mobjects/positions/index.md>)

  ---

  Points and directions, and the methods that place a mobject: at a point, by another mobject, at the frame's edge.
- [**Size and angle**](<https://manimgx.academa.ai/reference/mobjects/size-and-angle/index.md>)

  ---

  Scale, stretch, turn and flip a mobject, or move every point through a function.
- [**Style**](<https://manimgx.academa.ai/reference/mobjects/style/index.md>)

  ---

  Stroke and fill, color and opacity, gradients, and what covers what.
- [**Colors**](<https://manimgx.academa.ai/reference/mobjects/colors/index.md>)

  ---

  The named colors, and the functions that make, blend and choose colors.
- [**Groups**](<https://manimgx.academa.ai/reference/mobjects/groups/index.md>)

  ---

  Mobjects made of mobjects: add, remove, arrange and sort the parts.
- [**Copies and states**](<https://manimgx.academa.ai/reference/mobjects/copies-and-states/index.md>)

  ---

  Copy a mobject, keep its state to come back to, and prepare a state to move to.
- [**Paths**](<https://manimgx.academa.ai/reference/mobjects/paths/index.md>)

  ---

  The curves a shape is made of: draw a path of your own, and find points along one.

## Kinds of mobjects

- [**Shapes**](<https://manimgx.academa.ai/reference/mobjects/shapes/index.md>)

  ---

  Lines and arrows, circles and arcs, polygons, and shapes made from other shapes.
- [**Annotations**](<https://manimgx.academa.ai/reference/mobjects/annotations/index.md>)

  ---

  Braces, labels, frames, underlines and angle marks: what points at other mobjects.
- [**Text and math**](<https://manimgx.academa.ai/reference/mobjects/text-and-math/index.md>)

  ---

  Words, formulas and numbers, set by Typst inside ManimGX.
- [**Graphs**](<https://manimgx.academa.ai/reference/mobjects/graphs/index.md>)

  ---

  Axes, number lines and planes, the graphs of functions and data, vector fields.
- [**Networks**](<https://manimgx.academa.ai/reference/mobjects/networks/index.md>)

  ---

  Vertices joined by edges, laid out for you, which grow and change.
- [**Matrices and tables**](<https://manimgx.academa.ai/reference/mobjects/matrices-and-tables/index.md>)

  ---

  Entries in rows and columns, between brackets or between lines.
- [**Images and SVG**](<https://manimgx.academa.ai/reference/mobjects/images-and-svg/index.md>)

  ---

  Pictures from files or pixels, and drawings read from SVG files.
- [**Point clouds**](<https://manimgx.academa.ai/reference/mobjects/point-clouds/index.md>)

  ---

  Mobjects drawn as points, each a dot of its own color.

## The mobject

### Mobject

The object everything in a scene is made of: shapes, text, groups, trackers.

A mobject has points in scene coordinates (x to the right, y up, z out of the screen; the frame is 8 units on its short side, about 14.2 × 8 at 16:9, centered on the origin); submobjects, a tree drawn and moved with it; a style: its fill, its stroke and their colors; updaters, which change it as time passes; and a z-index, its place in the drawing order. You make one through its subclasses — `Circle`, `Text`, `VGroup` and the rest — and they all share the methods here: to transform it (`shift`, `scale`, `rotate`), lay it out (`next_to`, `arrange`), style it (`set_color`), keep it updated (`add_updater`), and animate any of that (`animate`).

A transformation or a style acts on the mobject's whole family — the mobject, its submobjects, theirs, and so on — and returns the mobject, so calls chain: `Square().scale(2).set_color(BLUE)`. Size and layout go by the mobject's bounding box: the smallest box, aligned with the axes, around what it draws.

```python
m.Mobject(**kwargs)
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

#### submobjects

The mobject's children, in drawing order: each is drawn over those before it, at an equal z-index.

#### name

The mobject's name: its class's name, unless it was made with one.
