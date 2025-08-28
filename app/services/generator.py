from typing import List, Tuple, Optional
from ..models import NutritionProfile, Recommendation, RecipeCard

# Nutrition database for different foods
NUTRITION_DATA = {
    "grilled chicken": {
        "serving_grams": 150.0,
        "calories": 280.0,
        "macros": {"protein_g": 40.0, "carbs_g": 0.0, "fat_g": 12.0},
        "recipes": [
            RecipeCard(
                title="Protein Power Bowl",
                steps=[
                    "Season chicken breast with herbs and spices",
                    "Grill for 6-7 minutes each side until cooked through",
                    "Prepare quinoa or brown rice as base",
                    "Add steamed vegetables and sliced chicken",
                    "Drizzle with lemon juice and olive oil"
                ],
                time_minutes=25,
                cost_estimate_usd=6.50,
                ingredients=["chicken breast", "quinoa", "mixed vegetables", "olive oil", "lemon"]
            ),
            RecipeCard(
                title="Mediterranean Chicken Salad",
                steps=[
                    "Dice grilled chicken into bite-sized pieces",
                    "Mix greens, tomatoes, cucumbers, and olives",
                    "Add feta cheese and chicken",
                    "Dress with olive oil and balsamic vinegar"
                ],
                time_minutes=15,
                cost_estimate_usd=7.00,
                ingredients=["chicken", "mixed greens", "feta cheese", "olives", "tomatoes"]
            ),
            RecipeCard(
                title="Chicken Lettuce Wraps",
                steps=[
                    "Shred the grilled chicken",
                    "Mix with diced vegetables and Asian sauce",
                    "Serve in crisp lettuce cups",
                    "Garnish with sesame seeds and green onions"
                ],
                time_minutes=10,
                cost_estimate_usd=5.50,
                ingredients=["chicken", "lettuce", "carrots", "bell peppers", "soy sauce"]
            )
        ]
    },
    "pizza": {
        "serving_grams": 107.0,
        "calories": 285.0,
        "macros": {"protein_g": 12.0, "carbs_g": 36.0, "fat_g": 10.0},
        "recipes": [
            RecipeCard(
                title="Veggie-Loaded Pizza",
                steps=[
                    "Start with whole wheat pizza dough",
                    "Spread tomato sauce evenly",
                    "Add mozzarella and vegetable toppings",
                    "Bake at 450°F for 12-15 minutes"
                ],
                time_minutes=20,
                cost_estimate_usd=8.00,
                ingredients=["pizza dough", "tomato sauce", "mozzarella", "vegetables"]
            ),
            RecipeCard(
                title="Pizza Salad Bowl",
                steps=[
                    "Chop leftover pizza into bite-sized pieces",
                    "Toss with fresh arugula and spinach",
                    "Add cherry tomatoes and fresh basil",
                    "Drizzle with Italian dressing"
                ],
                time_minutes=10,
                cost_estimate_usd=6.00,
                ingredients=["pizza", "arugula", "spinach", "tomatoes", "Italian dressing"]
            )
        ]
    },
    "salmon": {
        "serving_grams": 150.0,
        "calories": 310.0,
        "macros": {"protein_g": 35.0, "carbs_g": 0.0, "fat_g": 18.0},
        "recipes": [
            RecipeCard(
                title="Lemon Herb Salmon",
                steps=[
                    "Season salmon with herbs, salt, and pepper",
                    "Pan-sear skin-side down for 4 minutes",
                    "Flip and cook for 3 more minutes",
                    "Serve with lemon wedges and steamed vegetables"
                ],
                time_minutes=15,
                cost_estimate_usd=12.00,
                ingredients=["salmon fillet", "lemon", "herbs", "olive oil", "vegetables"]
            ),
            RecipeCard(
                title="Salmon Poke Bowl",
                steps=[
                    "Cube salmon into bite-sized pieces",
                    "Marinate in soy sauce and sesame oil",
                    "Serve over sushi rice with avocado",
                    "Top with seaweed and sesame seeds"
                ],
                time_minutes=20,
                cost_estimate_usd=14.00,
                ingredients=["salmon", "sushi rice", "avocado", "soy sauce", "seaweed"]
            )
        ]
    },
    "pasta": {
        "serving_grams": 200.0,
        "calories": 320.0,
        "macros": {"protein_g": 12.0, "carbs_g": 62.0, "fat_g": 3.0},
        "recipes": [
            RecipeCard(
                title="Primavera Pasta",
                steps=[
                    "Cook pasta according to package directions",
                    "Sauté vegetables in olive oil",
                    "Toss pasta with vegetables and garlic",
                    "Finish with parmesan and fresh herbs"
                ],
                time_minutes=20,
                cost_estimate_usd=6.00,
                ingredients=["pasta", "mixed vegetables", "garlic", "olive oil", "parmesan"]
            )
        ]
    },
    "burger": {
        "serving_grams": 200.0,
        "calories": 450.0,
        "macros": {"protein_g": 28.0, "carbs_g": 35.0, "fat_g": 22.0},
        "recipes": [
            RecipeCard(
                title="Protein Style Burger",
                steps=[
                    "Wrap burger in lettuce instead of bun",
                    "Add tomato, onion, and pickles",
                    "Serve with side salad",
                    "Use mustard instead of mayo for lower calories"
                ],
                time_minutes=5,
                cost_estimate_usd=9.00,
                ingredients=["burger patty", "lettuce", "tomatoes", "onions", "pickles"]
            )
        ]
    },
    "salad": {
        "serving_grams": 200.0,
        "calories": 150.0,
        "macros": {"protein_g": 5.0, "carbs_g": 10.0, "fat_g": 10.0},
        "recipes": [
            RecipeCard(
                title="Power Greens Salad",
                steps=[
                    "Mix spinach, kale, and arugula",
                    "Add nuts, seeds, and dried fruit",
                    "Top with grilled protein of choice",
                    "Dress with vinaigrette"
                ],
                time_minutes=10,
                cost_estimate_usd=8.00,
                ingredients=["mixed greens", "nuts", "seeds", "dried fruit", "vinaigrette"]
            )
        ]
    }
}

