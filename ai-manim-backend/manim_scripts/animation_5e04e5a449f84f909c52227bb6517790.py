from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(ShowCreation(circle))
        self.play(Transform(circle, square))
        self.wait()