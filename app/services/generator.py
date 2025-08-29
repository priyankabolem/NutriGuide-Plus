from typing import List, Tuple, Optional
import re
from ..models import NutritionProfile, Recommendation, RecipeCard

def calculate_dynamic_nutrition(food_name: str, serving_grams: float = None) -> dict:
    """Calculate nutrition dynamically based on food name and type"""
    
    # Extract key components from food name
    food_lower = food_name.lower()
    
    # Base nutrition values (will be modified based on food type)
    base_calories = 200
    base_protein = 15
    base_carbs = 25
    base_fat = 8
    
    # Serving size determination
    if serving_grams is None:
        if any(word in food_lower for word in ["soup", "smoothie", "juice", "shake"]):
            serving_grams = 250  # Liquids
        elif any(word in food_lower for word in ["salad", "vegetables", "fruits"]):
            serving_grams = 200  # Light foods
        elif any(word in food_lower for word in ["steak", "tenderloin", "chops"]):
            serving_grams = 180  # Dense meats
        else:
            serving_grams = 150  # Default
    
    # Protein-rich foods
    if any(word in food_lower for word in ["chicken", "turkey", "beef", "pork", "lamb", "fish", "salmon", "tuna", "shrimp", "eggs"]):
        base_calories = 250
        base_protein = 35
        base_carbs = 2
        base_fat = 12
        
        if "grilled" in food_lower or "baked" in food_lower:
            base_fat -= 3
        elif "fried" in food_lower:
            base_fat += 8
            base_calories += 100
    
    # Carb-heavy foods
    elif any(word in food_lower for word in ["rice", "pasta", "bread", "potato", "quinoa", "noodles"]):
        base_calories = 220
        base_protein = 8
        base_carbs = 45
        base_fat = 2
        
        if "brown rice" in food_lower or "whole wheat" in food_lower:
            base_protein += 2
            base_carbs -= 5
    
    # Vegetables
    elif any(word in food_lower for word in ["salad", "vegetables", "broccoli", "spinach", "carrots", "peppers"]):
        base_calories = 80
        base_protein = 3
        base_carbs = 15
        base_fat = 2
        
        if "salad" in food_lower:
            base_calories += 70  # Dressing
            base_fat += 8
    
    # Fruits
    elif any(word in food_lower for word in ["fruit", "apple", "banana", "berries", "mango", "watermelon"]):
        base_calories = 120
        base_protein = 2
        base_carbs = 30
        base_fat = 0.5
    
    # Complex dishes
    elif any(word in food_lower for word in ["pizza", "burger", "tacos", "sandwich", "burrito"]):
        base_calories = 450
        base_protein = 22
        base_carbs = 45
        base_fat = 20
        
        if "veggie" in food_lower or "vegetarian" in food_lower:
            base_protein -= 10
            base_calories -= 50
    
    # Desserts
    elif any(word in food_lower for word in ["cake", "pie", "cookies", "ice cream", "brownie"]):
        base_calories = 380
        base_protein = 5
        base_carbs = 55
        base_fat = 16
    
    # Breakfast items
    elif any(word in food_lower for word in ["pancakes", "waffles", "french toast", "oatmeal"]):
        base_calories = 320
        base_protein = 10
        base_carbs = 50
        base_fat = 10
    
    # Beverages
    elif any(word in food_lower for word in ["smoothie", "juice", "shake", "coffee"]):
        base_calories = 150
        base_protein = 5
        base_carbs = 25
        base_fat = 3
        
        if "protein shake" in food_lower:
            base_protein = 25
            base_calories = 220
    
    # Adjust for modifiers
    if "organic" in food_lower:
        base_calories *= 0.95
    if "gourmet" in food_lower or "special" in food_lower:
        base_calories *= 1.1
        base_fat *= 1.2
    
    # Scale by serving size
    scale_factor = serving_grams / 150.0
    
    return {
        "serving_grams": serving_grams,
        "calories": round(base_calories * scale_factor),
        "protein_g": round(base_protein * scale_factor, 1),
        "carbs_g": round(base_carbs * scale_factor, 1),
        "fat_g": round(base_fat * scale_factor, 1)
    }

