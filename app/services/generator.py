from typing import List, Tuple, Optional
import re
import json
import os
from ..models import NutritionProfile, Recommendation, RecipeCard

def load_nutrition_database():
    """Load comprehensive nutrition database"""
    try:
        # Try comprehensive database first
        db_path = os.path.join(os.path.dirname(__file__), "../../data/comprehensive_nutrition.json")
        with open(db_path, 'r') as f:
            comprehensive_db = json.load(f)
        
        # Load original USDA data as fallback
        usda_path = os.path.join(os.path.dirname(__file__), "../../data/usda_nutrition.json")
        try:
            with open(usda_path, 'r') as f:
                usda_db = json.load(f)
            # Merge databases
            comprehensive_db.update(usda_db)
        except:
            pass
            
        print(f"✓ Loaded {len(comprehensive_db)} food items in nutrition database")
        return comprehensive_db
        
    except Exception as e:
        print(f"Error loading nutrition database: {e}")
        return {}

# Global nutrition database
NUTRITION_DB = load_nutrition_database()

def get_nutrition_from_database(food_name: str) -> Optional[dict]:
    """Get nutrition data from comprehensive database with intelligent matching"""
    food_lower = food_name.lower().strip()
    
    # Direct lookup first
    if food_lower in NUTRITION_DB:
        return NUTRITION_DB[food_lower]
    
    # Enhanced fuzzy matching for better accuracy
    best_match = None
    best_score = 0
    
    for db_food, data in NUTRITION_DB.items():
        # Calculate similarity score
        score = calculate_food_similarity(food_lower, db_food)
        
        if score > best_score and score > 0.5:  # Minimum similarity threshold
            best_score = score
            best_match = data
    
    if best_match:
        print(f"✓ Found nutrition match: {food_lower} → score {best_score:.2f}")
        return best_match
    
    return None

def calculate_food_similarity(food1: str, food2: str) -> float:
    """Calculate similarity between two food names"""
    words1 = set(food1.split())
    words2 = set(food2.split())
    
    # Exact match
    if food1 == food2:
        return 1.0
    
    # Word overlap score
    common_words = words1 & words2
    if not common_words:
        return 0.0
    
    # Calculate Jaccard similarity
    union_words = words1 | words2
    jaccard = len(common_words) / len(union_words)
    
    # Boost score for key food words
    key_words = ["chicken", "beef", "fish", "pizza", "salad", "rice", "pasta", "bread", "fruit"]
    for word in common_words:
        if word in key_words:
            jaccard += 0.2
    
    return min(jaccard, 1.0)

