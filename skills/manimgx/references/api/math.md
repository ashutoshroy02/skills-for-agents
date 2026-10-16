# Math

**The film's code**

```python
import manimgx as m

class MathHero(m.Scene):
    def construct(self) -> None:
        before = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=96)
        after = m.MathTex("a^2", "=", "c^2", "-", "b^2", font_size=96)
        before[2].set_color(m.YELLOW)
        after[4].set_color(m.YELLOW)
        self.play(m.Write(before))
        self.play(m.TransformMatchingTex(before, after))
        self.wait()
```

MathTex typesets a formula written in LaTeX: fractions, roots, sums and integrals, matrices, `cases`, Greek letters. Write it in a raw string, `r"..."`, so that Python keeps its backslashes. LaTeX packages and `\def` don't work; a command ManimGX doesn't know stops the scene with its name.

Give `MathTex` several strings, and each one is a part of the formula, to color, move or animate alone: `MathTex("a^2", "+", "b^2")[2]` is the b². Parts that are written the same in two formulas move into each other with TransformMatchingTex.

Tex is text with formulas in it, between `$` signs. If you know Typst, write it directly: Typst takes Typst markup, and MathTypst a formula in Typst's math syntax.

## MathTex

**Code**

```python
import manimgx as m

class MathTexExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex("a^2", "+", "b^2", "=", "c^2", font_size=144)
        formula[0].set_color(m.BLUE)
        formula[2].set_color(m.GREEN)
        formula[4].set_color(m.YELLOW)
        self.play(m.Write(formula))
```

**Code**

```python
import manimgx as m

class MathTexLatexExample(m.Scene):
    def construct(self) -> None:
        limit = r"\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e"
        formulas = m.VGroup(
            m.MathTex(r"\int_0^1 x^2 \, dx = \frac{1}{3}"),
            m.MathTex(r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}"),
            m.MathTex(limit),
            m.MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}"),
        )
        self.add(formulas.arrange_in_grid(rows=2, buff=1).scale(1.3))
```

LaTeX math, typeset in the engine, a part per string: `MathTex("a^2", "+", "b^2")[2]` is the \\(b^2\\), to color, move or match with another formula.

There is no LaTeX installation: the LaTeX is converted to Typst (by mitex, part of the engine) and typeset in display style, in New Computer Modern Math, white unless styled. Most of LaTeX's math converts: fractions, roots, sums and integrals, matrices (`pmatrix`, `bmatrix`, `array`), `cases` and `aligned`, accents, `\mathbb` and the other alphabets, `\text`, `\left` and `\right`, `\color`, `\newcommand`. Packages don't — `\usepackage` and their commands, such as `\ce` or `\SI` — nor does `\def`: a command mitex doesn't know raises a TypstError.

The strings are one formula, joined by `arg_separator` and typeset whole, so parting a formula moves none of its glyphs. Each string is a part, a MathTexPart of the glyphs it adds, and double braces set a part apart within a string: `MathTex("{{a^2}} + {{b^2}} = {{c^2}}")` has the five parts of the first example below. A string that stands on its own (its braces, environments and `\left`…`\right` closed within it) holds exactly its glyphs. The rest, such as a fraction's bar or the glyphs of a fragment like `"^2"`, go to the first fragment between the standing strings around them: in `MathTex(r"\frac{", "a", "}{", "b", "}")` the bar is the closing `"}"`'s, where TeX draws it, and in `MathTex(r"e^{i", r"\pi}")`, split inside a term, every glyph is the first part's. A formula whose parts can't be told apart raises ValueError.

`substrings_to_isolate` and `tex_to_color_map` split the strings further; set\_color\_by\_tex and get\_part\_by\_tex find parts by their LaTeX, and TransformMatchingTex moves each part to the part written the same way in another formula. Read as text (see Tex), the strings are one text in the same way, spaces and all.

```python
m.MathTex(*tex_strings, arg_separator=' ', substrings_to_isolate=None, tex_to_color_map=None, tex_environment='align*', **kwargs)
```

**`*tex_strings`**

The formula, in LaTeX: a string per part (a number is written as a string), and a part per `{{…}}` within one.

**`arg_separator`**

What joins the strings into `tex_string`, the formula (or text) they are typeset as.

**`substrings_to_isolate`**

Substrings to make parts of their own: each string is split around every occurrence of each.

**`tex_to_color_map`**

A color for each substring, which is made a part of its own and colored.

**`tex_environment`**

How the strings are read: with a name containing "align" (the default, "align\*"), as math; with any other, or None, as LaTeX text, math between `$` signs.

It also takes the `Typst` keywords and the style keywords.

### tex\_strings

