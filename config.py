import os
from typing import Optional

class Config:
    """Application configuration management"""
    
    @staticmethod
    def get_api_url() -> str:
        """Get API URL based on environment"""
        # For local development
        if os.getenv("ENV") != "production":
            return "http://localhost:8000"
        
        # For production (will be set in Streamlit secrets)
        return os.getenv("API_URL", "https://nutriguide-plus-api.onrender.com")
    
    @staticmethod
    def get_env() -> str:
        """Get current environment"""
        return os.getenv("ENV", "development")