def calculate_dynamic_nutrition(food_name: str, serving_grams: float = None) -> dict:
    """Calculate nutrition using real USDA database with fallback estimation"""
    
    # Try to get from database first
    db_nutrition = get_nutrition_from_database(food_name)
    
    if db_nutrition:
        # Use database values
        base_data = db_nutrition.copy()
        target_serving = serving_grams or base_data["serving_size_g"]
        
        # Scale nutrition based on serving size
        scale_factor = target_serving / base_data["serving_size_g"]
        
        return {
            "serving_grams": target_serving,
            "calories": round(base_data["calories"] * scale_factor),
            "protein_g": round(base_data["protein_g"] * scale_factor, 1),
            "carbs_g": round(base_data["carbs_g"] * scale_factor, 1),
            "fat_g": round(base_data["fat_g"] * scale_factor, 1),
            "fiber_g": round(base_data["fiber_g"] * scale_factor, 1),
            "sugar_g": round(base_data["sugar_g"] * scale_factor, 1),
            "sodium_mg": round(base_data["sodium_mg"] * scale_factor),
            "cholesterol_mg": round(base_data["cholesterol_mg"] * scale_factor)
        }
    
    # Fallback estimation for unknown foods
    food_lower = food_name.lower()
    
    # Base nutrition values (will be modified based on food type)
    base_calories = 200
    base_protein = 15
    base_carbs = 25
    base_fat = 8
    base_fiber = 2
    base_sugar = 5
    base_sodium = 250
    base_cholesterol = 30
    
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
    if any(word in food_lower for word in ["chicken", "turkey", "beef", "pork", "lamb", "fish", "salmon", "tuna", "shrimp", "eggs", "meat"]):
        base_calories = 280
        base_protein = 35
        base_carbs = 2
        base_fat = 12
        base_fiber = 0
        base_sugar = 0
        base_sodium = 80
        base_cholesterol = 100
        
        if "grilled" in food_lower or "baked" in food_lower:
            base_fat -= 3
        elif "fried" in food_lower:
            base_fat += 8
            base_calories += 100
    
    # Carb-heavy foods
    elif any(word in food_lower for word in ["rice", "pasta", "bread", "potato", "quinoa", "noodles"]):
        base_calories = 210
        base_protein = 6
        base_carbs = 43
        base_fat = 1
        base_fiber = 2
        base_sugar = 1
        base_sodium = 5
        base_cholesterol = 0
    
    # Vegetables
    elif any(word in food_lower for word in ["salad", "vegetable", "broccoli", "spinach", "carrots", "peppers", "green"]):
        base_calories = 50
        base_protein = 3
        base_carbs = 10
        base_fat = 0.5
        base_fiber = 4
        base_sugar = 6
        base_sodium = 30
        base_cholesterol = 0
        
        if "salad" in food_lower:
            base_calories += 80  # Dressing
            base_fat += 8
            base_sodium += 200
    
    # Fruits
    elif any(word in food_lower for word in ["fruit", "apple", "banana", "berries", "mango", "watermelon", "strawberries"]):
        base_calories = 80
        base_protein = 1
        base_carbs = 20
        base_fat = 0.3
        base_fiber = 3
        base_sugar = 15
        base_sodium = 2
        base_cholesterol = 0
    
    # Complex dishes
    elif any(word in food_lower for word in ["pizza", "burger", "tacos", "sandwich", "burrito"]):
        base_calories = 350
        base_protein = 18
        base_carbs = 40
        base_fat = 15
        base_fiber = 3
        base_sugar = 4
        base_sodium = 600
        base_cholesterol = 45
    
    # Desserts
    elif any(word in food_lower for word in ["cake", "pie", "cookies", "ice cream", "brownie", "chocolate"]):
        base_calories = 380
        base_protein = 5
        base_carbs = 55
        base_fat = 16
        base_fiber = 2
        base_sugar = 45
        base_sodium = 350
        base_cholesterol = 65
    
    # Soups
    elif any(word in food_lower for word in ["soup", "broth", "stew"]):
        base_calories = 120
        base_protein = 6
        base_carbs = 18
        base_fat = 3
        base_fiber = 2
        base_sugar = 4
        base_sodium = 500
        base_cholesterol = 5
    
    # Scale by serving size
    scale_factor = serving_grams / 150.0
    
    return {
        "serving_grams": serving_grams,
        "calories": round(base_calories * scale_factor),
        "protein_g": round(base_protein * scale_factor, 1),
        "carbs_g": round(base_carbs * scale_factor, 1),
        "fat_g": round(base_fat * scale_factor, 1),
        "fiber_g": round(base_fiber * scale_factor, 1),
        "sugar_g": round(base_sugar * scale_factor, 1),
        "sodium_mg": round(base_sodium * scale_factor),
        "cholesterol_mg": round(base_cholesterol * scale_factor)
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
            "fiber_g": nutrition_info.get("fiber_g", round(nutrition_info["carbs_g"] * 0.1, 1)),
            "sugar_g": nutrition_info.get("sugar_g", round(nutrition_info["carbs_g"] * 0.3, 1)),
            "sodium_mg": nutrition_info.get("sodium_mg", round(nutrition_info["calories"] * 1.5)),
            "cholesterol_mg": nutrition_info.get("cholesterol_mg", round(nutrition_info["fat_g"] * 10) if "meat" in main_food.lower() else 0)
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