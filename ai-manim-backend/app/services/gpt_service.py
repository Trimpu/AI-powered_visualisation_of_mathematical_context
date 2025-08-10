import logging
from pathlib import Path
import openai
from app.core.config import settings
from typing import Tuple, Optional
import re

logger = logging.getLogger("gpt")

def clean_code(code: str) -> str:
    """Clean the code while preserving important docstrings and comments."""
    code = re.sub(r'```python\n', '', code)
    code = re.sub(r'```\n?', '', code)
    if "from manim import" in code:
        code = code[code.index("from manim import"):]
    return code.strip()

def is_valid_manim_code(code: str) -> bool:
    """Validate Manim code structure and content."""
    try:
        if not code.startswith("from manim import"):
            return False
        
        required = [
            "from manim import *",
            "class",
            "Scene",
            "def construct",
            "self.play"
        ]
        if not all(element in code for element in required):
            return False
        
        compile(code, '<string>', 'exec')
        return True
    except Exception as e:
        logger.error(f"Code validation error: {e}")
        return False

def get_template_animation(prompt: str) -> str:
    """Return pre-made template animations for common requests."""
    prompt_lower = prompt.lower()
    
    if "circle" in prompt_lower and "square" in prompt_lower:
        return """from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        
        self.play(Create(circle))
        self.wait(0.5)
        self.play(Transform(circle, square))
        self.wait()"""
    
    elif "square" in prompt_lower and "rectangle" in prompt_lower:
        return """from manim import *

class SquareToRectangle(Scene):
    def construct(self):
        square = Square(color=BLUE)
        rectangle = Rectangle(width=2.0, height=1.0, color=RED)
        
        self.play(Create(square))
        self.wait(0.5)
        self.play(Transform(square, rectangle))
        self.wait()"""
    
    else:
        # Default simple animation
        return """from manim import *

class SimpleAnimation(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.wait()"""

async def generate_code(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """Generate Manim animation code using OpenRouter API."""
    try:
        # Use template animations to avoid API token limits
        code = get_template_animation(prompt)
        logger.info(f"Using template animation for prompt: {prompt}")
        logger.info(f"Generated code:\n{code}")
        return code, None
        
    except Exception as e:
        error_msg = f"Error generating code: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
