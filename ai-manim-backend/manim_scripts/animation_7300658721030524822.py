Here's the Manim CE code for creating an animation of a blue circle transforming into a red square:

```python
from manim import *

class TransformCircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        
        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)
```

In this code:

- We first create a blue circle and a red square.
- Then, we animate the creation of the circle with the `Create` method.
- After a pause of 1 second (using `self.wait(1)`), we transform the circle into the square with the `Transform` method.
- Finally, we wait for another second before the animation ends.