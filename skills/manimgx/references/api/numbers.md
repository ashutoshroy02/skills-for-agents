# Numbers

**The film's code**

```python
import manimgx as m

class NumbersHero(m.Scene):
    def construct(self) -> None:
        number = m.DecimalNumber(0, num_decimal_places=2, font_size=96, color=m.YELLOW)
        variable = m.Variable(0, m.MathTex("x"), num_decimal_places=2).scale(1.5)
        tracker = variable.tracker
        m.VGroup(number, variable).arrange(m.DOWN, buff=1)

        def follow(mobject: m.DecimalNumber) -> None:
            mobject.set_value(tracker.get_value())

        number.add_updater(follow)
        self.add(number, variable)
        self.play(tracker.animate.set_value(3.14), run_time=2)
        self.wait()
```

A number is a text that knows its value. set\_value shows another value in its place, with the same look, so a number can count while a scene plays: by an [updater](<https://manimgx.academa.ai/reference/updaters/index.md>) that sets it at every frame, or by ChangeDecimalToValue.

## DecimalNumber

**Code**

```python
import manimgx as m

class DecimalNumberExample(m.Scene):
    def construct(self) -> None:
        numbers = m.VGroup(
            m.DecimalNumber(3.14159),
            m.DecimalNumber(1234567.891, num_decimal_places=1),
            m.DecimalNumber(42, include_sign=True, color=m.YELLOW),
            m.DecimalNumber(90, num_decimal_places=0, unit=r"^\circ"),
            m.DecimalNumber(3.14159, num_decimal_places=4, show_ellipsis=True),
        )
        self.add(numbers.arrange(m.DOWN, buff=0.4).scale(1.5))
```

A number, written with a fixed number of decimal places: white and filled unless styled.

Its parts are its characters, in order, each typeset by `mob_class`: the sign, the digits, the commas and the decimal point; then "…" and the unit, if any (and a background rectangle before them all, if asked for). The number shown is rounded (a negative one that rounds to zero loses its sign, in either component of a complex number), and a complex one is written `a+bi`. set\_value shows another number, keeping the font size, the color and the edge `edge_to_fix` where they are: driven by a value tracker, or by ChangeDecimalToValue, the number counts on screen.

A type checker follows the initial value's kind: real by default, complex for a complex initial value. Use `DecimalNumber[complex](0)` to start real and later accept complex values.

```python
m.DecimalNumber(number=0, num_decimal_places=2, mob_class=MathTex, include_sign=False, group_with_commas=True, digit_buff_per_font_unit=0.001, show_ellipsis=False, unit=None, unit_buff_per_font_unit=0, include_background_rectangle=False, edge_to_fix=LEFT, font_size=DEFAULT_FONT_SIZE, **kwargs)
```

**`number`**

The number to show; a complex one too.

**`num_decimal_places`**

How many digits follow the decimal point.

**`mob_class`**

The class each character is typeset with.

**`include_sign`**

Whether a number that is not negative is written with a plus sign.

**`group_with_commas`**

Whether the digits before the decimal point are grouped in threes by commas.

**`digit_buff_per_font_unit`**

The gap between characters, per unit of font size (0.001: 0.048 scene units at 48).

**`show_ellipsis`**

Whether "…" follows the number.

**`unit`**

A unit after the number, in LaTeX math (`"^\circ"`, `r"\text{ m}"`); one that starts with "^" is raised to the number's top.

**`unit_buff_per_font_unit`**

The gap before the unit, beyond the gap between characters, per unit of font size.

**`include_background_rectangle`**

Whether a background rectangle is behind the number.

**`edge_to_fix`**

The edge, as a direction, that stays where it is when a new value changes the number's width.

**`font_size`**

The characters' font size, as `mob_class` measures it.

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

### font\_size

The number's font size: the one it was made with, times how much it has been scaled since. Set it, to a positive size, to scale the number to it.

```python
number.font_size
```

### get\_value

The number shown, as it was given: not rounded.

```python
number.get_value()
```

### increment\_value

Show the number plus `delta_t`.

```python
number.increment_value(delta_t=1)
```

**`delta_t`**

What to add.

### set\_value

**Code**

```python
import manimgx as m

class DecimalNumberSetValueExample(m.Scene):
    def construct(self) -> None:
        tracker = m.ValueTracker(0)
        number = m.DecimalNumber(0, font_size=144).shift(2 * m.LEFT)
        number.add_updater(lambda n: n.set_value(tracker.get_value()))
        self.add(number)
        self.play(tracker.animate.set_value(100), run_time=3)
```

Show another number, keeping the look: the font size, the edge `edge_to_fix` where it is, and the color — every character takes the number's own, so a color given to single characters is not kept.

```python
number.set_value(number)
```

**`number`**

The number to show.

        import manimgx as m

        class DecimalNumberSetValueExample(m.Scene):
            def construct(self) -> None:
                tracker = m.ValueTracker(0)
                number = m.DecimalNumber(0, font_size=144).shift(2 * m.LEFT)
                number.add_updater(lambda n: n.set_value(tracker.get_value()))
                self.add(number)
                self.play(tracker.animate.set_value(100), run_time=3)
        ```
    """
    # every glyph takes the number's own color, as CE's `init_colors` repaints them.
    # A number still as it was left showing the same string is left alone: its
    # members' geometry and paint are values, so "as it was left" is the same objects
    shown = self._get_num_string(number)
    key = self._row_key(shown)
    last = self._shown
    if last is not None and last[0] == key:
        family = self.get_family()
        if len(family) == len(last[1]) and all(
            m is was and m._geometry is g and m.paint is p
            for m, (was, g, p) in zip(family, last[1], strict=True)
        ):
            self.number = number
            return self
    old_font_size = self.font_size
    move_to_point = self.get_critical_point(self.edge_to_fix)
    key = self._set_submobjects_from_number(number)
    self.font_size = old_font_size
    self.move_to(move_to_point, self.edge_to_fix)
    self.init_colors()
    self._shown = (
        key,
        tuple((m, m._geometry, m.paint) for m in self.get_family()),
    )
    return self
````

## Integer

**Code**

```python
import manimgx as m

class IntegerExample(m.Scene):
    def construct(self) -> None:
        count = m.Integer(0, font_size=144).shift(1.5 * m.LEFT)
        self.add(count)
        self.play(m.ChangeDecimalToValue(count, 1000), run_time=3)
```

An integer: a DecimalNumber with no decimal places, white and filled unless styled.

A number with a fractional part is shown rounded, and get\_value rounds it too.

```python
m.Integer(number=0, num_decimal_places=0, **kwargs)
```

**`number`**

The number to show.

**`num_decimal_places`**

How many digits follow the decimal point: none unless given.

It also takes the `DecimalNumber` keywords.

### get\_value

The number shown: the number given, rounded to an integer.

```python
integer.get_value()
```

## Variable

**Code**

```python
import manimgx as m

class VariableExample(m.Scene):
    def construct(self) -> None:
        x = m.Variable(2.0, "x", num_decimal_places=3)
        y = m.Variable(4.0, "x^2", num_decimal_places=3)
        self.add(m.VGroup(x, y).arrange(m.DOWN, buff=0.5).scale(2))
        t = x.tracker
        y.add_updater(lambda v: v.tracker.set_value(t.get_value() ** 2))
        self.play(t.animate.set_value(5), run_time=3, rate_func=m.linear)
```

A named value: a label, "=", and a number that shows a value tracker's value.

Its parts are its label, followed by "=", and its value, a DecimalNumber or an Integer that shows its tracker's value at every frame: animate the tracker, and the number counts.

```python
m.Variable(var, label, var_type=DecimalNumber, num_decimal_places=2, **kwargs)
```

**`var`**

The value it starts with.

**`label`**

The label: a string, typeset as math (MathTex), or a text or math mobject.

**`var_type`**

The number's class: DecimalNumber or a subclass, such as Integer.

**`num_decimal_places`**

How many digits follow the decimal point. Integer classes use their own precision defaults instead.

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

### label

The label, followed by "=", one of its submobjects.

### tracker

The value tracker the number shows: set or animate it to change the number.

### value

The number, which shows the tracker's value at every frame.

## Count to a value

### ChangeDecimalToValue

**Code**

```python
import manimgx as m

class ChangeDecimalToValueExample(m.Scene):
    def construct(self) -> None:
        number = m.DecimalNumber(0, font_size=144)
        self.add(number)
        self.play(m.ChangeDecimalToValue(number, 3.14, run_time=2))
```

Count a number to a value.

It goes from the value it has when the animation is made to `target_number`, eased by the rate function.

```python
m.ChangeDecimalToValue(decimal_mob, target_number, **kwargs)
```

**`decimal_mob`**

The number to change.

**`target_number`**

The value it ends at.

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

### ChangingDecimal

**Code**

```python
import manimgx as m

class ChangingDecimalExample(m.Scene):
    def construct(self) -> None:
        number = m.DecimalNumber(0, font_size=144)
        self.add(number)
        self.play(m.ChangingDecimal(number, lambda a: 100 * a, run_time=3))
```

Change the value a number shows with the animation's progress.

At every frame, the number shows `number_update_func` of the progress, from 0 to 1, eased by the rate function.

```python
m.ChangingDecimal(decimal_mob, number_update_func, **kwargs)
```

**`decimal_mob`**

The number to change.

**`number_update_func`**

A function from the progress to the value to show.

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
