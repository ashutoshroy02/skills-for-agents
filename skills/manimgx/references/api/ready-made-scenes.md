# Ready-made scenes

**The film's code**

```python
import manimgx as m

class ReadyMadeScenesHero(m.LinearTransformationScene):
    def construct(self) -> None:
        self.add_vector([1, 2], color=m.YELLOW)
        self.apply_matrix([[1, 1], [0, 1]])
        self.wait()
```

These scenes come with what one kind of video needs. A vector scene draws vectors from the origin of a plane, with their labels and their coordinates. A linear transformation scene applies a matrix to the plane and to everything on it, in one play. A zoomed scene shows a magnified part of the frame, in an inset.

## VectorScene

**Code**

```python
import manimgx as m

class VectorSceneExample(m.VectorScene):
    def construct(self) -> None:
        self.add_plane()
        vector = self.add_vector([3, 2], color=m.YELLOW)
        self.write_vector_coordinates(vector)
        self.wait()
```

A scene for drawing vectors: arrows from the origin, their labels and their coordinates.

Its methods add a plane and axes, draw vectors and label them, and animate the passage from a vector to its coordinates and back. `add_vector` draws a vector from the origin, in scene units; `get_vector` makes one in the coordinates of the scene's `plane`.

```python
class MyScene(m.VectorScene):
```

**`basis_vector_stroke_width`**

The stroke width of the basis vectors (see `get_basis_vectors`), in hundredths of a scene unit.

### plane

The plane whose coordinates `get_vector` reads: a `LinearTransformationScene` makes it; in a vector scene, assign it (`self.plane = self.add_plane()`).

### grows\_vectors

Whether `add_vector` shows a vector growing unless told otherwise: True in a vector scene, False in a transformation scene.

### add\_plane

Add a number plane to the scene.

```python
self.add_plane(animate=False, **kwargs)
```

**`animate`**

Whether to draw it in (`Create`, its lines overlapping).

It also takes the `NumberPlane` keywords.

Returns The plane. It is not the scene's `plane` unless assigned to it.

### add\_axes

Add axes to the scene, one scene unit to one unit.

```python
self.add_axes(animate=False, color=WHITE)
```

**`animate`**

Whether to draw them in (`Create`).

**`color`**

Their color.

Returns The axes.

### get\_vector

Make an arrow from the origin of the scene's plane to a point given in its coordinates.

```python
self.get_vector(numerical_vector, **kwargs)
```

**`numerical_vector`**

The point's coordinates on `plane`: x and y (a z is ignored).

It also takes the `Arrow` keywords.

Returns A new arrow, not added to the scene.

### add\_vector

Add a vector to the scene: the arrow given, or a Vector from the origin to the coordinates given.

It is shown growing from the origin (GrowArrow) if `animate` says so, or else if the scene's `grows_vectors` does (a vector scene's does, a transformation scene's doesn't); then the scene takes it up: a LinearTransformationScene moves it with the plane.

```python
self.add_vector(vector, color=PURE_YELLOW, animate=None, **kwargs)
```

**`vector`**

An arrow, or the coordinates of a vector's tip, in scene units.

**`color`**

The vector's color, when it is made from coordinates.

**`animate`**

Whether it grows in a play; None for the scene's `grows_vectors`.

It also takes the `Arrow` keywords.

Returns The arrow.

### write\_vector\_coordinates

Write a vector's coordinates beside its tip, as a column (its `coordinate_label`), in a play of `Write`.

```python
self.write_vector_coordinates(vector, **kwargs)
```

It also takes the `Matrix` keywords.

Returns The column.

### get\_basis\_vectors

Make the basis vectors î and ĵ: arrows from the origin to (1, 0) and (0, 1), in scene units.

```python
self.get_basis_vectors(i_hat_color=X_COLOR, j_hat_color=Y_COLOR)
```

**`i_hat_color`**

The color of î.

**`j_hat_color`**

The color of ĵ.

Returns A new group of the two, î first.

### get\_basis\_vector\_labels

Make labels for the basis vectors: î and ĵ, in the colors of the x and y axes (green and red).

```python
self.get_basis_vector_labels(**kwargs)
```

**`at_tip`**

Whether the label goes beyond the vector's tip, rather than beside its middle (default False).

**`direction`**

Which side of the vector the label goes on, looking along the vector (default "left").

**`rotate`**

Whether the label turns with the vector, rather than staying upright (default False).

Returns A new group of the two labels, î's first.

### get\_vector\_label

Make a label for a vector: beside its middle, on its left or its right, or beyond its tip.

A string is typeset as LaTeX, a single letter as a bold vector (`\vec{\textbf{v}}`), in the vector's color. The label gets a background rectangle, to be read over the lines under it.

