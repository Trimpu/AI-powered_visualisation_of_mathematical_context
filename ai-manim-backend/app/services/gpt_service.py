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

async def generate_code(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """Generate Manim animation code using OpenRouter API."""
    if not settings.OPENROUTER_API_KEY:
        return None, "OpenRouter API key not configured"

    try:
        async with openai.AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
            default_headers={"HTTP-Referer": "https://github.com"}
        ) as client:
            system_prompt = "Write minimal Manim code. Start: from manim import *"

            try:
                response = await client.chat.completions.create(
                    model="openai/gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=120,  # reduced token budget to avoid 402 errors
                    presence_penalty=0,
                    frequency_penalty=0
                )
                
                if not response.choices:
                    return None, "No response from API"
                    
                code = response.choices[0].message.content.strip()
                code = clean_code(code)
                
                if not code:
                    return None, "Empty response from API"
                
                if not is_valid_manim_code(code):
                    logger.error(f"Invalid code generated: {code}")
                    return None, "Invalid Manim code generated"
                
                replacements = {
                    "ShowCreation": "Create",
                    "FadeIn(": "FadeIn(",
                    "GrowFromCenter": "Create"
                }
                
                for old, new in replacements.items():
                    code = code.replace(old, new)
                
                logger.info(f"Generated code:\n{code}")
                return code, None

            except openai.APIError as e:
                err_msg = str(e)
                if "code': 402" in err_msg or 'code": 402' in err_msg:
                    user_msg = (
                        "Code generation failed due to insufficient OpenRouter API credits. "
                        "Please reduce `max_tokens` further or upgrade your plan at "
                        "https://openrouter.ai/settings/credits"
                    )
                    logger.error(user_msg)
                    return None, user_msg
                logger.error(f"API error: {err_msg}")
                return None, f"OpenRouter API error: {err_msg}"

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
