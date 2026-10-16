# Copies and states

**The film's code**

```python
import manimgx as m

class CopiesAndStatesHero(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.6)
        self.play(m.Create(square))
        square.save_state()
        copy = square.copy().set_color(m.YELLOW)
        self.play(copy.animate.shift(3 * m.RIGHT))
        target = square.generate_target()
        target.shift(3 * m.LEFT).rotate(m.PI / 4).set_color(m.RED)
        self.play(m.MoveToTarget(square))
        self.play(m.Restore(square))
        self.wait()
```

A mobject is one object in the scene: a variable that names it names that object, and a change to it shows wherever it is. To have two, copy it. To change a mobject and come back, keep its state first. To animate a change into a state that you prepare step by step, make its target.

## copy

A copy of the mobject, with its whole family.

Every mobject its attributes refer to is copied once, so an attribute that refers to one of its members refers to the copy's member. The copy runs the same updater functions, on itself, and is not in the scene. Copying is cheap: the copy shares the original's points and style until either one changes them.

```python
mobject.copy()
```

## Keep a state

### save\_state

**Code**

```python
import manimgx as m

class MobjectSaveStateExample(m.Scene):
    def construct(self) -> None:
        square = m.Square(color=m.BLUE, fill_opacity=0.5)
        square.save_state()
        self.add(square)
        self.play(square.animate.set_color(m.YELLOW).shift(3 * m.LEFT))
        self.play(square.animate.rotate(m.PI / 4).scale(2))
        self.play(m.Restore(square))
```

Keep a copy of the mobject as it is now, to return to with restore or the Restore animation.

The copy is the mobject's `saved_state`; saving again replaces it.

```python
mobject.save_state()
```

        import manimgx as m

        class MobjectSaveStateExample(m.Scene):
            def construct(self) -> None:
                square = m.Square(color=m.BLUE, fill_opacity=0.5)
                square.save_state()
                self.add(square)
                self.play(square.animate.set_color(m.YELLOW).shift(3 * m.LEFT))
                self.play(square.animate.rotate(m.PI / 4).scale(2))
                self.play(m.Restore(square))
        ```
    """
    self.saved_state = None  # not copied into the new saved state
    self.saved_state = self.copy()
    return self
````

### restore

Make the mobject what it was when save\_state last kept it: its points and its style, member by member (see become).

Raises an exception if its state was never saved.

```python
mobject.restore()
```

## Prepare a state

### generate\_target

**Code**

```python
import manimgx as m

class MobjectGenerateTargetExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=1.5, color=m.BLUE).shift(3 * m.LEFT)
        target = circle.generate_target()
        target.set_fill(m.GREEN, opacity=0.5).shift(6 * m.RIGHT + m.UP)
        target.scale(0.5)
        self.add(circle)
        self.play(m.MoveToTarget(circle))
```

Make the mobject's target: a copy of it, which you change into the state MoveToTarget then animates the mobject to.

Using animate makes a new target too, in place of this one.

```python
mobject.generate_target()
```

Returns The target.

        import manimgx as m

        class MobjectGenerateTargetExample(m.Scene):
            def construct(self) -> None:
                circle = m.Circle(radius=1.5, color=m.BLUE).shift(3 * m.LEFT)
                target = circle.generate_target()
                target.set_fill(m.GREEN, opacity=0.5).shift(6 * m.RIGHT + m.UP)
                target.scale(0.5)
                self.add(circle)
                self.play(m.MoveToTarget(circle))
        ```
    """
    self.target = None  # not copied into the new target
    self.target = self.copy()
    return self.target
````

### target

The state MoveToTarget moves the mobject to: made by generate\_target, or given when the mobject was made; None if neither.

## Look like another

### become

**Code**

```python
import manimgx as m

class MobjectBecomeExample(m.Scene):
    def construct(self) -> None:
        shape = m.Circle(radius=2, color=m.RED, fill_opacity=0.8)
        shape.add_updater(lambda mob, dt: mob.rotate(dt))
        self.add(shape)
        self.wait()
        square = m.Square(side_length=4, color=m.BLUE, fill_opacity=0.8)
        shape.become(square)
        self.wait(2)  # the same mobject: its updater still turns it
```

Make the mobject look like another, at once, while staying itself: the same object in the scene, with its updaters.

The two families are first given the same structure; then each member takes its counterpart's points and its colors, opacities, stroke widths, sheen and texture (its joint and cap styles and 3D shading stay its own, unless they are the same). With a `match_*` flag or `stretch`, a copy of `mobject` is first fitted to this mobject.

```python
mobject.become(mobject, match_height=False, match_width=False, match_depth=False, match_center=False, stretch=False)
```

**`mobject`**

The mobject to look like.

**`match_height`**

Whether the copy is first scaled, in proportion, to this mobject's height.

**`match_width`**

Whether it is first scaled to this mobject's width.

**`match_depth`**

Whether it is first scaled to this mobject's depth.

**`match_center`**

Whether it is first moved to this mobject's center.

**`stretch`**

Whether it is first stretched to this mobject's width, height and depth, in place of the `match_*` scalings.

        import manimgx as m

        class MobjectBecomeExample(m.Scene):
            def construct(self) -> None:
                shape = m.Circle(radius=2, color=m.RED, fill_opacity=0.8)
                shape.add_updater(lambda mob, dt: mob.rotate(dt))
                self.add(shape)
                self.wait()
                square = m.Square(side_length=4, color=m.BLUE, fill_opacity=0.8)
                shape.become(square)
                self.wait(2)  # the same mobject: its updater still turns it
        ```
    """
    if stretch or match_height or match_width or match_depth or match_center:
        mobject = mobject.copy()
        for dim, match in ((1, match_height), (0, match_width), (2, match_depth)):
            if stretch or match:
                mobject.rescale_to_fit(self.length_over_dim(dim), dim, stretch)
        if match_center:
            mobject.move_to(self.get_center())
    self.align_data(mobject, skip_point_alignment=True)
    for sm1, sm2 in zip(self.get_family(), mobject.get_family(), strict=True):
        sm1._geometry = sm2._geometry  # immutable: shared, not copied
        sm1._take_shape(sm2)
        a, b = sm1.paint, sm2.paint
        # (the rest — colors, widths, windows, dashes — `mixed` takes from b at 1); a
        # picture is what the mobject shows, so it becomes b's too (a texture is an array
        # or a camera: compared by identity)
        same = (a.joint, a.cap, a.shade_in_3d) == (b.joint, b.cap, b.shade_in_3d)
        sm1.paint = (  # a value: shared, not copied
            b
            if same and a.texture is b.texture
            else a.mixed(a, b, 1).but(texture=b.texture)
        )
    return self
````

### match\_points

Take another mobject's shape: its points, member by member in family order; this mobject's style stays its own.

Members past the end of the shorter family stay as they are.

```python
mobject.match_points(mobject)
```

**`mobject`**

The mobject whose shape to take.