```python
self.get_vector_label(vector, label, at_tip=False, direction='left', rotate=False, color=None, label_scale_factor=LARGE_BUFF - 0.2)
```

**`vector`**

The vector, from the origin.

**`label`**

The label: a mobject, or LaTeX.

**`at_tip`**

Whether it goes beyond the vector's tip, rather than beside its middle.

**`direction`**

Which side of the vector it goes on, looking along the vector.

**`rotate`**

Whether it turns with the vector, rather than staying upright.

**`color`**

Its color, when it is made from a string; None for the vector's.

**`label_scale_factor`**

How much it is scaled.

Returns The label, not added to the scene.

### label\_vector

Label a vector, and add the label to the scene (see `get_vector_label`).

```python
self.label_vector(vector, label, animate=True, **kwargs)
```

**`vector`**

The vector, from the origin.

**`label`**

The label: a mobject, or LaTeX.

**`animate`**

Whether to write it in (`Write`).

**`color`**

The label's color, when it is made from a string (default None: the vector's).

**`label_scale_factor`**

How much the label is scaled (default 0.8).

**`at_tip`**

Whether the label goes beyond the vector's tip, rather than beside its middle (default False).

**`direction`**

Which side of the vector the label goes on, looking along the vector (default "left").

**`rotate`**

Whether the label turns with the vector, rather than staying upright (default False).

Returns The label.

### vector\_to\_coords

Show how a vector gives its coordinates, in a series of plays.

The vector (drawn first, when it is given by its coordinates) gets a line along x and a line up to its tip, each written with its coordinate; the coordinates then move into a column beside its tip.

```python
self.vector_to_coords(vector, integer_labels=True, clean_up=True)
```

**`vector`**

The vector, from the origin, or its coordinates.

**`integer_labels`**

Whether the coordinates are rounded to integers.

**`clean_up`**

Whether the scene is left holding what it held before, at the end.

Returns The column of coordinates, the line along x and the line up to the tip.

## LinearTransformationScene

**Code**

```python
import manimgx as m

class LinearTransformationSceneExample(m.LinearTransformationScene):
    def __init__(self) -> None:
        super().__init__(show_coordinates=True, leave_ghost_vectors=True)

    def construct(self) -> None:
        self.add_unit_square()
        self.add_vector([-1, 2], color=m.YELLOW)
        self.apply_matrix([[1, 1], [0, 1]])  # a shear
        self.wait()
```

A scene for linear transformations of the plane: a matrix applied to the plane and to everything on it, in one animation.

Before `construct`, it lays a still plane in the background (`background_plane`), a plane over it that the transformations move (`plane`), and the basis vectors î and ĵ (`i_hat` and `j_hat`, together `basis_vectors`). `apply_matrix` then transforms what the scene holds, by kind: the points of the transformable mobjects, as the plane's; the vectors, redrawn to where their tips go; the labels that follow them; and the moving mobjects, moved whole to where their centers go. The background and foreground mobjects stay where they are.

```python
class MyScene(m.LinearTransformationScene):
```

**`include_background_plane`**

Whether a plane stays still in the background.

**`include_foreground_plane`**

Whether a plane over it moves with the transformations: the scene's `plane`.

**`background_plane_kwargs`**

Number plane keywords for the background plane, over its own (grey lines).

**`foreground_plane_kwargs`**

Number plane keywords for the moving plane, over its own (it reaches past the frame, so that the frame stays covered as it moves).

**`show_coordinates`**

Whether the background plane's axes are numbered.

**`show_basis_vectors`**

Whether the basis vectors are drawn; they move with the transformations.

**`basis_vector_stroke_width`**

The basis vectors' stroke width, in hundredths of a scene unit.

**`i_hat_color`**

The color of î.

**`j_hat_color`**

The color of ĵ.

**`leave_ghost_vectors`**

Whether each transformation leaves faded copies of the vectors where they were.

### ghost\_vectors

The faded copies the transformations left of what they moved whole, where it was, with `leave_ghost_vectors`.

### setup

Lay out the planes and the basis vectors, and add them to the scene.

`render` calls it before `construct`; it acts once. A subclass that overrides it calls this one first.

```python
self.setup()
```

### add\_background\_mobject

Add mobjects that the transformations leave where they are, as they leave the background plane.

```python
self.add_background_mobject(*mobjects)
```

### add\_foreground\_mobject

Add mobjects that stay in front: drawn over everything else, and left where they are by the transformations.

```python
self.add_foreground_mobject(*mobjects)
```

### add\_transformable\_mobject

Add mobjects that the transformations move point by point, as they move the plane.

```python
self.add_transformable_mobject(*mobjects)
```

