from fastapi import APIRouter, HTTPException
import base64
import io
from PIL import Image
from ..models import FoodScan, Recommendation
from ..services.vision import classify_topk
from ..services.generator import generate_profile_and_recipes

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
        
        # Check confidence threshold
        primary_confidence = topk[0][1]
        if primary_confidence < 0.3:
            # Low confidence - provide general guidance with disclaimer
            topk = [("mixed dish", 0.3)]
            print(f"⚠ Low confidence detection: {topk[0][0]} ({primary_confidence:.2f})")
        
        # Generate comprehensive recommendation
        recommendation = generate_profile_and_recipes(topk, notes=scan.notes)
        
        # Add confidence note to profile name if moderate confidence
        if 0.3 <= primary_confidence < 0.7:
            recommendation.profile.name = f"{recommendation.profile.name} (estimated)"
            print(f"⚠ Moderate confidence detection: {topk[0][0]} ({primary_confidence:.2f})")
        
        return recommendation
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")