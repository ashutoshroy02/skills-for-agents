# Images and SVG

**The film's code**

```python
import manimgx as m
import numpy as np

class ImagesAndSvgHero(m.Scene):
    def construct(self) -> None:
        x = np.linspace(-1, 1, 64)
        pixels = np.zeros((64, 64, 3), dtype=np.uint8)
        pixels[..., 0] = 255 * (x[None, :] + 1) / 2
        pixels[..., 2] = 255 * (x[:, None] + 1) / 2
        image = m.ImageMobject(pixels).scale_to_fit_height(4)
        image.set_resampling_algorithm(m.RESAMPLING_ALGORITHMS["nearest"])
        self.play(m.FadeIn(image))
        self.play(image.animate.rotate(m.PI / 8).scale(0.8))
        self.wait()
```

An image is a picture on a rectangle: read from a file (PNG, JPEG and the rest), or made from an array of pixels. It moves, scales, turns and fades as any mobject; its pixels stay its own. An SVG drawing is different: its shapes become paths, each a part to color, move and draw in, as a shape of ManimGX's own.

## ImageMobject

**Code**

```python
import numpy as np

import manimgx as m

class ImageMobjectExample(m.Scene):
    def construct(self) -> None:
        ramp = np.linspace(0, 255, 256)
        pixels = np.zeros((256, 256, 3), dtype=np.uint8)
        pixels[..., 0] = ramp  # red grows to the right
        pixels[..., 2] = ramp[:, np.newaxis]  # blue grows downward
        image = m.ImageMobject(pixels, scale_to_resolution=400)
        self.play(m.FadeIn(image))
```

**Code**

```python
import numpy as np

import manimgx as m

class ImageMobjectResamplingExample(m.Scene):
    def construct(self) -> None:
        pixels = np.full((3, 3), 60, dtype=np.uint8)
        pixels[1, 1] = 255  # one white pixel, amid gray ones
        images = m.Group()
        for name in ("nearest", "linear", "cubic"):
            image = m.ImageMobject(
                pixels,
                scale_to_resolution=6,
                resampling_algorithm=m.RESAMPLING_ALGORITHMS[name],
            )
            images.add(m.Group(image, m.Text(name).next_to(image, m.DOWN)))
        self.add(images.arrange(buff=0.5))
```

A picture: an image file or an array of pixels, on a rectangle as tall as its pixels make it.

An image `scale_to_resolution` pixels tall (1080 unless given) is as tall as the frame's short side (8 scene units by default), and any other in proportion. Shown larger than its pixels, the picture is reconstructed from them by `resampling_algorithm`: by default a smooth cubic through every pixel; linear blends neighboring pixels; nearest shows each pixel as a square of its color. Shown smaller, it is sampled, not averaged. The mobject's opacity multiplies its pixels' own.

```python
m.ImageMobject(filename_or_array, scale_to_resolution=1080, invert=False, image_mode='RGBA', resampling_algorithm=3, stroke_width=0, stroke_color=WHITE, **kwargs)
```

**`filename_or_array`**

The picture: an image file's path, the file's contents (bytes), or an array of pixel values from 0 to 255: (h, w) gray, (h, w, 3) RGB or (h, w, 4) RGBA.

**`scale_to_resolution`**

How many pixels tall an image as tall as the frame's short side is; 0 for an image 3 units tall, whatever its size.

**`invert`**

Whether its colors are inverted (not its transparency).

**`image_mode`**

The mode, as the Pillow library names them, a file is read in: "RGBA", or "L" for gray.

**`resampling_algorithm`**

How the picture is reconstructed from its pixels, by the Pillow library's number: 0, nearest; 2, linear; 3, cubic (Keys' cubic convolution, Pillow's bicubic); RESAMPLING\_ALGORITHMS gives them by name.

**`stroke_width`**

The width of a border around the picture, in hundredths of a scene unit; 0 for none.

**`stroke_color`**

The border's color.

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

### pixel\_array

The current picture's (h, w, 4) RGBA pixels, from 0 to 255.

Pictures decoded or tinted by this image are read-only. Becoming another textured mesh adopts its texture, including whether it is writable.

```python
image_mobject.pixel_array
```

### set\_color

Paint every pixel `color`, keeping its opacity: the picture becomes a silhouette in that color.

```python
image_mobject.set_color(color=YELLOW_C, alpha=None, family=True)
```

**`alpha`**

Every pixel's opacity too, from 0 to 1; None keeps each one's.