def generate_profile_and_recipes(topk: List[Tuple[str, float]], notes: Optional[str] = None) -> Recommendation:
    """Generate nutrition profile and recipes based on identified food"""
    main_label = topk[0][0].lower()
    
    # Get nutrition data or use defaults
    if main_label in NUTRITION_DATA:
        data = NUTRITION_DATA[main_label]
        prof = NutritionProfile(
            name=main_label,
            serving_grams=data["serving_grams"],
            calories=data["calories"],
            macros=data["macros"],
            micronutrients={}
        )
        recipes = data["recipes"]
    else:
        # Default nutrition profile for unrecognized foods
        prof = NutritionProfile(
            name=main_label,
            serving_grams=150.0,
            calories=200.0,
            macros={"protein_g": 15.0, "carbs_g": 25.0, "fat_g": 8.0},
            micronutrients={}
        )
        # Generic recipes
        recipes = [
            RecipeCard(
                title=f"Healthy {main_label.title()} Bowl",
                steps=[
                    f"Prepare {main_label} according to preference",
                    "Add to a bowl with mixed greens",
                    "Include whole grains for balance",
                    "Top with a healthy dressing"
                ],
                time_minutes=15,
                cost_estimate_usd=7.00,
                ingredients=[main_label, "mixed greens", "whole grains", "dressing"]
            ),
            RecipeCard(
                title=f"{main_label.title()} Salad",
                steps=[
                    f"Dice or slice {main_label}",
                    "Mix with fresh vegetables",
                    "Add a protein source",
                    "Dress lightly with vinaigrette"
                ],
                time_minutes=10,
                cost_estimate_usd=6.00,
                ingredients=[main_label, "vegetables", "protein", "vinaigrette"]
            ),
            RecipeCard(
                title=f"Quick {main_label.title()} Wrap",
                steps=[
                    f"Place {main_label} in whole wheat tortilla",
                    "Add fresh vegetables and greens",
                    "Include a healthy sauce",
                    "Roll tightly and serve"
                ],
                time_minutes=8,
                cost_estimate_usd=5.00,
                ingredients=[main_label, "tortilla", "vegetables", "sauce"]
            )
        ]
    
    # Add only 3 recipes max
    return Recommendation(profile=prof, recipes=recipes[:3])