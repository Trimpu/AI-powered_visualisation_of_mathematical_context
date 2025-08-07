from manim import *

class SquareToRectangle(Scene):
    def construct(self):
        square = Square()
        self.play(Create(square))
        rectangle = square.scale(1.5, about_edge=LEFT)
        self.play(Transform(square, rectangle))
        self.wait()