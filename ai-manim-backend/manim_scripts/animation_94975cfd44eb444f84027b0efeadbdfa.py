Here is the Manim CE code for the animation you requested:

from manim import *

class TransformCircleIntoSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(FadeIn(circle))
        self.wait()
        self.play(Transform(circle, square))
        self.wait()

This animation starts with the creation and display of a blue circle. Then, the circle is transformed into a red square. The `wait()` function is used to pause the animation for a bit before moving on to the next part.