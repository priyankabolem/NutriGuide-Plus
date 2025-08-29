"""
Debug endpoints for troubleshooting Google Vision API integration
"""
from fastapi import APIRouter, HTTPException
import os
import base64
import requests
from ..services.vision import classify_topk
from ..services.google_vision_recognizer import detect_food_with_google_vision
from ..services.robust_food_detection import get_robust_food_detection
import json

router = APIRouter()

@router.get("/status")
def check_system_status():
    """Comprehensive system status check"""
    
    # Check Google Vision API key
    api_key = os.environ.get('GOOGLE_VISION_API_KEY')
    api_key_status = {
        "configured": bool(api_key),
        "length": len(api_key) if api_key else 0,
        "prefix": api_key[:10] + "..." if api_key and len(api_key) > 10 else "NOT_SET",
        "suffix": "..." + api_key[-5:] if api_key and len(api_key) > 5 else "NOT_SET"
    }
    
    # Check all environment variables
    env_vars = {
        "GOOGLE_VISION_API_KEY": bool(os.environ.get('GOOGLE_VISION_API_KEY')),
        "API_URL": os.environ.get('API_URL', 'not_set'),
        "ENV": os.environ.get('ENV', 'not_set'),
        "PYTHON_VERSION": os.environ.get('PYTHON_VERSION', 'not_set'),
    }
    
    # Test Google Vision API if key exists
    google_vision_test = {"status": "not_tested"}
    if api_key:
        try:
            # Test with a minimal request
            test_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
            test_payload = {"requests": []}
            response = requests.post(test_url, json=test_payload, timeout=5)
            
            google_vision_test = {
                "status": "tested",
                "response_code": response.status_code,
                "api_key_valid": response.status_code in [200, 400],  # 400 is expected for empty request
                "error": response.text if response.status_code not in [200, 400] else None
            }
        except Exception as e:
            google_vision_test = {
                "status": "error",
                "error": str(e)
            }
    
    return {
        "service": "NutriGuide+ Debug",
        "api_key_status": api_key_status,
        "environment_variables": env_vars,
        "google_vision_test": google_vision_test,
        "deployment_info": {
            "platform": "Render" if os.environ.get('RENDER') else "Local",
            "instance_id": os.environ.get('RENDER_INSTANCE_ID', 'local')
        }
    }

@router.post("/test-vision")
def test_vision_methods(test_image_url: str = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400"):
    """Test all vision methods with a sample image"""
    
    try:
        # Download test image
        response = requests.get(test_image_url, timeout=10)
        image_b64 = base64.b64encode(response.content).decode('utf-8')
        
        results = {
            "test_image": test_image_url,
            "image_size_bytes": len(response.content),
            "methods_tested": {}
        }
        
        # Test 1: Google Vision API directly
        try:
            food, confidence, features = detect_food_with_google_vision(image_b64)
            results["methods_tested"]["google_vision_direct"] = {
                "success": True,
                "food": food,
                "confidence": confidence,
                "api_available": features.get('api_available', False),
                "labels": features.get('google_vision_labels', [])[:5] if 'google_vision_labels' in features else []
            }
        except Exception as e:
            results["methods_tested"]["google_vision_direct"] = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
        
        # Test 2: Robust detection (fallback)
        try:
            food, confidence, features = get_robust_food_detection(image_b64)
            results["methods_tested"]["robust_detection"] = {
                "success": True,
                "food": food,
                "confidence": confidence,
                "dominant_color": features.get('dominant_color', 'unknown')
            }
        except Exception as e:
            results["methods_tested"]["robust_detection"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test 3: Main classify_topk function
        try:
            topk = classify_topk(image_b64, k=3)
            results["methods_tested"]["classify_topk"] = {
                "success": True,
                "results": [{"food": food, "confidence": conf} for food, conf in topk]
            }
        except Exception as e:
            results["methods_tested"]["classify_topk"] = {
                "success": False,
                "error": str(e)
            }
        
        # Check which method was actually used
        api_key = os.environ.get('GOOGLE_VISION_API_KEY')
        results["analysis"] = {
            "google_vision_should_be_used": bool(api_key),
            "actual_method_used": "Unknown - check logs"
        }
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@router.get("/env-check")
def check_environment():
    """Check all environment variables (safe version for production)"""
    
    def mask_sensitive(value: str, show_chars: int = 4) -> str:
        if not value or len(value) <= show_chars * 2:
            return "***"
        return f"{value[:show_chars]}...{value[-show_chars:]}"
    
    env_vars = {}
    sensitive_keys = ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']
    
    for key, value in os.environ.items():
        if any(sensitive in key.upper() for sensitive in sensitive_keys):
            env_vars[key] = mask_sensitive(value) if value else "NOT_SET"
        else:
            env_vars[key] = value if value else "NOT_SET"
    
    return {
        "total_env_vars": len(env_vars),
        "google_vision_configured": "GOOGLE_VISION_API_KEY" in os.environ,
        "relevant_vars": {
            k: v for k, v in env_vars.items() 
            if any(term in k.upper() for term in ['GOOGLE', 'VISION', 'API', 'RENDER', 'ENV'])
        }
    }

@router.post("/test-image-analysis")
async def test_specific_image(image_b64: str):
    """Test a specific image with all methods and return detailed results"""
    
    results = {
        "image_info": {
            "base64_length": len(image_b64),
            "estimated_size_kb": len(image_b64) * 0.75 / 1024  # Rough estimate
        },
        "google_vision_enabled": bool(os.environ.get('GOOGLE_VISION_API_KEY')),
        "analysis_results": {}
    }
    
    # Test with main classifier
    try:
        topk = classify_topk(image_b64, k=3)
        results["analysis_results"]["main_classifier"] = {
            "success": True,
            "primary_detection": {
                "food": topk[0][0] if topk else "unknown",
                "confidence": topk[0][1] if topk else 0
            },
            "all_results": [{"food": f, "confidence": c} for f, c in topk]
        }
    except Exception as e:
        results["analysis_results"]["main_classifier"] = {
            "success": False,
            "error": str(e)
        }
    
    # Test Google Vision directly if available
    if os.environ.get('GOOGLE_VISION_API_KEY'):
        try:
            food, confidence, features = detect_food_with_google_vision(image_b64)
            results["analysis_results"]["google_vision"] = {
                "success": True,
                "food": food,
                "confidence": confidence,
                "detected_labels": features.get('google_vision_labels', [])[:10],
                "api_responded": features.get('api_available', False)
            }
        except Exception as e:
            results["analysis_results"]["google_vision"] = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    else:
        results["analysis_results"]["google_vision"] = {
            "success": False,
            "error": "API key not configured"
        }
    
    return results