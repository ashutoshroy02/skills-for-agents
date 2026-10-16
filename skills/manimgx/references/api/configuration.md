# Configuration

**The film's code**

```python
import manimgx as m

m.config.pixel_width, m.config.pixel_height = 1080, 1920

class ConfigurationHero(m.Scene):
    def construct(self) -> None:
        frame = m.Rectangle(
            width=m.config.frame_width - 0.2,
            height=m.config.frame_height - 0.2,
            color=m.BLUE,
        )
        square = m.Square(side_length=8, color=m.YELLOW).scale(0.97)
        label = m.Text("1080 × 1920", font_size=56)
        self.play(m.Create(frame), m.Create(square), m.Write(label))
        self.wait()
```

`m.config` holds what every scene is made with: the video's size in pixels, its frame rate, its background, and the frame's size in units. Set it after `import manimgx as m`, before the scene is made; the command line's options set it too (`-r 1080x1920`, `--fps 30`).

The frame has the video's shape, and its short side is 8 units: a wide video shows about 14.2 × 8 units, a tall one 8 × 14.2, and the 8 × 8 square in the middle is in both.

## m.config

The configuration every scene is made and rendered with, as `m.config`: a `Config`. Set its fields before making a scene: `m.config.pixel_width, m.config.pixel_height = 1280, 720`.

## Config

The configuration scenes are made and rendered with: the video's size, frame rate and background, and the frame's size in scene units.

There is one, `config`. Set its fields before making a scene: a scene's camera, and the mobjects that fill the frame, take their sizes and the background from it when they are made, and `render` takes the video's size and frame rate when it starts. It can be read and set as a dictionary too, as Manim code does: `config["frame_width"]`, `config["pixel_height"] = 720`.

The frame has the video's proportions, and its short side is 8 units: a wide video (16:9) shows about 14.2 × 8 units, a tall one (9:16) 8 × 14.2. So what fits in the 8 × 8 square at the center fits both, at the same size.

### pixel\_width

The width of the video, in pixels (default 1920).

### pixel\_height

The height of the video, in pixels (default 1080). For a tall video (9:16), make it the larger: `config.pixel_width, config.pixel_height = 1080, 1920`.

### frame\_rate

How many frames a second the film has (default 60): frame k shows the scene at exactly k / `frame_rate` seconds. A video needs a whole number.

### simulation\_rate

How many times a second the simulation clock ticks (default 60).

A time-based updater that is not a flow is simulated: it steps at each tick of this clock and at the end of each play and wait, never at frames, so it takes the same steps at any frame rate, and a frame shows it as its last step left it. While one is in the scene, the scene computes every tick. At 60 frames a second each frame is a tick, so the ticks cost nothing more; at a frame rate that divides it (10, 12, 15, 20, 30), every frame falls on a tick too.

### background\_color

The color of the background (default black).

### background\_opacity

The opacity of the background, from 0 to 1 (default 1).

### frame\_height

The height of the frame, in scene units. Unless set, the frame's short side is 8 units: a wide video's frame is 8 high, a tall one's as high as its proportions make it when it is 8 wide (about 14.2 at 9:16). Its width follows from the video's proportions.

```python
config.frame_height
```

### frame\_width

The width of the frame, in scene units: `frame_height` times the video's aspect ratio (about 14.2 at 16:9, 8 at 9:16).

```python
config.frame_width
```

### frame\_x\_radius

Half the frame's width, in scene units: the x of its right edge.

```python
config.frame_x_radius
```

### frame\_y\_radius

Half the frame's height, in scene units (4 for a wide video): the y of its top edge.

```python
config.frame_y_radius
```

### top

The middle of the frame's top edge: `frame_y_radius` up from the origin.

```python
config.top
```

### bottom

The middle of the frame's bottom edge: `frame_y_radius` down from the origin.

```python
config.bottom
```

### right\_side

The middle of the frame's right edge: `frame_x_radius` right of the origin.

```python
config.right_side
```

### left\_side

The middle of the frame's left edge: `frame_x_radius` left of the origin.

```python
config.left_side
```

### aspect\_ratio

The video's width over its height: `pixel_width / pixel_height` (16:9 by default).

```python
config.aspect_ratio
```

### background

The color of the background, as a `ManimColor`.

```python
config.background
```