**`family`**

Accepted for Manim compatibility; ignored: the picture alone is painted.

### set\_opacity

Set the picture's opacity, which multiplies its pixels' own.

```python
image_mobject.set_opacity(opacity=1.0, family=True, *, alpha=None)
```

**`opacity`**

The opacity, from 0 to 1.

**`family`**

Whether its whole family is set (a border too), or the picture alone.

**`alpha`**

The opacity, by the name Manim's images give it; given, it wins over `opacity`.

### set\_resampling\_algorithm

Set how the picture is reconstructed from its pixels where it is shown larger than they are.

```python
image_mobject.set_resampling_algorithm(resampling_algorithm)
```

**`resampling_algorithm`**

The filter, by the Pillow library's number: 0, nearest (each pixel a square of its color); 2, linear; 3, cubic (smooth, and through every pixel); RESAMPLING\_ALGORITHMS gives them by name.

### m.RESAMPLING\_ALGORITHMS

The filters an image can be reconstructed with, by name, each with its number (see Resampling): "nearest" or "none", "bilinear" or "linear", "bicubic" or "cubic".

### Resampling

```python
Resampling = Literal[0, 2, 3]
```

How an image is reconstructed from its pixels where it is drawn larger than they are, numbered as the Pillow library numbers its filters: 0, nearest (each pixel a square of its color); 2, linear; 3, cubic (Keys' cubic convolution with a = −½, Pillow's BICUBIC: smooth, and through every pixel).

## SVGMobject

A drawing read from an SVG file: each of its shapes a part, painted as the file paints it, 2 units tall unless sized.

Paths, lines, rectangles (rounded too), circles, ellipses, polygons and polylines become parts, in the file's order, with the file's fills, strokes and transforms; groups and `<use>` are followed, and text is skipped, with a warning. What the file leaves unpainted takes SVG's defaults, a black fill and no stroke, unless `svg_default` says otherwise. The file's groups are kept by their ids, in id\_to\_vgroup\_dict.

```python
m.SVGMobject(file_name=None, should_center=True, height=2, width=None, color=None, opacity=None, fill_color=None, fill_opacity=None, stroke_color=None, stroke_opacity=None, stroke_width=None, svg_default=None, path_string_config=None, use_svg_cache=True, **kwargs)
```

**`file_name`**

The SVG file.

**`should_center`**

Whether the drawing is centered on the origin.

**`height`**

The height to scale the drawing to, in scene units; None keeps the file's size, a scene unit per SVG unit.

**`width`**

The width to scale the drawing to, in scene units, after `height` (so it wins); None: as `height` makes it.

**`color`**

Accepted for Manim compatibility; no effect: the parts keep the file's colors (paint over them with `fill_color` and `stroke_color`, or color what the file leaves unpainted through `svg_default`).

**`opacity`**

Accepted for Manim compatibility; ignored.

**`fill_color`**

A fill color for every part; None keeps the file's.

**`fill_opacity`**

A fill opacity for every part, from 0 to 1; None keeps the file's.

**`stroke_color`**

A stroke color for every part; None keeps the file's.

**`stroke_opacity`**

A stroke opacity for every part, from 0 to 1; None keeps the file's.

**`stroke_width`**

A stroke width for every part, in hundredths of a scene unit; None keeps the file's.

**`svg_default`**

Paint keywords for what the file leaves unpainted; None for `{"stroke_width": 0}`: no stroke.

**`path_string_config`**

SVG path keywords for every path.

**`use_svg_cache`**

Whether parsed drawings are kept and copied for the same SVG content and path settings. The file is always read for changes.

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

### id\_to\_vgroup\_dict

The drawing's groups, by their ids: each `<g>` element's id names a group of the shapes inside it, and "root" all of them; an element without an id is named "numbered\_group\_" and a number.

### PathOptions

How an SVG path becomes curves: an SVGMobject's `path_string_config`, the keywords of each path it reads.

Beyond these, they take the style keywords.

**`long_lines`**

Accepted for Manim compatibility; ignored (default False).

**`should_subdivide_sharp_curves`**

Accepted for Manim compatibility; ignored (default False).

**`should_remove_null_curves`**

Accepted for Manim compatibility; ignored (default False).

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

#### long\_lines

Accepted for Manim compatibility; ignored (default False).

#### should\_subdivide\_sharp\_curves

Accepted for Manim compatibility; ignored (default False).

#### should\_remove\_null\_curves

Accepted for Manim compatibility; ignored (default False).
