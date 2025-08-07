import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import settings

# Create logs directory if it doesn't exist
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
def setup_logging():
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configure file handler
    file_handler = RotatingFileHandler(
        settings.LOGS_DIR / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Create separate loggers for different components
    loggers = {
        "gpt": logging.getLogger("gpt"),
        "manim": logging.getLogger("manim"),
        "api": logging.getLogger("api")
    }

    for logger in loggers.values():
        logger.setLevel(logging.INFO)

    return loggers

# Initialize loggers
loggers = setup_logging()