### add\_moving\_mobject

Add a mobject that the transformations move whole, its shape unchanged: to where they take its center.

```python
self.add_moving_mobject(mobject, target_mobject=None)
```

**`target_mobject`**

What it becomes as it moves, placed where the transformation takes its center; None for itself.

### get\_ghost\_vectors

The faded copies the transformations left of what they moved whole, where it was, with `leave_ghost_vectors`.

```python
self.get_ghost_vectors()
```

Returns The group of them.

### get\_unit\_square

Make a rectangle over the plane's unit square: from its origin, one unit of x wide and one unit of y tall.

```python
self.get_unit_square(color=PURE_YELLOW, opacity=0.3, stroke_width=3)
```

**`color`**

The color of its fill and its stroke.

**`opacity`**

Its fill's opacity, from 0 to 1.

**`stroke_width`**

Its stroke's width, in hundredths of a scene unit.

Returns A new rectangle, also kept as the scene's `square`.

### add\_unit\_square

Add the plane's unit square, which the transformations move with the plane: its area shows how they scale areas.

The moving vectors are then brought to the front, over it.

```python
self.add_unit_square(animate=False, **kwargs)
```

**`animate`**

Whether to draw it in: its border, then its fill.

**`color`**

The color of its fill and its stroke (default yellow).

**`opacity`**

Its fill's opacity, from 0 to 1 (default 0.3).

**`stroke_width`**

Its stroke's width, in hundredths of a scene unit (default 3).

### write\_vector\_coordinates

Write a vector's coordinates beside its tip, as a column that stays in front, where it is, through the transformations.

```python
self.write_vector_coordinates(vector, **kwargs)
```

It also takes the `Matrix` keywords.

Returns The column.

### add\_transformable\_label

Label a vector with a label that the transformations carry along and rewrite.

After a transformation, the label sits by the vector where it went, and reads `new_label`, or else the label in the transformation's name: `L(v)` for a label `v`.

```python
self.add_transformable_label(vector, label, transformation_name='L', new_label=None, *, animate=True, **kwargs)
```

**`vector`**

The vector, from the origin.

**`label`**

The label: a mobject, or LaTeX (see `get_vector_label`).

**`transformation_name`**

The name of the transformation.

**`new_label`**

What the label reads after a transformation; None for the transformation's name around it.

**`animate`**

Whether to write it in.

**`color`**

The label's color, when it is made from a string (default None: the vector's).

**`label_scale_factor`**

How much the label is scaled (default 0.8).

**`at_tip`**

Whether the label goes beyond the vector's tip, rather than beside its middle (default False).

**`direction`**

Which side of the vector the label goes on, looking along the vector (default "left").

**`rotate`**

Whether the label turns with the vector, rather than staying upright (default False).

Returns The label.

### add\_title

Add a title at the top of the frame, in front and still, on a background rectangle.

```python
self.add_title(title, scale_factor=1.5, animate=False)
```

**`title`**

The title: a mobject, or text, typeset as `Tex`.

**`scale_factor`**

How much text is scaled.

**`animate`**

Whether to write it in.

### apply\_matrix

Apply a matrix to the plane and to everything on it, in one play.

Everything the transformations move goes where the matrix takes it (see `apply_function`). Unless a `path_arc` is given, the points travel along arcs that turn through the mean of the angles the matrix turns î and ĵ through.

```python
self.apply_matrix(matrix, **kwargs)
```

**`matrix`**

A 2 × 2 matrix, which acts on x and y, or a 3 × 3 one: its columns are where it takes î and ĵ.

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

### apply\_inverse

Apply the inverse of a matrix to the plane and to everything on it: undo `apply_matrix` of the same matrix.

```python
self.apply_inverse(matrix, **kwargs)
```

**`matrix`**

The matrix, 2 × 2 or 3 × 3, which must be invertible.

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

### apply\_transposed\_matrix

Apply a matrix, given by its transpose, to the plane and to everything on it: as `apply_matrix` does.

```python
self.apply_transposed_matrix(transposed_matrix, **kwargs)
```

**`transposed_matrix`**

The matrix's transpose, whose rows are where the matrix takes î and ĵ.

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

### apply\_inverse\_transpose

Apply the inverse of a matrix's transpose to the plane and to everything on it.

```python
self.apply_inverse_transpose(t_matrix, **kwargs)
```

**`t_matrix`**

The matrix, 2 × 2 or 3 × 3, which must be invertible.

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

### apply\_nonlinear\_transformation

Apply a function that need not be linear to the plane and to everything on it.

The plane's lines are first divided into many curves, so that they can bend (see `apply_function`).

```python
self.apply_nonlinear_transformation(function, **kwargs)
```

**`function`**

