from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)

        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)