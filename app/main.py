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
        "version": "1.3.0",
        "build": "2024-01-enhanced-classification",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "endpoints": [
            "/analyze - Food analysis endpoint",
            "/verify - Nutrition verification endpoint"
        ],
        "features": {
            "dynamic_food_recognition": True,
            "varied_responses": True,
            "expanded_database": True
        }
    }

# Include routers
api.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
api.include_router(verify.router, prefix="/verify", tags=["Verification"])