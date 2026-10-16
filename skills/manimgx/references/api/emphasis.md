# Emphasis

**The film's code**

```python
import manimgx as m

class EmphasisHero(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=96)
        self.add(formula)
        self.play(m.Indicate(formula[0]))
        self.play(m.Circumscribe(formula[2], color=m.YELLOW))
        self.play(m.Flash(formula[4], color=m.YELLOW, flash_radius=0.8))
        self.play(m.Wiggle(formula))
        self.wait()
```

These animations change a mobject for a moment and give it back as it was: they point a viewer's eye at it while the voice talks about it.

## Indicate

**Code**

```python
import manimgx as m

class IndicateExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=144)
        self.add(formula)
        self.play(m.Indicate(formula[4]))
```

Draw attention to a mobject: enlarge and color it for a moment.

It grows to `scale_factor` times its size in `color`, and comes back as it was (eased by `there_and_back`).

```python
m.Indicate(mobject, scale_factor=1.2, color=PURE_YELLOW, **kwargs)
```

**`mobject`**

The mobject to indicate.

**`scale_factor`**

How many times its size it grows to.

**`color`**

The color it turns.

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

## Circumscribe

**Code**

```python
import manimgx as m

class CircumscribeExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Circumscribe", font_size=96)
        self.add(text)
        self.play(m.Circumscribe(text))
        self.play(m.Circumscribe(text, m.Circle, fade_out=True))
```

Draw attention to a mobject with a frame drawn around it.

The frame, a rectangle or a circle `buff` away from the mobject, flashes around it (`ShowPassingFlash`); with `fade_in` it fades in and is then undrawn, with `fade_out` it is drawn and then fades out, and with both it fades in and out. It is gone when the animation finishes. `run_time` times the frame (1 second by default); the other options apply to the whole.

```python
m.Circumscribe(mobject, shape=None, fade_in=False, fade_out=False, time_width=0.3, buff=SMALL_BUFF, color=PURE_YELLOW, stroke_width=DEFAULT_STROKE_WIDTH, **kwargs)
```

**`mobject`**

The mobject to frame.

**`shape`**

The frame's kind: `Rectangle` (None, the default) or `Circle`; any other raises a ValueError.

**`fade_in`**

Whether the frame fades in.

**`fade_out`**

Whether the frame fades out.

**`time_width`**

The flashing stretch's length, as a fraction of the frame's, when it neither fades in nor out.

**`buff`**

The gap between the mobject and the frame, in scene units.

**`color`**

The frame's color.

**`stroke_width`**

The frame's width, in hundredths of a scene unit.

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

## Flash

**Code**

```python
import manimgx as m

class FlashExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=2, color=m.BLUE, fill_opacity=0.5)
        self.add(circle)
        self.play(
            m.Flash(
                circle,
                line_length=1,
                num_lines=24,
                flash_radius=2.2,
                time_width=0.3,
                run_time=2,
            )
        )
```

Flash lines out from a point, like a burst of light.

`num_lines` lines, `line_length` long and starting `flash_radius` from the point, shoot outward as passing flashes (`ShowPassingFlash`), and are gone when the animation finishes. The animation options go to each line's flash.

```python
m.Flash(point, line_length=0.2, num_lines=12, flash_radius=0.1, line_stroke_width=3, color=PURE_YELLOW, time_width=1, **kwargs)
```

**`point`**

The point to flash from, or a mobject whose center to flash from.

**`line_length`**

Each line's length, in scene units.

**`num_lines`**

How many lines.

**`flash_radius`**

How far from the point the lines start, in scene units.

**`line_stroke_width`**

The lines' width, in hundredths of a scene unit.

**`color`**

The lines' color.

**`time_width`**

Each line's flash window, as a fraction of its length.

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

## FocusOn

**Code**

```python
import manimgx as m

class FocusOnExample(m.Scene):
    def construct(self) -> None:
        dot = m.Dot(2 * m.DOWN, radius=0.2, color=m.YELLOW)
        self.add(m.Text("Focus on the dot below", font_size=60), dot)
        self.play(m.FocusOn(dot))
```

Close a spotlight in on a point.

A transparent disc covering the frame shrinks onto `focus_point`, turning `color` at `opacity` as it closes, and is gone when the animation finishes; it follows a mobject that moves. It runs 2 seconds.

```python
m.FocusOn(focus_point, opacity=0.2, color=GREY, **kwargs)
```

**`focus_point`**

The point to focus on, or a mobject whose center to focus on.

**`opacity`**

The disc's opacity at the end.

**`color`**

The disc's color.

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

## Wiggle

**Code**

```python
import manimgx as m

class WiggleExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Wiggle", font_size=144)
        self.add(text)
        self.play(m.Wiggle(text))
```

Wiggle a mobject: rock it back and forth while it swells and shrinks back.

