from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import loggers
from app.api.routes import router as api_router
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    loggers["api"].info("Starting AI Manim Backend...")
    loggers["api"].info(f"Server running at http://127.0.0.1:8000")
    loggers["api"].info(f"API documentation available at http://127.0.0.1:8000/docs")

@app.get("/", response_class=JSONResponse)
async def root():
    return {
        "status": "running",
        "message": "AI Manim Backend is running",
        "docs_url": "/docs",
        "api_url": f"{settings.API_V1_STR}/generate"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True
    )