from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class FoodScan(BaseModel):
    image_b64: str
    notes: Optional[str] = None

class NutritionProfile(BaseModel):
    name: str
    serving_grams: float
    calories: float
    macros: Dict[str, float]              # protein_g, carbs_g, fat_g
    micronutrients: Dict[str, float] = {}

class RecipeCard(BaseModel):
    title: str
    steps: List[str]
    time_minutes: int
    cost_estimate_usd: float
    ingredients: List[str]

class Recommendation(BaseModel):
    profile: NutritionProfile
    recipes: List[RecipeCard]

class VerificationItem(BaseModel):
    claim: str
    status: str                           # supported | flagged
    evidence: Optional[str] = None
    confidence: float = Field(ge=0, le=1)

class VerificationReport(BaseModel):
    items: List[VerificationItem]
    overall_confidence: float = Field(ge=0, le=1)