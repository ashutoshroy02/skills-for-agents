# Camera

**The film's code**

```python
import manimgx as m

class CameraHero(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=3, color=m.BLUE)
        tangent = m.Line(4 * m.LEFT, 4 * m.RIGHT, color=m.YELLOW).shift(3 * m.UP)
        self.add(circle, tangent)
        frame = self.camera.frame
        self.play(frame.animate.scale(0.25).move_to(3 * m.UP), run_time=2)
        self.wait()
        self.play(frame.animate.scale(4).move_to(m.ORIGIN), run_time=2)
```

Every scene has a camera, `self.camera`. Its frame, `self.camera.frame`, is a mobject: move it to pan, scale it to zoom, and animate it as any other mobject. A frame half as large shows everything twice as large.

The camera also sets the picture's look: its background, and, for 3D, its exposure, its tone mapping, its bloom and its shadows.

## Camera

What a frame shows: a view of the scene, made of mobjects, so that whatever moves a mobject moves the view.

Its `frame` is a rectangle in the scene whose center and size are the view: move it, scale it or animate it, and the view pans and zooms. In three dimensions (a `ThreeDScene`'s camera), it also orbits the frame's center, with perspective: five value trackers hold its angles `phi` and `theta`, its roll `gamma`, its `zoom` and its `focal_distance` (`phi_tracker`, `theta_tracker`, `gamma_tracker`, `zoom_tracker` and `focal_distance_tracker`), and its light is a point, `light_source`. A camera only describes the view: it never draws.

```python
m.Camera(*, three_d=False, frame_width=None, phi=0, theta=-90 * DEGREES, gamma=0, focal_distance=20.0, zoom=1, light_source_start_point=9 * DOWN + 7 * LEFT + 10 * OUT)
```

**`three_d`**

Whether it sees in three dimensions: with perspective and depth, from its orbit.

**`frame_width`**

The width of its frame, in scene units; None for the configured one (about 14.2 at 16:9). Its height is the configured one; a width out of the video's proportions stretches the picture.

**`phi`**

The angle between its line of sight and the z axis, in radians: 0 looks straight down on the xy plane.

**`theta`**

Its angle around the z axis, in radians, counterclockwise from the x axis: at −90° it looks from the side of negative y, so that x points right.

**`gamma`**

How far it turns about its line of sight, in radians.

**`focal_distance`**

Its distance from the frame's center, in scene units: the nearer, the stronger the perspective.

**`zoom`**

How much it magnifies: 2 shows everything twice as large.

**`light_source_start_point`**

Where the light is, in scene coordinates.

## The frame

### frame

The view: a rectangle in the scene, centered on the point the camera looks at, as wide and as tall as what it shows.

Move it, scale it or animate it to pan and zoom: `self.play(self.camera.frame.animate.scale(0.5))` zooms in, showing half as much, twice as large. Its outline is not drawn (a stroke width of 0).

### frame\_center

The point the camera looks at: its frame's center. Set it to move the frame there.

```python
camera.frame_center
```

### frame\_width

The width of the view, in scene units: its frame's.

```python
camera.frame_width
```

### frame\_height

The height of the view, in scene units: its frame's.

```python
camera.frame_height
```

### auto\_zoom

Fit the view around mobjects, in two dimensions: center the frame on them, and size it to fit them.

The frame keeps its proportions: its width fits the mobjects, or its height, whichever of the two they fill more of, and `margin` is added to it.

```python
camera.auto_zoom(mobjects, margin=0, animate=True)
```

**`mobjects`**

The mobjects to fit, the frame itself left out; at least one must remain (a ValueError otherwise).

**`margin`**

How much wider (or taller) than the mobjects the view is, in scene units.

**`animate`**

Whether to return an animation of the frame, to play, rather than fit it at once.

Returns The animation, to play; with `animate` False, the frame, fitted.

## The look

### background\_color

The color of the background: the configured one unless changed. Set it to any color.

```python
camera.background_color
```

### background\_opacity

The opacity of the background, from 0 to 1: the configured one unless changed.

### exposure

How much the light that mobjects with a material reflect is scaled before it is shown: 2 is twice as bright (one stop).

### tone\_mapping

How light brighter than white is shown: "linear" clips it (a lit surface's colors as they are, up to white), "agx" rolls it off as film does (AgX: highlights desaturate toward white, and nothing clips). The light lit surfaces send into a pixel is averaged first and shown once, as a camera records it.

### bloom

How much of the light that mobjects with a material send into the view the lens spreads around it, as a glow (bloom), from 0 to 1: 0 none (off), 0.05 a lens's faint glow, plain around light brighter than white, 1 all of it. What the glow spreads, the light leaves: the view keeps the light it has, spread.

It is spread from the light the view shows: what lies nearer, a mobject fixed in the frame too, hides the light behind it. It falls off with the distance from the light: half of it lies within a twentieth of the view's height, nearly all of it within a quarter. It is light, over everything the view shows: over a lit surface, it adds to the surface's light before the tone mapping shows them; over display paint (the background, mobjects without a material, mobjects fixed in the frame), the tone mapping shows it on its own and it adds to the paint, as a screen adds light (white stays white); where the view shows nothing (a transparent background), it shows alone, as opaque as it is bright. Mobjects without a material send no light: they never glow.

### ambient\_occlusion

How strongly the light from all around (an ambient or an environment light) is shut out of corners, creases and the ground under things, where the surfaces near them block it: 0 not at all (off), 1 the standard strength, more darker. Only mobjects with a material are lit by that light, and only opaque ones shut it out or are darkened; a sun's, a point's or a spot's light is left as it is.

It is found from what the view shows (screen-space ambient obscurance): a surface the view cannot see, such as a wall seen edge-on, shuts nothing out. Light bounces between the surfaces that shut it out, so light-colored ones darken less, and white ones hardly at all.

### ambient\_occlusion\_radius

How far around a point the surfaces that shut light out of it are sought, in scene units: about the size of the creases and contacts to darken.

### light\_source

Where the light comes from: a point in the scene, which lights the mobjects shaded in three dimensions (`shade_in_3d`). Move it like any mobject.

## Fixed on the screen

### fixed\_in\_frame\_mobjects

The mobjects pinned to the screen: those given to `add_fixed_in_frame_mobjects`, with every member of their families as they are now: a part one gains later (a number's new digits, what an updater or a Transform makes) is pinned with it.

```python
camera.fixed_in_frame_mobjects
```

### add\_fixed\_in\_frame\_mobjects

Pin mobjects to the screen: each is drawn where its points are, as in a two-dimensional view centered on the origin, over everything else.

They stay where they are on the screen whatever the camera's angles, zoom and center: a title placed with `to_corner` stays in its corner. Everything in them is pinned, now and later: a member added later (a number's new digits, what an updater or a Transform makes) is pinned too.

```python
camera.add_fixed_in_frame_mobjects(*mobjects)
```

**`*mobjects`**

The mobjects to pin, with their families.

## Its angles, in 3D

### three\_d

Whether the camera sees in three dimensions: with perspective and depth, from its orbit.

### get\_phi

The angle between the camera's line of sight and the z axis.

```python
camera.get_phi()
```

Returns The angle, in radians.

### get\_theta

The camera's angle around the z axis, counterclockwise from the x axis.

```python
camera.get_theta()
```

Returns The angle, in radians.

### get\_gamma

How far the camera turns about its line of sight.

```python
camera.get_gamma()
```

Returns The angle, in radians.

### get\_zoom

How much the camera magnifies.

```python
camera.get_zoom()
```

Returns 1 for none.

### get\_focal\_distance

The camera's distance from its frame's center.

```python
camera.get_focal_distance()
```

Returns The distance, in scene units.

### set\_phi

Set the angle between the camera's line of sight and the z axis, at once.

```python
camera.set_phi(value)
```

**`value`**

The angle, in radians: 0 looks straight down on the xy plane.

### set\_theta

Set the camera's angle around the z axis, at once.

```python
camera.set_theta(value)
```

**`value`**

The angle, in radians, counterclockwise from the x axis.

### set\_gamma

Set how far the camera turns about its line of sight, at once.

```python
camera.set_gamma(value)
```

**`value`**

The angle, in radians.