The strings, a part's each: the arguments, split at `{{…}}` and around the isolated substrings.

### tex\_string

The LaTeX of the whole formula, or text: the strings, joined by `arg_separator`.

### get\_parts\_by\_tex

Find the parts whose LaTeX contains `tex`, or is it.

```python
formula.get_parts_by_tex(tex, substring=True, case_sensitive=True)
```

**`tex`**

The LaTeX to look for.

**`substring`**

Whether a part whose LaTeX contains `tex` matches; if not, only one whose LaTeX is `tex`.

**`case_sensitive`**

Whether upper and lower case differ.

Returns A new group of the parts themselves, in order.

### get\_part\_by\_tex

**Code**

```python
import manimgx as m

class MathTexGetPartByTexExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex(
            r"\sin^2\theta", "+", r"\cos^2\theta", "=", "1", font_size=120
        )
        self.add(formula)
        self.play(m.Indicate(formula.get_part_by_tex(r"\cos")))
```

Find the first part whose LaTeX contains `tex`, or is it.

```python
formula.get_part_by_tex(tex, substring=True, case_sensitive=True)
```

**`tex`**

The LaTeX to look for.

**`substring`**

Whether a part whose LaTeX contains `tex` matches; if not, only one whose LaTeX is `tex`.

**`case_sensitive`**

Whether upper and lower case differ.

Returns The part itself, or None if none matches.

        import manimgx as m

        class MathTexGetPartByTexExample(m.Scene):
            def construct(self) -> None:
                formula = m.MathTex(
                    r"\sin^2\theta", "+", r"\cos^2\theta", "=", "1", font_size=120
                )
                self.add(formula)
                self.play(m.Indicate(formula.get_part_by_tex(r"\cos")))
        ```
    """
    parts = self.get_parts_by_tex(tex, substring, case_sensitive)
    return parts[0] if len(parts) else None
````

### index\_of\_part

Find where a part is among the formula's parts; a mobject that is not one raises ValueError.

```python
formula.index_of_part(part)
```

**`part`**

One of the parts.

Returns Its index, from 0.

### set\_color\_by\_tex

**Code**

```python
import manimgx as m

class MathTexSetColorByTexExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTex(
            "x + y = y + x", substrings_to_isolate=["x", "y"], font_size=144
        )
        formula.set_color_by_tex("x", m.YELLOW)
        formula.set_color_by_tex("y", m.BLUE)
        self.add(formula)
