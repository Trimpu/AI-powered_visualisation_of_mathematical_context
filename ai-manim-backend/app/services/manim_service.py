import subprocess
import logging
from pathlib import Path
from app.core.config import settings
from typing import Tuple, Optional
import shutil
import os
import re

logger = logging.getLogger("manim")

def get_scene_name(script_path: Path) -> str:
    """Extract scene name from the script content."""
    try:
        content = script_path.read_text()
        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', content)
        if match:
            return match.group(1)
    except Exception as e:
        logger.error(f"Failed to extract scene name: {e}")
    return script_path.stem

def render_video(script_path: Path) -> tuple[Path | None, str | None]:
    """
    Renders a Manim script to video.
    
    Args:
        script_path: Path to the Python script containing Manim code
    
    Returns:
        tuple: (video_path, error_message)
    """
    try:
        logger.info(f"Starting render for script: {script_path}")
        
        # Create media directory structure
        media_dir = settings.BASE_DIR / "media"
        media_dir.mkdir(exist_ok=True)
        videos_dir = media_dir / "videos"
        videos_dir.mkdir(exist_ok=True)
        
        # Ensure renders directory exists
        settings.RENDERS_DIR.mkdir(exist_ok=True)
        
        # Get scene name from script
        scene_name = get_scene_name(script_path)
        logger.info(f"Using scene name: {scene_name}")
        
        # Run manim with explicit scene name
        cmd = [
            "manim",
            "-pql",  # preview quality, last scene
            "--media_dir", str(media_dir),
            str(script_path),
            scene_name  # Explicitly specify the scene
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(settings.BASE_DIR)
        )
        
        logger.info(f"Manim stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"Manim stderr: {result.stderr}")
        
        if result.returncode != 0:
            return None, result.stderr
        
        # Debug: Check render directory contents
        render_dir = videos_dir / scene_name
        logger.info(f"Checking for mp4 in: {render_dir}")
        logger.info(f"Dir contents: {list(render_dir.rglob('*'))}")
        
        # Look for video in expected location first
        expected_path = render_dir / "1080p60" / f"{scene_name}.mp4"
        if expected_path.exists():
            latest_video = expected_path
            logger.info(f"Found video at expected path: {latest_video}")
        else:
            # Fall back to searching
            video_files = list(videos_dir.rglob("*.mp4"))
            if not video_files:
                video_files = list(media_dir.rglob("*.mp4"))
                
            if not video_files:
                logger.error("No video files found after rendering")
                return None, "Video file not found after rendering"
            
            latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
            logger.info(f"Found video at alternate location: {latest_video}")
        
        # Validate video file
        if not latest_video.exists() or latest_video.stat().st_size == 0:
            return None, "Rendered video file is empty or missing"
        
        # Copy to renders directory with a unique name
        output_path = settings.RENDERS_DIR / f"{script_path.stem}.mp4"
        shutil.copy2(latest_video, output_path)
        logger.info(f"Copied video to: {output_path}")
        
        if not output_path.exists():
            return None, "Failed to copy video to renders directory"
            
        return output_path, None
        
    except Exception as e:
        error_msg = f"Error rendering video: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg