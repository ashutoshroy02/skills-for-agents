# Rate functions

**The film's code**

```python
import manimgx as m

class RateFunctionsHero(m.Scene):
    def construct(self) -> None:
        rates = [m.smooth, m.linear, m.rush_into, m.there_and_back, m.ease_out_bounce]
        names = ["smooth", "linear", "rush_into", "there_and_back", "ease_out_bounce"]
        rows = m.VGroup()
        for name in names:
            label = m.Text(name, font="monospace", font_size=28)
            dot = m.Dot(radius=0.14, color=m.YELLOW)
            rows.add(m.VGroup(label, dot))
        rows.arrange(m.DOWN, buff=0.5)
        for row in rows:
            row[0].move_to([-2.2, row.get_y(), 0], aligned_edge=m.RIGHT)
            row[1].move_to([-1.4, row.get_y(), 0])
        self.add(rows)
        self.play(
            *[
                row[1].animate(rate_func=rate).shift(7 * m.RIGHT)
                for row, rate in zip(rows, rates, strict=True)
            ],
            run_time=3,
        )
        self.wait()
```

An animation runs from 0, its start, to 1, its end. Its rate function says how far along the change is at each moment of that time: `rate_func(t)` for t from 0 to 1. The default, smooth, starts slowly, speeds up and ends slowly; linear keeps one speed. Give another to `play` or to any animation: `self.play(square.animate.shift(m.RIGHT), rate_func=m.rush_into)`.

A rate function may go past 1 and back, for a bounce, or come back to 0, so that the animation ends where it started. Choose one to see it move:

## The usual ones

### smooth

Slow, fast, slow: a sigmoid curve, stretched to run from 0 to 1.

The default rate function of animations.

```python
m.smooth(t, inflection=10.0)
```

**`t`**

The time, from 0 to 1.

**`inflection`**

How steep its middle is: higher starts and ends slower and runs faster between.

Returns The progress, from 0 to 1.

### linear

Progress in step with time: t.

```python
m.linear(t)
```

### rush\_into

The first half of smooth, stretched over the whole time: starts slowly and ends at its greatest speed.

```python
m.rush_into(t, inflection=10.0)
```

**`t`**

The time, from 0 to 1.

**`inflection`**

How steep smooth is.

Returns The progress, from 0 to 1.

### rush\_from

The second half of smooth, stretched over the whole time: starts at its greatest speed and slows toward the end.

```python
m.rush_from(t, inflection=10.0)
```

**`t`**

The time, from 0 to 1.

**`inflection`**

How steep smooth is.

Returns The progress, from 0 to 1.

### slow\_into

√(1 − (1 − t)²), a quarter circle: starts sharply and slows to a stop.

```python
m.slow_into(t)
```

### double\_smooth

Two smooth moves, each half the way in half the time: comes to its slowest speed at the middle.

```python
m.double_smooth(t)
```

### there\_and\_back

There and back: smooth to the end by the middle, then back to the start.

```python
m.there_and_back(t, inflection=10.0)
```

**`t`**

The time, from 0 to 1.

**`inflection`**

How steep smooth is.

Returns The progress, 0 at the start and the end and 1 at the middle.

### there\_and\_back\_with\_pause

There and back with a pause: smooth to the end, a pause there, then back to the start.

```python
m.there_and_back_with_pause(t, pause_ratio=1.0 / 3)
```

**`t`**

The time, from 0 to 1.

**`pause_ratio`**

The fraction of the time spent at the end, in the middle.

Returns The progress, 0 at the start and the end and 1 during the pause.

### running\_start

Backs up for a running start, then runs to the end: with the default pull, back to −0.18 at t ≈ 0.29.

```python
m.running_start(t, pull_factor=-0.5)
```

**`t`**

The time, from 0 to 1.

**`pull_factor`**

How far it pulls back: the third and fourth of its Bézier curve's seven control values (0, 0, pull, pull, 1, 1, 1).

Returns The progress, from 0 to 1, after dipping below 0.

### lingering

Runs evenly to the end by 0.8 of the time, then lingers there.

```python
m.lingering(t)
```

### wiggle

Swings to either side of the start and comes back: sin(`wiggles`·πt), swelling and fading as there\_and\_back does.

With the default 2 wiggles, it swings to 0.73 and then to −0.73.

```python
m.wiggle(t, wiggles=2)
```

**`t`**

The time, from 0 to 1.

**`wiggles`**

How many swings, to one side or the other.

Returns The progress, 0 at the start and the end.

### exponential\_decay

1 − e^(−t / `half_life`), scaled to end at 1: shoots off, then closes in on the end, ever slower.

With the default time constant, it reaches about 1 − 1/e ≈ 0.63 at t = 0.1.

```python
m.exponential_decay(t, half_life=0.1)
```

**`t`**

The time, from 0 to 1.

**`half_life`**

The time constant, as a fraction of the time.

Returns The progress, from 0 to 1.

### smoothstep

3t² − 2t³: starts and ends at rest; gentler than smooth.

```python
m.smoothstep(t)
```

### smootherstep

6t⁵ − 15t⁴ + 10t³: starts and ends at rest, and without acceleration there.

```python
m.smootherstep(t)
```

## Easing curves

The easing curves are the web's: each eases in (starts slowly), eases out (ends slowly), or both, with a curve of its own.

### ease\_in\_back

Pulls back first, to −0.1, then speeds to the end.

```python
m.ease_in_back(t)
```

### ease\_in\_bounce

ease\_out\_bounce turned around: bounces off the start, higher each time (to 0.02, 0.06 and 0.25), then rises to the end.