```

Color the parts whose LaTeX contains `tex`, or is it.

```python
formula.set_color_by_tex(tex, color, substring=True, case_sensitive=True)
```

**`tex`**

The LaTeX to look for.

**`color`**

Their color.

**`substring`**

Whether a part whose LaTeX contains `tex` matches; if not, only one whose LaTeX is `tex`.

**`case_sensitive`**

Whether upper and lower case differ.

        import manimgx as m

        class MathTexSetColorByTexExample(m.Scene):
            def construct(self) -> None:
                formula = m.MathTex(
                    "x + y = y + x", substrings_to_isolate=["x", "y"], font_size=144
                )
                formula.set_color_by_tex("x", m.YELLOW)
                formula.set_color_by_tex("y", m.BLUE)
                self.add(formula)
        ```
    """
    for part in self.get_parts_by_tex(tex, substring, case_sensitive):
        part.set_color(color)
    return self
````

### set\_color\_by\_tex\_to\_color\_map

Color parts by their LaTeX: for each entry, the parts whose LaTeX contains it, or is it.

```python
formula.set_color_by_tex_to_color_map(texs_to_color_map, substring=True, case_sensitive=True)
```

**`texs_to_color_map`**

A color for each piece of LaTeX, applied in order.

**`substring`**

Whether a part whose LaTeX contains a piece matches; if not, only one whose LaTeX is the piece.

**`case_sensitive`**

Whether upper and lower case differ.

## MathTexPart

One of a MathTex's parts: the glyphs one of its strings adds to the formula, as a group that knows the string.

```python
m.MathTexPart(tex_string, *members)
```

**`tex_string`**

The LaTeX it was typeset from.

**`*members`**

Its glyphs.

### tex\_string

The LaTeX the part was typeset from.

## Tex

**Code**

```python
import manimgx as m

class TexExample(m.Scene):
    def construct(self) -> None:
        text = m.Tex(
            r"\textbf{Bold}, \emph{emphasized},\\ and math: $e^{i\pi} = -1$",
            font_size=96,
        )
        self.play(m.Write(text))
```

LaTeX text, typeset in the engine and centered, a part per string: math goes between `$` signs.

It is a MathTex that reads its strings as LaTeX text: bold (`\textbf`), italics (`\emph`, `\textit`), line breaks (`\\`) and inline math convert. The text is set in New Computer Modern, as LaTeX sets it, the math in New Computer Modern Math; white unless styled. The strings are one text, joined by `arg_separator` (nothing, by default) and typeset whole, as a MathTex's are one formula: `Tex("Fade", "In")` reads "FadeIn", and parting a text moves none of its glyphs. Its parts are told apart as a formula's are; a ligature two strings share is the first's.

```python
m.Tex(*tex_strings, **kwargs)
```

**`*tex_strings`**

The text, in LaTeX: a string per part.

It also takes the `MathTex` keywords and the style keywords.

## Typst

**Code**

```python
import manimgx as m

class TypstExample(m.Scene):
    def construct(self) -> None:
        document = m.Typst(
            "*Typst* markup, _typeset_ in the engine:\n\n"
            "$ sum_(k=1)^n k = (n(n+1))/2 $\n\n"
            "with #text(fill: orange)[colors of its own]",
            font_size=64,
        )
        self.play(m.Write(document))
```

A Typst document, typeset in the engine: every glyph and shape of its layout is a part, white unless styled.

The code is Typst markup, a document's body on a page as large as what it holds: `*strong*`, `_emphasis_`, math between `$` signs, `#set` and `#show` rules, and the rest of Typst. The parts are what Typst lays out, in document order, spaces excluded: glyphs (TypstGlyph) and shapes (a rule, a fraction's bar, a box). A labelled box, `#box[…] <name>`, is a group: select gives it. Packages are imported from `package_path` (and mitex, `@preview/mitex:0.2.7`, from ManimGX's engine), never downloaded; code Typst can't typeset raises a TypstError.

Text is set in Libertinus Serif and math in New Computer Modern Math, Typst's defaults, unless the code sets another font. The fonts are those ManimGX ships, so a document looks the same on every machine: Typst's own (these two, New Computer Modern and DejaVu Sans Mono), Noto Sans, and Noto faces for the scripts those lack, from Arabic, Hebrew and Devanagari to Chinese, Japanese and Korean, with symbols and emoji; a character a font lacks is set in one that has it. Fonts in `font_paths` come first, and a system font is read only for a family the code names that none of these has. A paragraph's direction and the forms of Han characters follow the code's `lang` and `dir` (`#set text(lang: "ja")`, `#set text(dir: rtl)`); a Text sets them from its characters.

What Typst paints in its default ink, black, takes `color`, and the colors the code sets are kept, unless paint keywords (`fill_color` and the rest) paint over every part. A document is typeset once: the same code is read back from a cache on disk, in any process.

```python
m.Typst(typst_code, *, font_size=DEFAULT_FONT_SIZE, typst_preamble='', font_paths=None, should_center=True, height=None, width=None, package_path=None, font_scale=1.0, color=None, fill_color=None, fill_opacity=None, stroke_color=None, stroke_opacity=None, stroke_width=None, opacity=None, **kwargs)
```

**`typst_code`**

The document: Typst markup.

**`font_size`**

The size of the text: an em is `font_size / 96` scene units (0.5 at 48).

**`typst_preamble`**

Typst code set before the document: rules, definitions, imports.

**`font_paths`**

Directories of font files, searched, with their subdirectories, before the fonts ManimGX ships.

**`should_center`**

Whether the mobject is centered on the origin.

**`height`**

The height to scale the mobject to, in scene units; None to size it by `font_size`.

**`width`**

The width to scale it to, in scene units, after `height`; None to size it by `font_size`.

**`package_path`**

The directory Typst packages are imported from (as `namespace/name/version` directories), besides mitex, which ManimGX's engine holds; None for none but mitex.

**`font_scale`**

How much larger than `font_size` the text is set: the layout is scaled by `font_size * font_scale`, while font\_size reads `font_size`. A Text sets it to its font's own scale, which makes a capital as tall in every font.

**`color`**

The color of Typst's default ink, black; None for white.

**`fill_color`**

A fill color for every part; None keeps the typeset ones.

**`fill_opacity`**

A fill opacity for every part, from 0 to 1; None keeps the typeset ones.

**`stroke_color`**

A stroke color for every part; None keeps the typeset ones.

**`stroke_opacity`**

A stroke opacity for every part, from 0 to 1; None keeps the typeset ones.

**`stroke_width`**

A stroke width for every part, in hundredths of a scene unit; None keeps the typeset ones, which scale with the mobject.

**`opacity`**

The opacity of every part's fill and stroke, from 0 to 1, where `fill_opacity` or `stroke_opacity` doesn't give one; None keeps the typeset ones.

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

### typst\_code

The Typst code the mobject was typeset from.

### typst\_preamble

The Typst code set before it.

### font\_size

The mobject's effective font size, including scaling. Explicit width or height determines this size when given at construction. Set it to a positive size to scale the mobject to it.

```python
typst.font_size
```

### select

**Code**

```python
import manimgx as m

class TypstSelectExample(m.Scene):
    def construct(self) -> None:
        text = m.Typst(
            "Label a #box[box] <noun> to #box[select] <verb> it",
            font_size=96,
        )
        text.select("noun").set_color(m.YELLOW)
        text.select("verb").set_color(m.BLUE)
        self.add(text)
```

Find the parts of a labelled group: of every group with that label, as one.

A label names a box in the code, `#box[…] <name>`; a MathTypst makes a group of `{{ … }}` too, named by `{{ … : name }}` or numbered in order. An unknown label raises KeyError, a number out of range IndexError.

```python
typst.select(key)
```

**`key`**

The label; or the number of a MathTypst's unnamed `{{ … }}` group, from 0.

Returns A new group of the parts themselves (not copies), in order.

        import manimgx as m

        class TypstSelectExample(m.Scene):
            def construct(self) -> None:
                text = m.Typst(
                    "Label a #box[box] <noun> to #box[select] <verb> it",
                    font_size=96,
                )
                text.select("noun").set_color(m.YELLOW)
                text.select("verb").set_color(m.BLUE)
                self.add(text)
        ```
    """
    label = f"_grp-{key}" if isinstance(key, int) else key
    if label not in self.labels:
        error = IndexError if isinstance(key, int) else KeyError
        raise error(f"no group {key!r}; labels: {list(self.labels)}")
    return self.labels[label]
