import os
import shutil
from pathlib import Path
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def cleanup_old_files(max_age_hours: int = 24):
    """Clean up old script and render files"""
    try:
        # Cleanup manim scripts
        cleanup_directory(settings.MANIM_SCRIPTS_DIR, max_age_hours)
        
        # Cleanup renders
        cleanup_directory(settings.RENDERS_DIR, max_age_hours)
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def cleanup_directory(directory: Path, max_age_hours: int):
    """Remove files older than max_age_hours in the given directory"""
    if not directory.exists():
        return
        
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for item in directory.iterdir():
        if item.is_file():
            age = current_time - item.stat().st_mtime
            if age > max_age_seconds:
                try:
                    item.unlink()
                    logger.info(f"Removed old file: {item}")
                except Exception as e:
                    logger.error(f"Error removing file {item}: {e}")