```python
m.ease_in_bounce(t)
```

### ease\_in\_circ

1 − √(1 − t²), a quarter circle: starts at rest and speeds up sharply.

```python
m.ease_in_circ(t)
```

### ease\_in\_cubic

t³: starts slow and speeds up.

```python
m.ease_in_cubic(t)
```

### ease\_in\_elastic

Swings about the start, more and more widely (down to −0.37), then springs to the end: a sine under the envelope of ease\_in\_expo.

```python
m.ease_in_elastic(t)
```

### ease\_in\_expo

(2^(10t) − 1) / 1023: barely moves at first, then shoots to the end.

```python
m.ease_in_expo(t)
```

### ease\_in\_out\_back

Pulls back to −0.1, then overshoots to 1.1 and settles at the end.

```python
m.ease_in_out_back(t)
```

### ease\_in\_out\_bounce

ease\_in\_bounce up to the middle, then ease\_out\_bounce.

```python
m.ease_in_out_bounce(t)
```

### ease\_in\_out\_circ

ease\_in\_circ up to the middle, then its mirror image.

```python
m.ease_in_out_circ(t)
```

### ease\_in\_out\_cubic

ease\_in\_cubic up to the middle, then its mirror image: slow, fast, slow.

```python
m.ease_in_out_cubic(t)
```

### ease\_in\_out\_elastic

Swings about the start, more and more widely (down to −0.12), springs across the middle, then swings about the end, less and less widely (up to 1.12).

```python
m.ease_in_out_elastic(t)
```

### ease\_in\_out\_expo

ease\_in\_expo up to the middle, then its mirror image.

```python
m.ease_in_out_expo(t)
```

### ease\_in\_out\_quad

ease\_in\_quad up to the middle, then its mirror image: slow, fast, slow.

```python
m.ease_in_out_quad(t)
```

### ease\_in\_out\_quart

ease\_in\_quart up to the middle, then its mirror image: slow, fast, slow.

```python
m.ease_in_out_quart(t)
```

### ease\_in\_out\_quint

ease\_in\_quint up to the middle, then its mirror image: slow, fast, slow.

```python
m.ease_in_out_quint(t)
```

### ease\_in\_out\_sine

(1 − cos(πt))/2: slow, fast, slow.

```python
m.ease_in_out_sine(t)
```

### ease\_in\_quad

t²: starts slow and speeds up.

```python
m.ease_in_quad(t)
```

### ease\_in\_quart

t⁴: starts slow and speeds up.

```python
m.ease_in_quart(t)
```

### ease\_in\_quint

t⁵: starts slow and speeds up.

```python
m.ease_in_quint(t)
```

### ease\_in\_sine

1 − cos(πt/2): starts slow and speeds up.

```python
m.ease_in_sine(t)
```

### ease\_out\_back

Overshoots the end, to 1.1, then settles back to it.

```python
m.ease_out_back(t)
```

### ease\_out\_bounce

Falls to the end and bounces off it like a ball: reaches it at t ≈ 0.36, then bounces back to 0.75, 0.94 and 0.98.

```python
m.ease_out_bounce(t)
```

### ease\_out\_circ

√(1 − (t − 1)²), a quarter circle: starts sharply and comes to rest.

```python
m.ease_out_circ(t)
```

### ease\_out\_cubic

1 − (1 − t)³: starts fast and slows to a stop.

```python
m.ease_out_cubic(t)
```

### ease\_out\_elastic

Springs past the end (to 1.37), then swings about it, less and less widely, like a spring: ease\_in\_elastic turned around.

```python
m.ease_out_elastic(t)
```

### ease\_out\_expo

ease\_in\_expo turned around: shoots off, then creeps to the end.

```python
m.ease_out_expo(t)
```

### ease\_out\_quad

1 − (1 − t)²: starts fast and slows to a stop.

```python
m.ease_out_quad(t)
```

### ease\_out\_quart

1 − (1 − t)⁴: starts fast and slows to a stop.

```python
m.ease_out_quart(t)
```

### ease\_out\_quint

1 − (1 − t)⁵: starts fast and slows to a stop.

```python
m.ease_out_quint(t)
```

### ease\_out\_sine

sin(πt/2): starts fast and slows to a stop.

```python
m.ease_out_sine(t)
```

## Make your own

A rate function is any Python function from a number to a number. These make one from another.

### squish\_rate\_func

Squeeze a rate function into part of the time: it runs between `a` and `b`, and holds its ends before and after.

```python
m.squish_rate_func(func, a=0.4, b=0.6)
```

**`func`**

The rate function.

**`a`**

When it starts, from 0 to 1.

**`b`**

When it ends, from `a` to 1; if it is `a`, the function steps from its start to its end at `a`.

Returns The squeezed rate function.

### not\_quite\_there

Scale a rate function so it goes only part of the way.

```python
m.not_quite_there(func=smooth, proportion=0.7)
```

**`func`**

The rate function.

**`proportion`**

How far it goes: its progress is scaled by this.

Returns The scaled rate function.

### unit\_interval

Make a rate function start exactly at 0 and end exactly at 1, and hold its ends outside \[0, 1\].

```python
m.unit_interval(function)
```

**`function`**

The rate function, as it runs from 0 to 1.

Returns 0 up to 0, 1 from 1 on.

### zero

Make a rate function that comes back to 0 start and end exactly at 0, and hold 0 outside \[0, 1\].

```python
m.zero(function)
```

**`function`**

The rate function, as it runs from 0 to 1.

Returns The rate function, 0 up to 0 and from 1 on.