````

### scale

Scale the mobject and its whole family about a point, as Mobject.scale does; the strokes the typesetting drew (a rule, a box's outline) keep their share of their part's size, unless the mobject was made with a `stroke_width`.

```python
typst.scale(scale_factor, scale_stroke=False, **kwargs)
```

**`scale_factor`**

The factor: 2 doubles the mobject's size, 0.5 halves it; or its factors along x, y and z.

**`scale_stroke`**

Whether the other strokes' widths scale too, by the factor.

**`about_point`**

The point that stays fixed, in scene coordinates; it takes precedence over `about_edge`.

**`about_edge`**

The point of the mobject's bounding box that stays fixed, named by a direction: UP for the middle of its top edge, UR for its top right corner, ORIGIN for its center.

## MathTypst

**Code**

```python
import manimgx as m

class MathTypstExample(m.Scene):
    def construct(self) -> None:
        formula = m.MathTypst(
            "{{ a^2 : a }} + {{ b^2 : b }} = {{ c^2 : c }}", font_size=144
        )
        formula.select("a").set_color(m.BLUE)
        formula.select("b").set_color(m.GREEN)
        formula.select("c").set_color(m.YELLOW)
        self.play(m.Write(formula))
```

A formula in Typst's math syntax, typeset in display style: its parts are its glyphs and shapes, white unless styled.

`MathTypst("x^2 + y^2")` typesets `$ x^2 + y^2 $`, in New Computer Modern Math. Double braces make groups, which select gives: `{{ x^2 }}` is numbered, 0 the first, and `{{ x^2 : square }}` is named "square"; the braces are not typeset.

```python
m.MathTypst(math_expression, **kwargs)
```

**`math_expression`**

The formula, in Typst math.

It also takes the `Typst` keywords and the style keywords.

## A typeset text's parts

Every text and formula is made of glyphs, as Typst sets them: each knows which characters of its source it draws. A source Typst can't set stops the scene with Typst's error.

### TypstGlyph

One glyph as Typst set it, a part of a typeset mobject: its outline, placed, and which characters of the source it draws.

`node` is where the glyph's source node starts in the Typst code (-1 if it isn't from the code), `drawn` the bytes of that node's text it draws, `key` its outline, `x_advance` its width in font units.

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

#### node

Where the source node the glyph came from starts in the Typst code, in bytes. A glyph a package's code drew (a radical a package's function sets) came from the innermost element of the code around it (its equation); -1 if none is.

#### drawn

The bytes of that node's text the glyph's cluster draws, from and to: of a string literal, the bytes of its value; -1, -1 if the node is an element around it.

#### key

The provenance key of its outline and font carets, the same in every process. Assigning a key does not change the live glyph's outline or carets.

#### x\_advance

Its advance, the width it takes in the line, in font units: a ligature's carets divide it.

### manimgx.drawing.typesetting.TypstError

The error raised when Typst can't typeset a document, or LaTeX can't be converted to Typst: its message is Typst's (or mitex's), each error with the bytes of the source it is at, counted from the start of the whole document typeset — a page setup and the preamble come before the code.
