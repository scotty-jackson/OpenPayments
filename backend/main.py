"""
FastAPI application for Global Factor Lab.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from api import countries, factors, analytics

# Create FastAPI app
app = FastAPI(
    title="Global Factor Lab API",
    description="API for exploring equity factor performance across countries and time",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(countries.router, prefix="/api", tags=["countries"])
app.include_router(factors.router, prefix="/api", tags=["factors"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Global Factor Lab API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host=host, port=port)
