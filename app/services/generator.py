from ..models import NutritionProfile, Recommendation, RecipeCard

def generate_profile_and_recipes(topk, notes=None) -> Recommendation:
    main_label = topk[0][0]
    prof = NutritionProfile(
        name=main_label,
        serving_grams=150.0,
        calories=280.0,
        macros={"protein_g": 40.0, "carbs_g": 0.0, "fat_g": 12.0},
        micronutrients={}
    )
    recipes = [
        RecipeCard(title="Protein Bowl", steps=["..."], time_minutes=20,
                   cost_estimate_usd=5.0, ingredients=["chicken","rice","veggies"]),
        RecipeCard(title="Quick Salad", steps=["..."], time_minutes=10,
                   cost_estimate_usd=3.0, ingredients=["chicken","greens","olive oil"]),
        RecipeCard(title="Wrap", steps=["..."], time_minutes=12,
                   cost_estimate_usd=3.5, ingredients=["chicken","tortilla","sauce"]),
    ]
    return Recommendation(profile=prof, recipes=recipes)