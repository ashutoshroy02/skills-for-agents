# Scenes

**The film's code**

```python
import manimgx as m

class ScenesHero(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(color=m.BLUE, fill_opacity=0.5)
        words = m.Text("Hello!", font_size=72)
        self.play(m.Create(circle))
        self.play(m.FadeOut(circle))
        self.play(m.Write(words))
        self.wait()
```

A scene is one video. Make a class from Scene, and write what happens in its `construct` method: ManimGX runs it from top to bottom, and each line adds to the video in that order. The class's name is the video's: the scene `Hello` makes `Hello.mp4`.

Time passes only in play and wait. A play starts when the one before it ends and lasts as long as its longest animation; a wait holds the picture, while updaters keep running. add shows a mobject at once, taking no time.

- [**Scene**](<https://manimgx.academa.ai/reference/scenes/scene/index.md>)

  ---

  What happens and when: plays and waits, what the scene shows, its sections and its film.
- [**3D scenes**](<https://manimgx.academa.ai/reference/camera-and-3d/three-d-scenes/index.md>)

  ---

  A scene seen in three dimensions, from a camera that turns around it.
- [**Ready-made scenes**](<https://manimgx.academa.ai/reference/scenes/ready-made-scenes/index.md>)

  ---

  Scenes made for vectors, for linear transformations of the plane, and for a zoomed inset.
