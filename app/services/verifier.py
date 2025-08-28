import pandas as pd
from ..models import NutritionProfile, VerificationReport, VerificationItem

_CANON = pd.read_csv("data/canonical_foods.csv")

def verify_profile(profile: NutritionProfile) -> VerificationReport:
    row = _CANON[_CANON["name"].str.lower() == profile.name.lower()]
    items = []
    if not row.empty:
        r = row.iloc[0]
        target = float(r["calories"])
        delta = abs(profile.calories - target) / max(1.0, target)
        ok = delta <= 0.15
        items.append(VerificationItem(
            claim=f"Calories ≈ {profile.calories}",
            status="supported" if ok else "flagged",
            evidence=f"Canonical ~ {target} kcal per {r['serving_grams']} g",
            confidence=0.85 if ok else 0.45
        ))
        overall = sum(i.confidence for i in items)/len(items)
    else:
        items.append(VerificationItem(
            claim=f"Unknown food: {profile.name}",
            status="flagged", evidence="Not found in canonical subset", confidence=0.30
        ))
        overall = 0.30
    return VerificationReport(items=items, overall_confidence=overall)