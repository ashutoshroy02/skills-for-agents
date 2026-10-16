# Transforms

**The film's code**

```python
import manimgx as m

class TransformsHero(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5).shift(3 * m.LEFT)
        circle = m.Circle(color=m.PINK, fill_opacity=0.5).shift(3 * m.LEFT)
        star = m.Star(color=m.YELLOW, fill_opacity=0.5).shift(3 * m.RIGHT)
        self.play(m.Create(square))
        self.play(m.ReplacementTransform(square, circle))
        self.play(m.TransformFromCopy(circle, star, path_arc=m.PI / 2))
        self.play(m.Swap(circle, star))
        self.wait()
```

A transform turns one mobject into another: its points travel to the other's, and its style blends into the other's. ReplacementTransform then puts the other mobject in its place, so that you go on with the new one; Transform keeps the first mobject, now in the other's shape. To turn a formula into another, part by part, match their parts: TransformMatchingTex.

Each point travels on a straight line unless you give an arc: `path_arc=m.PI` sends each point around half a circle. A path function chooses any other way.

## Transform

**Code**

```python
import manimgx as m

class TransformExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=3, color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(radius=1.5, color=m.YELLOW, fill_opacity=0.5)
        square.shift(3 * m.LEFT)
        circle.shift(3 * m.RIGHT)
        self.add(square)
        self.play(m.Transform(square, circle, path_arc=m.PI / 2, run_time=2))
```

Transform a mobject into the shape and style of another.

