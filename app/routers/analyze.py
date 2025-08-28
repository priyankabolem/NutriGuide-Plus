from fastapi import APIRouter
from ..models import FoodScan, Recommendation
from ..services.vision import classify_topk
from ..services.generator import generate_profile_and_recipes

router = APIRouter()

@router.post("", response_model=Recommendation)
def analyze(scan: FoodScan):
    topk = classify_topk(scan.image_b64, k=3)
    return generate_profile_and_recipes(topk, notes=scan.notes)