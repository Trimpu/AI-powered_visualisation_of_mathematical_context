# Contents of /ai-manim-backend/ai-manim-backend/app/__init__.py

from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI()

app.include_router(api_router)