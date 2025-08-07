from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Manim Backend"
    
    # OpenRouter Settings
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    MODEL_NAME: str = "openai/gpt-4"  # Changed to GPT-4
    
    # File Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MANIM_SCRIPTS_DIR: Path = BASE_DIR / "manim_scripts"
    RENDERS_DIR: Path = BASE_DIR / "renders"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Environment
    ENV: str = "development"
    
    # Ensure directories exist
    def create_directories(self):
        for dir_path in [self.MANIM_SCRIPTS_DIR, self.RENDERS_DIR, self.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def validate_api_key(self):
        if not self.OPENROUTER_API_KEY:
            if self.ENV == "production":
                raise ValueError("OPENROUTER_API_KEY is required in production")
            else:
                print("Warning: OPENROUTER_API_KEY not set. API calls will fail.")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
settings.create_directories()
settings.validate_api_key()