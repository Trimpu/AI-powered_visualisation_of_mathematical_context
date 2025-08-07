from manim import *

class TransformCircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(Create(circle))
        self.play(Transform(circle, square))