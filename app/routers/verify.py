from fastapi import APIRouter
from ..models import NutritionProfile, VerificationReport
from ..services.verifier import verify_profile
from ..services.google_vision_recognizer import google_recognizer
import os

router = APIRouter()

@router.post("", response_model=VerificationReport)
def verify(profile: NutritionProfile):
    return verify_profile(profile)

@router.get("/google-vision-status")
def check_google_vision_status():
    """Check if Google Vision API is configured and working"""
    api_key = os.environ.get('GOOGLE_VISION_API_KEY')
    
    status = {
        "api_key_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "status": "ready" if api_key else "not_configured"
    }
    
    if api_key:
        # Test with a simple request (without actual image to save quota)
        try:
            import requests
            test_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
            # This will fail but tells us if the key is valid
            test_response = requests.post(test_url, json={"requests": []}, timeout=5)
            
            if test_response.status_code == 400:  # Expected for empty request
                status["api_key_valid"] = True
                status["status"] = "ready"
            elif test_response.status_code == 403:
                status["api_key_valid"] = False
                status["status"] = "invalid_key"
                status["error"] = "API key invalid or Vision API not enabled"
            else:
                status["api_key_valid"] = "unknown"
                status["status"] = f"unknown_response_{test_response.status_code}"
                
        except Exception as e:
            status["test_error"] = str(e)
            status["status"] = "test_failed"
    
    return status