from manim import *

class TestScene(Scene):
    def construct(self):
        square = Square(color=BLUE)
        self.play(Create(square))
        self.wait()