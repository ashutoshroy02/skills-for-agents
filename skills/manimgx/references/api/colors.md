# Colors

**The film's code**

```python
import manimgx as m

class ColorsHero(m.Scene):
    def construct(self) -> None:
        rows = m.VGroup()
        for family in [
            "BLUE",
            "TEAL",
            "GREEN",
            "YELLOW",
            "GOLD",
            "RED",
            "MAROON",
            "PURPLE",
            "GREY",
        ]:
            row = m.VGroup(m.Text(family, font="monospace", font_size=24))
            for shade in "ABCDE":
                color = m.PALETTE[f"{family}_{shade}"]
                row.add(
                    m.Circle(radius=0.24, color=color, fill_opacity=1, stroke_width=0)
                )
            row.arrange(buff=0.16)
            rows.add(row)
        rows.arrange(m.DOWN, buff=0.16, aligned_edge=m.RIGHT)
        self.play(
            m.LaggedStart(
                *[m.FadeIn(row, shift=0.2 * m.RIGHT) for row in rows], lag_ratio=0.1
            )
        )
        self.wait()
```

A color is a name, such as `m.BLUE`; a hex code, such as `"#58C4DD"`; or numbers of red, green and blue. Each takes the place of the others wherever a color goes: `m.Circle(color="#58C4DD")` is `m.Circle(color=m.BLUE)`.

Most named colors come in a family of five shades, from A, the lightest, to E, the darkest; the family's own name is its C. GRAY and GREY are two spellings of one color.

## The named colors

`WHITE` \#FFFFFF

`GRAY_A``GREY_A` \#DDDDDD

`GRAY_B``GREY_B` \#BBBBBB

`GRAY_C``GREY_C` \#888888

`GRAY_D``GREY_D` \#444444

`GRAY_E``GREY_E` \#222222

`BLACK` \#000000

`LIGHTER_GRAY``LIGHTER_GREY` \#DDDDDD

`LIGHT_GRAY``LIGHT_GREY` \#BBBBBB

`GRAY``GREY` \#888888

`DARK_GRAY``DARK_GREY` \#444444

`DARKER_GRAY``DARKER_GREY` \#222222

`PURE_RED` \#FF0000

`PURE_GREEN` \#00FF00

`PURE_BLUE` \#0000FF

`PURE_CYAN` \#00FFFF

`PURE_MAGENTA` \#FF00FF

`PURE_YELLOW` \#FFFF00

`BLUE_A` \#C7E9F1

`BLUE_B` \#9CDCEB

`BLUE_C` \#58C4DD

`BLUE_D` \#29ABCA

`BLUE_E` \#236B8E

`BLUE` \#58C4DD

`DARK_BLUE` \#236B8E

`TEAL_A` \#ACEAD7

`TEAL_B` \#76DDC0

`TEAL_C` \#5CD0B3

`TEAL_D` \#55C1A7

`TEAL_E` \#49A88F

`TEAL` \#5CD0B3

`GREEN_A` \#C9E2AE

`GREEN_B` \#A6CF8C

`GREEN_C` \#83C167

`GREEN_D` \#77B05D

`GREEN_E` \#699C52

`GREEN` \#83C167

`YELLOW_A` \#FFF1B6

`YELLOW_B` \#FFEA94

`YELLOW_C` \#F7D96F

`YELLOW_D` \#F4D345

`YELLOW_E` \#E8C11C

`YELLOW` \#F7D96F

`GOLD_A` \#F7C797

`GOLD_B` \#F9B775

`GOLD_C` \#F0AC5F

`GOLD_D` \#E1A158

`GOLD_E` \#C78D46

`GOLD` \#F0AC5F

`RED_A` \#F7A1A3

`RED_B` \#FF8080

`RED_C` \#FC6255

`RED_D` \#E65A4C

`RED_E` \#CF5044

`RED` \#FC6255

`MAROON_A` \#ECABC1

`MAROON_B` \#EC92AB

`MAROON_C` \#C55F73

`MAROON_D` \#A24D61

`MAROON_E` \#94424F

`MAROON` \#C55F73

`PURPLE_A` \#CAA3E8

`PURPLE_B` \#B189C6

`PURPLE_C` \#9A72AC

`PURPLE_D` \#715582

`PURPLE_E` \#644172

`PURPLE` \#9A72AC

`PINK` \#D147BD

`LIGHT_PINK` \#DC75CD

`ORANGE` \#FF862F

