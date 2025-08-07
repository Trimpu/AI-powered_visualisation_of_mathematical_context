from manim import *

class CircleToSquareTransformation(Scene):
    def construct(self):
        blue_circle = Circle(color=BLUE)
        self.play(Create(blue_circle))
        red_square = Square(color=RED)
        self.play(Transform(blue_circle, red_square))