def generate_dynamic_recipes(food_name: str, nutrition_info: dict) -> List[RecipeCard]:
    """Generate contextual recipes based on the detected food"""
    
    food_lower = food_name.lower()
    recipes = []
    
    # Extract main ingredient
    main_ingredient = food_name.split()[-1] if food_name else "ingredient"
    
    # Healthy transformation recipe
    healthy_recipe = RecipeCard(
        title=f"Healthier {food_name.title()}",
        steps=[
            f"Start with fresh, high-quality {main_ingredient}",
            "Use minimal oil or opt for air-frying/grilling",
            "Add plenty of vegetables for extra nutrients",
            "Season with herbs and spices instead of excess salt",
            "Serve with a side of whole grains or salad"
        ],
        time_minutes=25,
        cost_estimate_usd=round(8 + len(food_name) * 0.2, 2),
        ingredients=[main_ingredient, "vegetables", "olive oil", "herbs", "whole grains"]
    )
    recipes.append(healthy_recipe)
    
    # Quick version recipe
    if nutrition_info["calories"] > 300:
        quick_recipe = RecipeCard(
            title=f"Quick {food_name.title()} Bowl",
            steps=[
                f"Prepare base of quinoa or brown rice",
                f"Add pre-cooked or leftover {main_ingredient}",
                "Top with fresh vegetables and greens",
                "Drizzle with your favorite healthy sauce",
                "Garnish with seeds or nuts for crunch"
            ],
            time_minutes=15,
            cost_estimate_usd=round(6 + len(food_name) * 0.15, 2),
            ingredients=[main_ingredient, "quinoa", "mixed vegetables", "sauce", "nuts/seeds"]
        )
        recipes.append(quick_recipe)
    
    # Meal prep version
    meal_prep_recipe = RecipeCard(
        title=f"Meal Prep {food_name.title()}",
        steps=[
            f"Batch cook {main_ingredient} for the week",
            "Portion into meal prep containers",
            "Add different vegetables to each container",
            "Prepare various sauces for variety",
            "Store in refrigerator for up to 5 days"
        ],
        time_minutes=45,
        cost_estimate_usd=round(5 * (5 + len(food_name) * 0.1), 2),
        ingredients=[f"{main_ingredient} (bulk)", "variety of vegetables", "meal prep containers", "sauces"]
    )
    recipes.append(meal_prep_recipe)
    
    return recipes[:3]

def generate_profile_and_recipes(topk: List[Tuple[str, float]], notes: Optional[str] = None) -> Recommendation:
    """Generate nutrition profile and recipes for any detected food"""
    
    # Get the primary detected food
    main_food = topk[0][0]
    confidence = topk[0][1]
    
    # Calculate dynamic nutrition
    nutrition_info = calculate_dynamic_nutrition(main_food)
    
    # Create nutrition profile
    prof = NutritionProfile(
        name=main_food,
        serving_grams=nutrition_info["serving_grams"],
        calories=float(nutrition_info["calories"]),
        macros={
            "protein_g": nutrition_info["protein_g"],
            "carbs_g": nutrition_info["carbs_g"],
            "fat_g": nutrition_info["fat_g"]
        },
        micronutrients={
            "fiber_g": round(nutrition_info["carbs_g"] * 0.1, 1),
            "sugar_g": round(nutrition_info["carbs_g"] * 0.3, 1),
            "sodium_mg": round(nutrition_info["calories"] * 1.5),
            "cholesterol_mg": round(nutrition_info["fat_g"] * 10) if "meat" in main_food.lower() else 0
        }
    )
    
    # Generate contextual recipes
    recipes = generate_dynamic_recipes(main_food, nutrition_info)
    
    # Adjust based on notes
    if notes:
        notes_lower = notes.lower()
        if "low carb" in notes_lower or "keto" in notes_lower:
            prof.macros["carbs_g"] *= 0.5
            prof.calories -= prof.macros["carbs_g"] * 2
        elif "high protein" in notes_lower:
            prof.macros["protein_g"] *= 1.5
            prof.calories += prof.macros["protein_g"] * 2
        elif "vegan" in notes_lower or "vegetarian" in notes_lower:
            if any(meat in main_food.lower() for meat in ["chicken", "beef", "pork", "fish", "turkey"]):
                main_food = main_food.replace("chicken", "tofu").replace("beef", "tempeh").replace("pork", "seitan")
                prof.name = main_food
                prof.micronutrients["cholesterol_mg"] = 0
    
    return Recommendation(profile=prof, recipes=recipes)