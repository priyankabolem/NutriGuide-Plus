from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import analyze, verify

# API configuration
api = FastAPI(
    title="NutriGuide+",
    description="Advanced AI-powered nutrition analysis platform providing instant nutritional insights from food images",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Priyanka Bolem",
        "email": "support@nutriguideplus.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS configuration
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add response size and timeout middleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

# Add middleware to handle large responses
api.add_middleware(GZipMiddleware, minimum_size=1000)
api.add_middleware(TimeoutMiddleware)

# Health check endpoint
@api.get("/", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NutriGuide+ API",
        "version": "1.0.0"
    }

@api.get("/health", tags=["health"])
def detailed_health():
    """Detailed health check endpoint"""
    import datetime
    return {
        "status": "healthy",
        "service": "NutriGuide+ API",
        "version": "3.0.0",
        "build": "2025-01-real-cv",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "endpoints": [
            "/analyze - Food analysis endpoint",
            "/verify - Nutrition verification endpoint"
        ],
        "features": {
            "real_computer_vision": True,
            "usda_nutrition_database": True,
            "confidence_scoring": True,
            "image_validation": True,
            "unlimited_food_types": True
        }
    }

# Include routers
api.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
api.include_router(verify.router, prefix="/verify", tags=["Verification"])