The function, from a point to its image, in scene coordinates.

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

### apply\_function

Apply a function to the plane and to everything on it, in one play.

Every point of the transformable mobjects goes where `function` takes it; each vector is redrawn to where its tip goes, and its transformable label follows it; each moving mobject moves whole to where its center goes; the foreground mobjects stay where they are. With `leave_ghost_vectors`, faded copies of what moves whole are left behind.

```python
self.apply_function(function, added_anims=None, **kwargs)
```

**`function`**

The function, from a point to its image, in scene coordinates.

**`added_anims`**

Animations to play along.

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

## ZoomedScene

**Code**

```python
import manimgx as m

class ZoomedSceneExample(m.ZoomedScene):
    def construct(self) -> None:
        title = m.Text("manimgx", font_size=120).shift(m.LEFT)
        note = m.Text("exact in time, typed throughout", font_size=14)
        note.next_to(title, m.DOWN)
        self.add(title, note)
        frame = self.zoomed_camera.frame
        frame.move_to(note.get_left())
        self.activate_zooming(animate=True)
        self.play(frame.animate.move_to(note.get_right()), run_time=2)
```

A scene with a second camera, whose picture is shown in the frame: a magnifying glass.

`zoomed_camera` sees what its frame, a small rectangle in the scene (`zoomed_camera.frame`), covers, and `zoomed_display` shows its picture, larger, in a corner of the frame. Both appear with `activate_zooming`; move, scale or animate the zoomed camera's frame to look elsewhere, and the picture follows.

```python
class MyScene(m.ZoomedScene):
```

**`zoomed_display_height`**

The display's height, in scene units.

**`zoomed_display_width`**

The display's width, in scene units.

**`zoomed_display_center`**

Where the display's center is; None for a corner of the frame.

**`zoomed_display_corner`**

Which corner of the frame the display is in, when it has no `zoomed_display_center`: a direction, such as `UR`.

**`zoomed_display_corner_buff`**

The display's distance from the edges at that corner, in scene units.

**`zoomed_camera_config`**

The zoomed camera's look: its frame's outline, and its picture's background.

**`zoomed_camera_image_mobject_config`**

Keywords for the display, the picture of what the zoomed camera sees: its style, and its outline's (`default_display_frame_config`).

**`zoomed_camera_frame_starting_position`**

Where the zoomed camera's frame starts.

**`zoom_factor`**

The size of the zoomed camera's frame, as a fraction of the display's: the display magnifies `1 / zoom_factor` times.

**`image_frame_stroke_width`**

Accepted for Manim compatibility; ignored.

**`zoom_activated`**

Whether zooming is active: `activate_zooming` sets it, and it shows nothing by itself.

### setup

Make the zoomed camera and its display: `render` calls it before `construct`. A subclass that overrides it calls this one first.

```python
self.setup()
```

### activate\_zooming

Show the zoomed camera's frame and its display, in front of everything else.

```python
self.activate_zooming(animate=False)
```

**`animate`**

Whether to animate their coming first, in two plays: the frame shrinks from the whole view to its place (`get_zoom_in_animation`), then the display grows out of it to its own (`get_zoomed_display_pop_out_animation`).

### get\_zoom\_in\_animation

Make the animation in which the zoomed camera's frame shrinks from the whole view to its place.

The frame moves to its start at once: it covers the view, centered on the origin, without its outline, until the animation plays.

```python
self.get_zoom_in_animation(**kwargs)
```

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

Returns The animation, to play.

### get\_zoomed\_display\_pop\_out\_animation

Make the animation in which the display grows out of the zoomed camera's frame to its place.

The display moves to its start at once: over the zoomed camera's frame, until the animation plays.

```python
self.get_zoomed_display_pop_out_animation(**kwargs)
```

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

Returns The animation, to play.

### get\_zoom\_factor

How small the zoomed camera's frame is next to the display.

```python
self.get_zoom_factor()
```

Returns the display magnifies its inverse.

### ZoomedCameraConfig

The zoomed camera's look: its frame's stroke and its picture's background.

**`default_frame_stroke_width`**

The width of the zoomed camera frame's outline, in hundredths of a scene unit (default 2).

**`default_frame_stroke_color`**

The color of the zoomed camera frame's outline (default white).

**`background_opacity`**

The opacity of the zoomed picture's background, from 0 to 1 (default 1: it hides what is behind the display).

#### default\_frame\_stroke\_width

The width of the zoomed camera frame's outline, in hundredths of a scene unit (default 2).

#### default\_frame\_stroke\_color

The color of the zoomed camera frame's outline (default white).

#### background\_opacity

The opacity of the zoomed picture's background, from 0 to 1 (default 1: it hides what is behind the display).
