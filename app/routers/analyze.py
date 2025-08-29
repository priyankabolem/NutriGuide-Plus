from fastapi import APIRouter, HTTPException
import base64
import io
from PIL import Image
from ..models import FoodScan, Recommendation
from ..services.vision import classify_topk
from ..services.generator import generate_profile_and_recipes

def determine_fallback_food(img: Image.Image) -> str:
    """Determine a reasonable fallback food based on basic image analysis"""
    # Simple heuristics for fallback identification
    img_small = img.resize((100, 100))
    pixels = list(img_small.getdata())
    
    # Color analysis for fallback
    total_pixels = len(pixels)
    green_count = sum(1 for r, g, b in pixels if g > max(r, b) + 20)
    brown_count = sum(1 for r, g, b in pixels if 80 < r < 180 and 40 < g < 120 and b < 80)
    white_count = sum(1 for r, g, b in pixels if r > 180 and g > 180 and b > 180)
    
    green_ratio = green_count / total_pixels
    brown_ratio = brown_count / total_pixels
    white_ratio = white_count / total_pixels
    
    # Simple fallback logic
    if green_ratio > 0.2:
        return "vegetables"
    elif brown_ratio > 0.25:
        return "cooked food"
    elif white_ratio > 0.3:
        return "rice"
    else:
        return "mixed dish"

router = APIRouter()

@router.post("", response_model=Recommendation)
def analyze(scan: FoodScan):
    """
    Analyze food image with validation and confidence handling
    """
    try:
        # Basic image validation
        try:
            img_bytes = base64.b64decode(scan.image_b64)
            img = Image.open(io.BytesIO(img_bytes))
            
            # Check if image is too small or unclear
            width, height = img.size
            if width < 50 or height < 50:
                raise HTTPException(status_code=422, detail="Image too small for analysis. Please upload a clearer image.")
                
            # Check if image is suspiciously large (might not be food)
            if width > 4000 or height > 4000:
                # Resize for processing
                img = img.resize((min(width, 1024), min(height, 1024)), Image.Resampling.LANCZOS)
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='JPEG', quality=85)
                scan.image_b64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            raise HTTPException(status_code=400, detail="Unable to process image. Please upload a valid food image.")
        
        # Classify food using computer vision
        topk = classify_topk(scan.image_b64, k=3)
        
        if not topk:
            raise HTTPException(status_code=422, detail="Could not analyze the uploaded image")
        
        # Enhanced confidence handling with intelligent fallbacks
        primary_confidence = topk[0][1]
        primary_food = topk[0][0]
        
        if primary_confidence < 0.4:
            # Low confidence - use generic but reasonable estimates
            fallback_food = determine_fallback_food(img)
            topk = [(fallback_food, 0.4)]
            print(f"⚠ Low confidence, using fallback: {fallback_food}")
        
        # Generate comprehensive recommendation
        recommendation = generate_profile_and_recipes(topk, notes=scan.notes)
        
        # Add appropriate confidence indicators
        if primary_confidence < 0.6:
            recommendation.profile.name = f"{recommendation.profile.name} (estimated)"
        elif 0.6 <= primary_confidence < 0.8:
            recommendation.profile.name = f"{recommendation.profile.name}"
        
        print(f"✓ Final result: {recommendation.profile.name} ({primary_confidence:.2f})")
        
        return recommendation
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")