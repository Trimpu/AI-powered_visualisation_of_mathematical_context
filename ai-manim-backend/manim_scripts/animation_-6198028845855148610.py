Here is the Manim CE code to create an animation of a blue circle transforming into a red square.

```python
from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(Create(circle))
        self.wait()
        self.play(Transform(circle, square))
        self.wait()
```

In this code, we first create a blue circle and a red square. We then use `self.play(Create(circle))` to animate the creation of the circle. After waiting for a moment with `self.wait()`, we transform the circle into the square with `self.play(Transform(circle, square))`. Finally, we use `self.wait()` again to pause the scene before it ends.