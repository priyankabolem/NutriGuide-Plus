from fastapi import APIRouter
from ..models import NutritionProfile, VerificationReport
from ..services.verifier import verify_profile

router = APIRouter()

@router.post("", response_model=VerificationReport)
def verify(profile: NutritionProfile):
    return verify_profile(profile)