`LIGHT_BROWN` \#CD853F

`DARK_BROWN` \#8B4513

`GRAY_BROWN``GREY_BROWN` \#736357

`LOGO_WHITE` \#ECE7E2

`LOGO_GREEN` \#87C2A5

`LOGO_BLUE` \#525893

`LOGO_RED` \#E07A5F

`LOGO_BLACK` \#343434

### m.PALETTE

The named colors, by name: `PALETTE["BLUE"]` is `BLUE`. A color's name, in any case, is read as the color.

## Make a color

### ManimColor

**Code**

```python
import manimgx as m

class ManimColorExample(m.Scene):
    def construct(self) -> None:
        colors = [
            m.ManimColor("#58C4DD"),
            m.ManimColor("orange"),
            m.ManimColor((0.9, 0.3, 0.5)),
            m.ManimColor.from_hsv((0.75, 0.6, 0.9)),
            m.RED.lighter(0.4),
            m.RED.darker(0.4),
        ]
        swatches = m.VGroup(
            *(
                m.VGroup(
                    m.Square(side_length=1.6, color=color, fill_opacity=1),
                    m.Text(color, font_size=24),
                ).arrange(m.DOWN)
                for color in colors
            )
        )
        self.add(swatches.arrange(buff=0.4))
```

A color: red, green, blue and opacity, from 0 to 1, which is also its hex string.

As a string it is `"#RRGGBB"`, or `"#RRGGBBAA"` when translucent, so it goes wherever a string does; to\_rgba gives its values. `ManimColor(value, alpha=1.0)` reads `value` as a color, of opacity `alpha` (from 0 to 1) where `value` gives none. `value` is:

- a hex string, `"#FC6255"` or `"0xFC6255"`, of 3, 4, 6 or 8 digits (the fourth of four, and the last two of eight, are the opacity);
- a color's name, in any case: `"BLUE"`, `"blue_c"`;
- an integer, `0xFC6255`;
- three or four numbers, red, green, blue and opacity: from 0 to 1 if all are floats, from 0 to 255 otherwise (`(1.0, 0.5, 0.0)` is orange, `(1, 0.5, 0)` nearly black);
- another color, copied as it is;
- None, for black.

#### to\_rgb

The color's red, green and blue.

```python
color.to_rgb()
```

Returns An array of three floats, from 0 to 1.

#### to\_rgba

The color's red, green, blue and opacity.

```python
color.to_rgba()
```

Returns An array of four floats, from 0 to 1.

#### to\_hex

The color as a hex string, `"#RRGGBB"`, in capitals.

```python
color.to_hex(with_alpha=False)
```

**`with_alpha`**

Whether to add the opacity's two digits: `"#RRGGBBAA"`.

Returns The string.

#### interpolate

The color a fraction of the way from this one to another, mixed as every blend of colors is: in OKLab, where the colors between two are those the eye sees between them.

```python
color.interpolate(other, alpha)
```

**`other`**

The color at 1.

**`alpha`**

How far toward it, from 0 (this color) to 1 (`other`).

Returns A new color.

#### opacity

This color with another opacity.

```python
color.opacity(opacity)
```

**`opacity`**

The opacity, from 0 (transparent) to 1 (opaque).

Returns A new color.

#### lighter

This color mixed toward white, its opacity kept.

```python
color.lighter(blend=0.2)
```

**`blend`**

How far toward white, from 0 (this color) to 1 (white).

Returns A new color.

#### darker

This color mixed toward black, its opacity kept.

```python
color.darker(blend=0.2)
```

**`blend`**

How far toward black, from 0 (this color) to 1 (black).

Returns A new color.

#### from\_hex

