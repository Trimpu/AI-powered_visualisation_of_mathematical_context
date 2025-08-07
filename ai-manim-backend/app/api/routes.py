from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.gpt_service import generate_code
from app.services.manim_service import render_video
from app.core.config import settings
import logging
from typing import Optional
import uuid
import os

router = APIRouter()
logger = logging.getLogger("api")

class AnimationRequest(BaseModel):
    prompt: str

class AnimationResponse(BaseModel):
    video_url: Optional[str] = None
    error: Optional[str] = None
@router.post("/generate", response_model=AnimationResponse)
async def generate_animation(request: AnimationRequest):
    # Generate Manim code from prompt
    code, error = await generate_code(request.prompt)
    if error:
        logger.error(f"Code generation failed: {error}")
        return AnimationResponse(error=f"Code generation failed: {error}")
    
    logger.info(f"Generated code:\n{code}")
    
    try:
        # Save code to file
        script_path = settings.MANIM_SCRIPTS_DIR / f"animation_{uuid.uuid4().hex}.py"
        script_path.write_text(code)
        logger.info(f"Saved script to: {script_path}")
        
        # Render the animation
        video_path, render_error = render_video(script_path)
        if render_error:
            logger.error(f"Rendering failed: {render_error}")
            return AnimationResponse(error=f"Video rendering failed: {render_error}")
        
        if not video_path or not video_path.exists():
            return AnimationResponse(error="Video file was not created")
        
        # Create a relative URL path for the video
        video_url = f"/videos/{video_path.name}"
        logger.info(f"Video URL: {video_url}")
        
        return AnimationResponse(video_url=video_url)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return AnimationResponse(error=f"Server error: {str(e)}")