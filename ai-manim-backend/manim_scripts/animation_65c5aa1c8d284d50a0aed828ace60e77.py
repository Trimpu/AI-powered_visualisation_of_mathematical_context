from manim import *

class TransformCircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(Transform(circle, square))