It grows to `scale_value` times its size and back, while turning back and forth by up to `rotation_angle`, `n_wiggles` swings in all, about its center or the given points. It runs 2 seconds.

```python
m.Wiggle(mobject, scale_value=1.1, rotation_angle=0.01 * TAU, n_wiggles=6, scale_about_point=None, rotate_about_point=None, **kwargs)
```

**`mobject`**

The mobject to wiggle.

**`scale_value`**

How many times its size it grows to, halfway through.

**`rotation_angle`**

How far it turns each way at most, in radians.

**`n_wiggles`**

How many swings it makes.

**`scale_about_point`**

The point it grows about; None for its center.

**`rotate_about_point`**

The point it turns about; None for its center.

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

## ShowPassingFlash

**Code**

```python
import manimgx as m

class ShowPassingFlashExample(m.Scene):
    def construct(self) -> None:
        pentagon = m.RegularPolygon(5, color=m.GREY, stroke_width=8).scale(3)
        flash = pentagon.copy().set_color(m.YELLOW)
        self.add(pentagon)
        self.play(m.ShowPassingFlash(flash, time_width=0.5, run_time=2))
```

Flash a stretch of a mobject's path along it, from its start to past its end.

A window, `time_width` of the path's length, travels along the mobject, which shows only what lies inside it. The mobject joins the scene for the flash and leaves it at the end, even if it was there before (flash a copy to keep the original); its paths are whole again afterward.

```python
m.ShowPassingFlash(mobject, time_width=0.1, **kwargs)
```

**`mobject`**

The mobject whose paths the window travels along.

**`time_width`**

The window's length, as a fraction of the path's length.

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

## ShowPassingFlashWithThinningStrokeWidth

**Code**

```python
import manimgx as m

class ShowPassingFlashWithThinningStrokeWidthExample(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=2.5, color=m.YELLOW, stroke_width=16)
        self.add(circle.copy().set_stroke(m.GREY, width=4))
        self.play(
            m.ShowPassingFlashWithThinningStrokeWidth(
                circle, time_width=0.5, run_time=2
            )
        )
```

Flash a stretch of a mobject's path along it, with a tail that thins behind it.

`n_segments` passing flashes (`ShowPassingFlash`) of copies of the mobject play together: their widths rise from none to the mobject's stroke width as their windows shrink from `time_width` to none, so the flash is widest at its head. The copies are gone when the animation finishes, and the mobject itself is left as it is. The animation options go to each flash.

```python
m.ShowPassingFlashWithThinningStrokeWidth(vmobject, n_segments=10, time_width=0.1, **kwargs)
```

**`vmobject`**

The mobject whose paths the flash travels along.

**`n_segments`**

How many flashes make it up.

**`time_width`**

The tail's length, as a fraction of the path's length.

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

## Blink

**Code**

```python
import manimgx as m

class BlinkExample(m.Scene):
    def construct(self) -> None:
        text = m.Text("Blinking", font_size=120)
        self.add(text)
        self.play(m.Blink(text, blinks=3))
```

Blink a mobject: hide it and show it again, a number of times.

It shows for `time_on` seconds and hides for `time_off`, `blinks` times, then shows again for `time_on` (or stays hidden, with `hide_at_end`). It is made fully opaque to show it, and fully transparent to hide it.

```python
m.Blink(mobject, time_on=0.5, time_off=0.5, blinks=1, hide_at_end=False, **kwargs)
```

**`mobject`**

The mobject to blink.

**`time_on`**

How long it shows each time, in seconds.

**`time_off`**

How long it hides each time, in seconds.

**`blinks`**

How many times it blinks.

**`hide_at_end`**

Whether it stays hidden at the end.

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

## Broadcast

**Code**

```python
import manimgx as m

class BroadcastExample(m.Scene):
    def construct(self) -> None:
        self.add(m.Dot(radius=0.2, color=m.TEAL))
        self.play(m.Broadcast(m.Circle(radius=3.5, color=m.TEAL)))
```

Send copies of a mobject spreading out from a point, one after another.

Each of `n_mobs` copies starts at `focal_point`, `initial_width` wide and at `initial_opacity`, and grows like a ripple to the mobject's size, centered on `focal_point`, as its opacity goes to `final_opacity`. They begin one after another (`lag_ratio` 0.2, over 3 seconds), and leave the scene when the animation finishes, unless given `remover=False`. The copies of a filled mobject fade as a whole, those of an outline in their stroke. The mobject itself is not shown.

```python
m.Broadcast(mobject, focal_point=ORIGIN, n_mobs=5, initial_opacity=1, final_opacity=0, initial_width=0.0, **kwargs)
```

**`mobject`**

The ripples' shape, at its largest.

**`focal_point`**

Where the ripples spread from.

**`n_mobs`**

How many copies.

**`initial_opacity`**

The copies' opacity at the start.

**`final_opacity`**

The copies' opacity at the end.

**`initial_width`**

The copies' width at the start, in scene units.

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