The mobject stays in the scene and ends looking like `target_mobject`, which is not added (with `ReplacementTransform`, the target takes the mobject's place). Their parts are matched up one to one (the side with fewer parts gains some, and so do the points of each pair), so the mobject may end with more parts than it had. Each point travels from its start to its end in a straight line, or along an arc with `path_arc`.

Transforms that begin together on one mobject compose: `square.animate.shift(RIGHT)` and `Rotate(square)` played together move the square and turn it. One that begins later takes the mobject over from where the others have brought it. A target that has updaters and is not in the scene moves while the animation plays (the animation runs its updaters), and the mobject follows it.

```python
m.Transform(mobject, target_mobject=None, path_func=None, path_arc=0, path_arc_axis=OUT, path_arc_centers=None, replace_mobject_with_target_in_scene=False, *, keys=None, **kwargs)
```

**`mobject`**

The mobject to transform.

**`target_mobject`**

The mobject it turns into; None creates an empty target when `keys` is omitted. Passing only `keys` leaves `target_mobject` as None.

**`path_func`**

How each point travels from its start to its end: a function of the start points, the end points and the progress (see paths); it replaces `path_arc` and `path_arc_centers`. None: a straight path.

**`path_arc`**

The angle each point turns through on its way, in radians: 0 is a straight path, and a positive angle turns counterclockwise.

**`path_arc_axis`**

The axis the arcs of `path_arc` turn about.

**`path_arc_centers`**

A point the mobject turns about by `path_arc` on its way, or one for each of its points; None: each point turns about the center of its own arc.

**`replace_mobject_with_target_in_scene`**

Whether an independent target takes the mobject's place when the animation finishes. Presets without such a target retain their usual removal or restoration behavior.

**`keys`**

Two or more states to pass through, in order: None for the mobject as the animation starts, a function of it, or a mobject, copied when the animation starts. Without them, the states are the mobject and `target_mobject`.

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

It also takes the animation keywords.

### path\_arc

The angle each point turns through on its way, in radians.

Setting it makes the path an arc of that angle about `path_arc_axis`.

```python
transform.path_arc
```

### path\_func

How each point travels from its start to its end.

A function of the start points, the end points and the progress; setting None keeps the current one.

```python
transform.path_func
```

## ReplacementTransform

**Code**

```python
import manimgx as m

class ReplacementTransformExample(m.Scene):
    def construct(self) -> None:
        numbers = m.VGroup(*(m.MathTex(n, font_size=144) for n in "123"))
        numbers.arrange(buff=3)
        self.add(numbers[0])
        self.play(m.ReplacementTransform(numbers[0], numbers[1]))
        self.play(m.ReplacementTransform(numbers[1], numbers[2]))
```

Transform a mobject into another, which then takes its place in the scene.

It plays as `Transform` does; when it finishes, `target_mobject` is in the scene where the mobject was, and the mobject is not: go on animating the target.

```python
m.ReplacementTransform(mobject, target_mobject, **kwargs)
```

**`mobject`**

The mobject to transform; it leaves the scene.

**`target_mobject`**

The mobject it turns into, which takes its place.

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

## TransformFromCopy

**Code**

```python
import manimgx as m

class TransformFromCopyExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2.5, color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(radius=1.25, color=m.YELLOW, fill_opacity=0.5)
        square.shift(3 * m.LEFT)
        circle.shift(3 * m.RIGHT)
        self.add(square)
        self.play(m.TransformFromCopy(square, circle, run_time=2))
```

Transform a copy of a mobject into another, leaving the mobject where it is.

`target_mobject` joins the scene, starting as a copy of the mobject and turning into itself; the mobject stays as it is.

```python
m.TransformFromCopy(mobject, target_mobject, **kwargs)
```

**`mobject`**

The mobject the copy is made from.

**`target_mobject`**

The mobject the copy turns into; it joins the scene.

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

## ClockwiseTransform

**Code**

```python
import manimgx as m

class ClockwiseTransformExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(2.5 * m.LEFT, radius=0.3, color=m.YELLOW)
        square = m.Square(side_length=1.5, color=m.BLUE, fill_opacity=0.5)
        square.shift(2.5 * m.RIGHT)
        self.add(dot)
        self.play(m.ClockwiseTransform(dot, square, run_time=2))
```

Transform a mobject into another along clockwise half circles.

Each point travels from its start to its end clockwise along a half circle: a `Transform` whose `path_arc` is −π, unless given another.

```python
m.ClockwiseTransform(mobject, target_mobject, **kwargs)
```

**`mobject`**

The mobject to transform.

**`target_mobject`**

The mobject whose shape and style it takes.

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

## CounterclockwiseTransform

**Code**

```python
import manimgx as m

class CounterclockwiseTransformExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=1.5, color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(radius=0.75, color=m.YELLOW, fill_opacity=0.5)
        square.shift(2.5 * m.RIGHT)
        circle.shift(2.5 * m.LEFT)
        self.add(square)
        self.play(m.CounterclockwiseTransform(square, circle, run_time=2))
```

Transform a mobject into another along counterclockwise half circles.

Each point travels from its start to its end counterclockwise along a half circle: a `Transform` whose `path_arc` is π, unless given another.

```python
m.CounterclockwiseTransform(mobject, target_mobject, **kwargs)
```

**`mobject`**

The mobject to transform.

**`target_mobject`**

The mobject whose shape and style it takes.

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

## FadeTransform

**Code**

```python
import manimgx as m

class FadeTransformExample(m.Scene):
    def construct(self) -> None:
        rectangle = m.Rectangle(
            width=4, height=1.5, color=m.BLUE, fill_opacity=0.5
        ).shift(3 * m.LEFT)
        circle = m.Circle(radius=1.5, color=m.YELLOW, fill_opacity=0.5)
        circle.shift(3 * m.RIGHT)
        self.add(rectangle)
        self.play(m.FadeTransform(rectangle, circle, run_time=2))
```

Cross-fade a mobject into another, each moving onto the other's place and size.

The mobject fades out as it moves and stretches onto `target_mobject`, and the target fades in from the mobject's place and size. When it finishes, the target is in the scene and the mobject is not (it is back as it was when the animation was made).

```python
m.FadeTransform(mobject, target_mobject, stretch=True, dim_to_match=1, **kwargs)
```

**`mobject`**

The mobject to fade out.

**`target_mobject`**

The mobject to fade in; it joins the scene.

**`stretch`**

Whether each is stretched to the other's width and height; if not, it is scaled evenly to match the dimension `dim_to_match`.

**`dim_to_match`**

The dimension matched when not stretching: 0 the width, 1 the height.

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

## FadeTransformPieces

**Code**

```python
import manimgx as m

class FadeTransformPiecesExample(m.Scene):
    def construct(self) -> None:
        source = m.VGroup(m.Square(), m.Circle().shift(m.LEFT + m.UP))
        target = m.VGroup(m.Circle(), m.Triangle().shift(m.RIGHT + m.DOWN))
        source.set_color(m.BLUE).shift(3 * m.LEFT)
        target.set_color(m.YELLOW).shift(3 * m.RIGHT)
        self.add(source)
        self.play(m.FadeTransformPieces(source, target, run_time=2))
```

Cross-fade a mobject into another, part by part.

The parts of the two are matched up, and each part cross-fades onto its match as `FadeTransform` does for a whole.

```python
m.FadeTransformPieces(mobject, target_mobject, stretch=True, dim_to_match=1, **kwargs)
```

**`mobject`**

The mobject to fade out.

**`target_mobject`**

The mobject to fade in; it joins the scene.

**`stretch`**

Whether each part is stretched to its match's width and height; if not, it is scaled evenly to match the dimension `dim_to_match`.

**`dim_to_match`**

The dimension matched when not stretching: 0 the width, 1 the height.

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

## Match the parts

### TransformMatchingTex

**Code**

```python
import manimgx as m

class TransformMatchingTexExample(m.Scene):
    def construct(self) -> None:
        before = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=120)
        after = m.MathTex("a^2", "=", "c^2", "-", "b^2", font_size=120)
        self.add(before)
        self.play(
            m.TransformMatchingTex(before, after, path_arc=m.PI / 2), run_time=2
        )
        self.wait(0.5)
```

Transform a formula into another by matching their parts: each part moves to a part written the same way, and the others fade.

The parts of a `MathTex` are the strings it is made of: the arguments it is given and what `{{…}}` sets apart in them, split further at its `substrings_to_isolate` and at the strings of its `tex_to_color_map` (a group's parts are its members'). Two parts match when their strings are the same, so give each term that should travel as an argument of its own. When the animation finishes, `target_mobject` is in the scene in the place of `mobject`.

```python
m.TransformMatchingTex(mobject, target_mobject, transform_mismatches=False, fade_transform_mismatches=False, key_map=None, **kwargs)
```

**`mobject`**

The formula to transform: a `MathTex`, or a group of them.

**`target_mobject`**

The formula it becomes.

**`transform_mismatches`**

Whether the unmatched parts transform into the target's unmatched parts, rather than fade.

**`fade_transform_mismatches`**

Whether they cross-fade into the target's unmatched parts (see `FadeTransformPieces`), rather than fade.

**`key_map`**

Pairs of strings to match although they differ: the parts of `mobject` written the first way cross-fade into the target's parts written the second. These matches take precedence over equal keys.

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

### TransformMatchingShapes

**Code**

```python
import manimgx as m

class TransformMatchingShapesExample(m.Scene):
    def construct(self) -> None:
        source = m.Text("the morse code", font_size=96)
        target = m.Text("here come dots", font_size=96, color=m.YELLOW)
        self.add(source)
        self.play(
            m.TransformMatchingShapes(source, target, path_arc=m.PI / 2),
            run_time=2,
        )
        self.wait(0.5)
```

Transform a mobject into another by matching their shapes: each part moves to a part of the same shape, and the others fade.

The parts are the members with points (the letters of a text); two match when they have the same shape, whatever their size and place (their points, centered and scaled to a height of 1, agree to 3 decimals). So a text becomes its anagram letter by letter. When the animation finishes, `target_mobject` is in the scene in the place of `mobject`.

```python
m.TransformMatchingShapes(mobject, target_mobject, transform_mismatches=False, fade_transform_mismatches=False, key_map=None, **kwargs)
```

**`mobject`**

The mobject to transform.

**`target_mobject`**

The mobject it becomes.

**`transform_mismatches`**

Whether the unmatched parts transform into the target's unmatched parts, rather than fade.

**`fade_transform_mismatches`**

Whether they cross-fade into the target's unmatched parts (see `FadeTransformPieces`), rather than fade.

**`key_map`**

Pairs of keys to match although they differ: the parts of `mobject` with the first key cross-fade into the target's parts with the second. These matches take precedence over equal keys.

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

## Trade places

### Swap

**Code**

```python
import manimgx as m

class SwapExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(side_length=2, color=m.BLUE, fill_opacity=1)
        circle = m.Circle(color=m.RED, fill_opacity=1)
        square.shift(2 * m.LEFT)
        circle.shift(2 * m.RIGHT)
        self.add(square, circle)
        self.play(m.Swap(square, circle))
```

Swap the places of two mobjects, each along an arc.

The same as `CyclicReplace`, which with two mobjects moves each to the other's place.

```python
m.Swap(*mobjects, **kwargs)
```

**`*mobjects`**

The two mobjects.

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

### CyclicReplace

**Code**

```python
import manimgx as m

class CyclicReplaceExample(m.Scene):
    def construct(self) -> None:
        shapes = m.VGroup(
            m.Square(color=m.BLUE),
            m.Circle(color=m.YELLOW),
            m.Triangle(color=m.GREEN),
            m.Star(color=m.RED),
        ).arrange(buff=1)
        self.add(shapes)
        self.play(m.CyclicReplace(*shapes))
        self.play(m.CyclicReplace(*shapes))
```

Move each mobject to the place of the next one, and the last to the first's.

Each travels along an arc, of 90° by default (`path_arc`). A group given alone is taken as the mobjects.

```python
m.CyclicReplace(*mobjects, **kwargs)
```

**`*mobjects`**

The mobjects, in the order of the cycle.

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

## The transform keywords

### TransformOptions

The options a transform takes, by keyword: the animation options and its path.

**`path_func`**

How each point travels from its start to its end: a function of the start points, the end points and the progress (see paths); it replaces `path_arc` and `path_arc_centers` (default None: a straight path).

**`path_arc`**

The angle each point turns through on its way, in radians: 0 is a straight path, and a positive angle turns counterclockwise about `path_arc_axis` (default 0).

**`path_arc_axis`**

The axis the arcs of `path_arc` turn about (default `OUT`: in the plane of the screen).

**`path_arc_centers`**

A point the mobject turns about by `path_arc` on its way, or one for each of its points (default None: each point turns about the center of its own arc).

**`replace_mobject_with_target_in_scene`**

Whether the target takes the mobject's place in the scene when the animation finishes, as with `ReplacementTransform` (default False).

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

#### path\_func

How each point travels from its start to its end: a function of the start points, the end points and the progress (see paths); it replaces `path_arc` and `path_arc_centers` (default None: a straight path).

#### path\_arc

The angle each point turns through on its way, in radians: 0 is a straight path, and a positive angle turns counterclockwise about `path_arc_axis` (default 0).

#### path\_arc\_axis

The axis the arcs of `path_arc` turn about (default `OUT`: in the plane of the screen).

#### path\_arc\_centers

A point the mobject turns about by `path_arc` on its way, or one for each of its points (default None: each point turns about the center of its own arc).

#### replace\_mobject\_with\_target\_in\_scene

Whether the target takes the mobject's place in the scene when the animation finishes, as with `ReplacementTransform` (default False).

## Paths

A path function says how each point travels from where it starts to where it ends: give one as `path_func`.

### straight\_path

The straight path: each point goes along the line from its start to its end, as a transform moves points by default.

```python
m.straight_path()
```

### path\_along\_arc

A path along arcs: each point travels along a circular arc from its start to its end, turning through an angle, as a transform's `path_arc` makes it move.

```python
m.path_along_arc(arc_angle, axis=_PATH_AXIS)
```

**`arc_angle`**

The angle each arc turns through, in radians, counterclockwise about `axis`; smaller in size than STRAIGHT\_PATH\_THRESHOLD, the straight path.

**`axis`**

The axis the arcs turn about.

### clockwise\_path

A path along half circles, clockwise: each point turns through π on its way from its start to its end.

```python
m.clockwise_path()
```

### counterclockwise\_path

A path along half circles, counterclockwise: each point turns through π on its way from its start to its end.

```python
m.counterclockwise_path()
```

### spiral\_path

A spiral path: each point spirals out from its start to its end, its offset from its start growing as it turns counterclockwise through `angle` (for a positive angle) into line with its end.

```python
m.spiral_path(angle, axis=_PATH_AXIS)
```

**`angle`**

How far each point turns, in radians, about `axis`; smaller in size than STRAIGHT\_PATH\_THRESHOLD, the straight path.

**`axis`**

The axis the points turn about.

### path\_along\_circles

A path about centers: each point turns about its center through an angle while it moves from its start to its end, as a transform's `path_arc_centers` makes it move.

With one center, the shape turns about it as a whole, as a Path; with a center per point, each point turns about its own, as a plain function of `(start, end, alpha)`.

```python
m.path_along_circles(arc_angle, centers, axis=_PATH_AXIS)
```

**`arc_angle`**

The angle, in radians, counterclockwise about `axis`.

**`centers`**

One center, or one per point, in scene coordinates.

**`axis`**

The axis the points turn about.

### Path

How the points of a shape travel in a transform, from where they start to where they end, as a value.

A path takes each point to Lₛ·start + Lₑ·end + k, where Lₛ, Lₑ and k depend on the animation's progress α alone: so a shape moves without its points being touched. Call it as `path(start, end, alpha)`, on arrays of points; the functions below make the paths ManimGX provides.

```python
m.Path(kind='motion', angle=0.0, axis=(lambda: copy())(), steps=())
```

**`kind`**

What the path is. "motion": the shape is carried by the motion G of its `steps` while it changes along straight lines in the moving frame, G(α)·((1 − α)·start + α·G(1)⁻¹·end); with no steps, the straight path. "arc": each point travels along a circular arc from its start to its end, turning through `angle` (and at a steady rate along `axis`, if its ends differ along it). "spiral": each point spirals out from its start to its end, start + α·R((α − 1)·`angle`)·(end − start).

**`angle`**

The angle an "arc" or "spiral" path turns through, in radians, counterclockwise about `axis`.

**`axis`**

The axis the path turns about.

**`steps`**

The steps of a "motion" path, taken in order: each a move (a vector), a move along a curve, or a turn about a pivot.

### m.STRAIGHT\_PATH\_THRESHOLD

The smallest angle, in radians, path\_along\_arc and spiral\_path turn through: with less, they are the straight path.