The color of a hex string, read as the constructor reads it (`"#RRGGBB"`, `"#RGB"`, with or without opacity digits; a color's name too).

```python
ManimColor.from_hex(hex_str, alpha=1.0)
```

**`hex_str`**

The string.

**`alpha`**

The opacity, from 0 to 1, if the string gives none.

Returns A new color.

#### from\_rgb

The color of a red, green and blue.

```python
ManimColor.from_rgb(rgb, alpha=1.0)
```

**`rgb`**

Red, green and blue, from 0 to 1.

**`alpha`**

The opacity, from 0 to 1.

Returns A new color.

#### from\_rgba

The color of a red, green, blue and opacity.

```python
ManimColor.from_rgba(rgba)
```

**`rgba`**

Red, green, blue and opacity, from 0 to 1.

Returns A new color.

#### from\_hsv

The color of a hue, saturation and value.

```python
ManimColor.from_hsv(hsv, alpha=1.0)
```

**`hsv`**

Hue, saturation and value, each a float from 0 to 1: a hue of 0 (or 1) is red, ⅓ green, ⅔ blue.

**`alpha`**

The opacity, from 0 to 1.

Returns A new color.

#### from\_hsl

The color of a hue, saturation and lightness.

```python
ManimColor.from_hsl(hsl, alpha=1.0)
```

**`hsl`**

Hue, saturation and lightness, each from 0 to 1: a hue of 0 (or 1) is red, ⅓ green, ⅔ blue; a lightness of 0.5 is the full color.

**`alpha`**

The opacity, from 0 to 1.

Returns A new color.

#### to\_hsv

The color's hue, saturation and value.

```python
color.to_hsv()
```

Returns An array of three floats, from 0 to 1.

#### contrasting

A color that stands out against this one, as text on it would: dark on a light color, light on a dark one.

```python
color.contrasting(threshold=0.5, light=None, dark=None)
```

**`threshold`**

The luma (0.30 red + 0.59 green + 0.11 blue), from 0 to 1, above which this color counts as light.

**`light`**

The color for a dark color; None for white.

**`dark`**

The color for a light color; None for black.

Returns `dark` or `light`.

#### invert

The color's complement: each of red, green and blue taken from 1, the opacity kept.

```python
color.invert()
```

Returns A new color.

### HSV

**Code**

```python
import manimgx as m

class HSVExample(m.Scene):
    def construct(self) -> None:
        color = m.HSV((0.0, 0.7, 0.9))
        swatches = m.VGroup()
        for step in range(8):
            color.hue = step / 8
            swatches.add(m.Square(side_length=1.2, color=color, fill_opacity=1))
        self.add(swatches.arrange(buff=0.3))
```

A color made from a hue, saturation and value, which can be read and set.

`HSV(hsv, alpha=1.0)` takes the hue, saturation and value, each from 0 to 1, and the opacity: a fourth number of `hsv`, if given, or else `alpha`, from 0 to 1. Setting hue, saturation or value changes the color, as a value and as its `str`; it still compares equal to (and hashes as) the string it was made as.

#### h

The color's hue, from 0 to 1: 0 (or 1) red, ⅓ green, ⅔ blue. Set it to change the color.

#### hue

The color's hue, from 0 to 1: 0 (or 1) red, ⅓ green, ⅔ blue. Set it to change the color.

#### s

The color's saturation, from 0 (grey) to 1 (the full color). Set it to change the color.

#### saturation

The color's saturation, from 0 (grey) to 1 (the full color). Set it to change the color.

#### v

The color's value, from 0 (black) to 1 (the brightest). Set it to change the color.

#### value

The color's value, from 0 (black) to 1 (the brightest). Set it to change the color.

## Blend colors

### interpolate\_color

**Code**

```python
import manimgx as m

class InterpolateColorExample(m.Scene):
    def construct(self) -> None:
        swatches = m.VGroup()
        for alpha in (0, 0.25, 0.5, 0.75, 1):
            color = m.interpolate_color(m.BLUE, m.RED, alpha)
            square = m.Square(side_length=1.8, color=color, fill_opacity=1)
            label = m.Text(str(alpha), font_size=32).next_to(square, m.DOWN)
            swatches.add(m.VGroup(square, label))
        self.add(swatches.arrange(buff=0.5))
```

The color a fraction of the way from one color to another.

The two mix as every blend of colors does: in OKLab, where the colors between two are those the eye sees between them.

```python
m.interpolate_color(a, b, alpha)
```

**`a`**

The color at 0.

**`b`**

The color at 1.

**`alpha`**

How far from `a` to `b`, from 0 to 1.

Returns A new color.

        import manimgx as m

        class InterpolateColorExample(m.Scene):
            def construct(self) -> None:
                swatches = m.VGroup()
                for alpha in (0, 0.25, 0.5, 0.75, 1):
                    color = m.interpolate_color(m.BLUE, m.RED, alpha)
                    square = m.Square(side_length=1.8, color=color, fill_opacity=1)
                    label = m.Text(str(alpha), font_size=32).next_to(square, m.DOWN)
                    swatches.add(m.VGroup(square, label))
                self.add(swatches.arrange(buff=0.5))
        ```
    """
    return ManimColor(a).interpolate(ManimColor(b), alpha)
````

### color\_gradient

**Code**

```python
import manimgx as m

class ColorGradientExample(m.Scene):
    def construct(self) -> None:
        colors = m.color_gradient([m.BLUE, m.GREEN, m.YELLOW, m.RED], 12)
        dots = m.VGroup(*(m.Dot(radius=0.4, color=color) for color in colors))
        self.add(dots.arrange(buff=0.3))
```

Colors evenly spaced along a gradient through reference colors, from the first to the last.

Each is mixed between the two reference colors on either side of it, as interpolate\_color mixes them.

```python
m.color_gradient(reference_colors, length_of_output)
```

**`reference_colors`**

The colors the gradient runs through, evenly spaced along it.

**`length_of_output`**

How many colors to return; one is the last reference color.

Returns The colors, in order along the gradient.

        import manimgx as m

        class ColorGradientExample(m.Scene):
            def construct(self) -> None:
                colors = m.color_gradient([m.BLUE, m.GREEN, m.YELLOW, m.RED], 12)
                dots = m.VGroup(*(m.Dot(radius=0.4, color=color) for color in colors))
                self.add(dots.arrange(buff=0.3))
        ```
    """
    if length_of_output == 0:
        return []
    if len(reference_colors) == 1:
        return [ManimColor(reference_colors[0])] * length_of_output
    rgbas = [ManimColor(c).to_rgba() for c in reference_colors]
    alphas = np.linspace(0, len(rgbas) - 1, length_of_output)
    floors = alphas.astype(int)
    alphas_mod1 = alphas % 1
    alphas_mod1[-1] = 1
    floors[-1] = len(rgbas) - 2
    return [
        ManimColor(tuple(mix_rgba(rgbas[i], rgbas[i + 1], float(a))))
        for i, a in zip(floors, alphas_mod1, strict=True)
    ]
````

### average\_color

The average of colors, taken in OKLab: the color the eye sees as their middle.

Their opacities are left out: the average is opaque.

```python
m.average_color(*colors)
```

**`*colors`**

The colors, in any form ManimColor reads.

Returns A new, opaque color.

### invert\_color

A color's complement: each of red, green and blue taken from 1, the opacity kept.

```python
m.invert_color(color)
```

**`color`**

The color, in any form ManimColor reads.

Returns A new color.

### colors\_by\_value

The color of each value on a colorscale: mixed between the colors on either side of it, and held beyond the colorscale's ends.

The colors mix as every blend of colors does: in OKLab, where the colors between two are those the eye sees between them.

```python
m.colors_by_value(colorscale, values, low, high)
```

**`colorscale`**

Colors spread evenly from `low` to `high`, or (color, value) pairs, each color at its value, in increasing order of value.

**`values`**

The values to color.

**`low`**

The value of the first color, when the colors are spread evenly.

**`high`**

The value of the last color, when the colors are spread evenly.

Returns One color per value, in order.

## Choose colors at random

### random\_color

A named color, drawn at random.

Python's `random` draws it, so `random.seed` makes it repeatable; see RandomColorGenerator for a stream of its own.

```python
m.random_color()
```

Returns One of the named colors.

### random\_bright\_color

A light color, drawn at random: its red, green and blue each from 0.5 to 1.

NumPy's global generator draws it, so `np.random.seed` makes it repeatable.

```python
m.random_bright_color()
```

Returns A new, opaque color.

### RandomColorGenerator

**Code**

```python
import manimgx as m

class RandomColorGeneratorExample(m.Scene):
    def construct(self) -> None:
        palette = [m.RED, m.GREEN, m.BLUE, m.YELLOW, m.PURPLE, m.TEAL]
        colors = m.RandomColorGenerator(seed=7, sample_colors=palette)
        squares = m.VGroup(
            *(
                m.Square(side_length=1, color=colors.next(), fill_opacity=1)
                for _ in range(40)
            )
        )
        self.add(squares.arrange_in_grid(rows=4, buff=0.2))
```

A stream of colors drawn at random, the same for the same seed.

```python
m.RandomColorGenerator(seed=None, sample_colors=None)
```

**`seed`**

The seed; None for a different stream each run.

**`sample_colors`**

The colors to draw from; None (or no colors) for the named colors.

#### next

The stream's next color: one of its colors, drawn at random.

```python
random_color_generator.next()
```
