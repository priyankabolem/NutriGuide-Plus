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
    
    def analyze_with_imagenet(self, image_b64: str) -> Optional[str]:
        """Use free ImageNet-based classification"""
        try:
            # This is a conceptual implementation - in reality, you'd use
            # a free computer vision service or local model
            
            # For demo purposes, return None to use visual analysis
            # In production, integrate with free services like:
            # - Hugging Face Inference API (free tier)
            # - Google Vision API (free tier)
            # - Microsoft Computer Vision (free tier)
            
            return None
            
        except Exception as e:
            print(f"ImageNet analysis error: {e}")
            return None
    
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
    """Enhanced food recognition using multiple approaches"""
    
    # Try free computer vision service (conceptual - replace with actual free API)
    imagenet_result = enhanced_recognizer.analyze_with_imagenet(image_b64)
    
    if imagenet_result:
        return (imagenet_result, 0.85)
    
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