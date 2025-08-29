"""
Advanced Food Recognition with Free Computer Vision Services
Uses multiple fallback systems for accurate food identification
"""
import os
import requests
import base64
from typing import Dict, List, Tuple, Optional
import json
import re

class EnhancedFoodRecognizer:
    def __init__(self):
        # Food pattern database for intelligent classification
        self.food_patterns = {
            # Common patterns that indicate specific foods
            "pizza": ["round", "red", "white", "brown", "cheese", "crust"],
            "burger": ["round", "brown", "layers", "meat", "bread"],
            "salad": ["green", "fresh", "mixed", "vegetables", "leaves"],
            "pasta": ["white", "yellow", "noodles", "sauce"],
            "rice": ["white", "grains", "small", "uniform"],
            "chicken": ["brown", "meat", "cooked", "protein"],
            "beef": ["brown", "red", "meat", "cooked"],
            "fish": ["light", "flaky", "protein"],
            "fruit": ["colorful", "fresh", "sweet", "natural"],
            "vegetable": ["green", "fresh", "natural", "healthy"],
            "bread": ["brown", "baked", "texture", "carbs"],
            "soup": ["liquid", "bowl", "smooth", "warm"],
            "dessert": ["sweet", "colorful", "sugar", "treat"]
        }
    
    def analyze_with_google_vision(self, image_b64: str) -> Optional[str]:
        """Use Google Vision API for accurate food detection"""
        try:
            # Check for API key
            api_key = os.getenv('GOOGLE_VISION_API_KEY')
            if not api_key:
                print("No Google Vision API key found")
                return None
            
            # Google Vision API endpoint
            url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
            
            # Request payload for label detection
            payload = {
                "requests": [
                    {
                        "image": {
                            "content": image_b64
                        },
                        "features": [
                            {
                                "type": "LABEL_DETECTION",
                                "maxResults": 20
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if "responses" in result and result["responses"]:
                    labels = result["responses"][0].get("labelAnnotations", [])
                    
                    # Extract food-related labels
                    food_labels = []
                    food_keywords = [
                        "food", "dish", "cuisine", "meal", "ingredient", "recipe",
                        "pizza", "burger", "salad", "chicken", "beef", "fish", "rice", 
                        "pasta", "bread", "fruit", "vegetable", "meat", "seafood",
                        "sandwich", "soup", "cake", "dessert", "breakfast", "lunch", "dinner"
                    ]
                    
                    for label in labels:
                        description = label.get("description", "").lower()
                        score = label.get("score", 0)
                        
                        # Check if label is food-related
                        if any(keyword in description for keyword in food_keywords):
                            food_labels.append((description, score))
                    
                    # Sort by confidence and return best food match
                    food_labels.sort(key=lambda x: x[1], reverse=True)
                    
                    if food_labels:
                        best_food = food_labels[0][0]
                        confidence = food_labels[0][1]
                        
                        # Map generic labels to specific food names
                        mapped_food = self.map_vision_label_to_food(best_food)
                        print(f"✓ Google Vision: {mapped_food} (confidence: {confidence:.2f})")
                        return mapped_food
                    
            return None
            
        except Exception as e:
            print(f"Google Vision API error: {e}")
            return None
    
    def map_vision_label_to_food(self, label: str) -> str:
        """Map Google Vision labels to specific food names"""
        label_lower = label.lower()
        
        # Comprehensive mappings for vision labels to standardized food names
        mappings = {
            # Main dishes
            "pizza": "pizza",
            "hamburger": "burger", 
            "cheeseburger": "burger",
            "sandwich": "sandwich",
            "hot dog": "hot dog",
            "taco": "tacos",
            "burrito": "burrito",
            
            # Proteins
            "chicken": "grilled chicken breast",
            "fried chicken": "fried chicken",
            "beef": "grilled steak",
            "steak": "grilled steak",
            "pork": "pork chops",
            "fish": "grilled fish",
            "salmon": "grilled salmon",
            "tuna": "tuna",
            "shrimp": "shrimp",
            "turkey": "turkey breast",
            "eggs": "scrambled eggs",
            
            # Grains & Starches
            "rice": "white rice",
            "fried rice": "fried rice",
            "pasta": "pasta with sauce",
            "spaghetti": "spaghetti",
            "noodles": "noodles",
            "bread": "bread",
            "toast": "toast",
            "potato": "baked potato",
            "french fries": "french fries",
            "quinoa": "quinoa",
            
            # Vegetables
            "salad": "green salad",
            "caesar salad": "caesar salad",
            "vegetable": "cooked vegetables",
            "broccoli": "steamed broccoli",
            "carrot": "carrots",
            "spinach": "spinach",
            "tomato": "tomato",
            "corn": "corn",
            "green beans": "green beans",
            
            # Fruits
            "fruit": "mixed fruit",
            "apple": "apple",
            "banana": "banana",
            "orange": "orange",
            "strawberry": "strawberries",
            "grapes": "grapes",
            "watermelon": "watermelon",
            "mango": "mango",
            
            # Soups & Liquids
            "soup": "vegetable soup",
            "tomato soup": "tomato soup",
            "chicken soup": "chicken soup",
            "smoothie": "fruit smoothie",
            "juice": "orange juice",
            
            # Desserts
            "cake": "chocolate cake",
            "ice cream": "vanilla ice cream",
            "cookie": "chocolate chip cookies",
            "pie": "apple pie",
            "brownie": "chocolate brownie",
            
            # Breakfast items
            "pancakes": "pancakes",
            "waffles": "waffles",
            "oatmeal": "oatmeal",
            "cereal": "cereal",
            "yogurt": "greek yogurt"
        }
        
        # Check direct mappings first
        for key, value in mappings.items():
            if key in label_lower:
                return value
        
        # Fallback to original label with cleanup
        return re.sub(r'[^\w\s]', '', label).strip() or "food item"
    
    def classify_by_common_patterns(self, visual_features: Dict) -> str:
        """Enhanced pattern-based food classification"""
        
        # Score each food type based on visual characteristics
        food_scores = {}
        
        for food_type, patterns in self.food_patterns.items():
            score = 0
            
            # Pizza scoring
            if food_type == "pizza":
                if (visual_features["red_ratio"] > 0.1 and 
                    visual_features["white_ratio"] > 0.1 and 
                    visual_features["brown_ratio"] > 0.05):
                    score += 0.8
                if visual_features["texture_complexity"] > 150:
                    score += 0.2
            
            # Salad scoring
            elif food_type == "salad":
                if visual_features["green_ratio"] > 0.25:
                    score += 0.9
                if visual_features["texture_complexity"] > 100:
                    score += 0.1
            
            # Meat scoring  
            elif food_type in ["chicken", "beef"]:
                if visual_features["brown_ratio"] > 0.3:
                    score += 0.7
                if visual_features["texture_complexity"] > 100:
                    score += 0.2
                if visual_features["red_ratio"] > 0.05:
                    score += 0.1
            
            # Fruit scoring
            elif food_type == "fruit":
                if (visual_features["red_ratio"] > 0.2 or 
                    visual_features["yellow_ratio"] > 0.2):
                    score += 0.6
                if visual_features["avg_brightness"] > 120:
                    score += 0.3
                if visual_features["brown_ratio"] < 0.1:
                    score += 0.1
            
            # Rice/pasta scoring
            elif food_type in ["rice", "pasta"]:
                if visual_features["white_ratio"] > 0.35:
                    score += 0.7
                if visual_features["texture_complexity"] < 80:
                    score += 0.2
                if food_type == "pasta" and visual_features["yellow_ratio"] > 0.1:
                    score += 0.1
            
            food_scores[food_type] = score
        
        # Return the highest scoring food type
        if food_scores:
            best_food = max(food_scores, key=food_scores.get)
            best_score = food_scores[best_food]
            
            if best_score > 0.6:
                return best_food
        
        # Fallback classification
        if visual_features["green_ratio"] > 0.2:
            return "vegetables"
        elif visual_features["brown_ratio"] > 0.25:
            return "cooked food"
        elif visual_features["white_ratio"] > 0.3:
            return "rice"
        else:
            return "food item"

# Global enhanced recognizer
enhanced_recognizer = EnhancedFoodRecognizer()

def get_food_from_apis(image_b64: str) -> Optional[Tuple[str, float]]:
    """Enhanced food recognition using Google Vision API"""
    
    # Try Google Vision API for accurate food detection
    vision_result = enhanced_recognizer.analyze_with_google_vision(image_b64)
    
    if vision_result:
        return (vision_result, 0.90)
    
    # If no API available, use None to trigger visual analysis
    return None

def get_enhanced_food_classification(visual_features: Dict) -> Tuple[str, float]:
    """Get enhanced food classification with confidence"""
    
    food_name = enhanced_recognizer.classify_by_common_patterns(visual_features)
    
    # Calculate confidence based on feature strength
    confidence = 0.7
    
    # Strong indicators boost confidence
    max_ratio = max(visual_features["red_ratio"], visual_features["green_ratio"], 
                   visual_features["brown_ratio"], visual_features["white_ratio"])
    
    if max_ratio > 0.4:
        confidence += 0.15
    elif max_ratio > 0.25:
        confidence += 0.08
    
    if visual_features["texture_complexity"] > 200:
        confidence += 0.1
    elif visual_features["texture_complexity"] > 100:
        confidence += 0.05
    
    return (food_name, min(confidence, 0.95))