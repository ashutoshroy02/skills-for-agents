"""Reel template: copy to videos/<date>-<slug>/manim/scene.py and replace the beats.

Render from the video folder:
    manimgx inspect manim/scene.py -o work/Reel.storyboard.png
    manimgx render  manim/scene.py -r 540x960 -o work/Reel-preview.mp4
    manimgx render  manim/scene.py -o work/Reel.mp4
    vk render work/Reel.mp4 --preset reels --reframe none --fps 30
"""
import manimgx as m
import mgxkit

mgxkit.tall()  # 1080x1920 at 30 fps; frame 8 wide, ~14.2 high; keep content in mgxkit.SAFE


class Reel(m.Scene):
    voice = mgxkit.Kokoro("am_michael", 0.95)  # free local voice; lines cache in manim/voice/

    def construct(self) -> None:
        # Beat 1, the hook: on screen from the first frame, emphasised while it is said.
        hook = m.Text("Your hook here", font_size=72, weight=m.BOLD).move_to(2 * m.UP)
        self.add(hook)
        self.say("Your spoken hook, [the key words.]", m.Indicate(hook))

        # Beat 2, the payoff: each animation plays during its bracketed words.
        self.play(hook.animate.scale(0.6).to_edge(m.UP, buff=2.0))
        body = m.MathTex(r"a^2 + b^2 = c^2", font_size=110)
        self.say("Then show [the idea itself.]", m.Write(body))

        # Beat 3, the loop/CTA: a short line, then a beat of silence before the end.
        cta = m.Text("Follow for more", font_size=44).next_to(body, m.DOWN, buff=1.2)
        self.say("[Follow] for more.", m.FadeIn(cta, shift=m.UP))
        self.wait(0.8)
