"""
Google Vision API Food Recognition
Professional-grade food detection using Google's computer vision
Supports API key authentication for Render deployment
"""
import base64
import io
import json
import os
from typing import Dict, List, Tuple, Optional
import requests
import numpy as np
from PIL import Image

class GoogleVisionFoodRecognizer:
    def __init__(self):
        # Initialize Google Vision API
        self.api_key = os.environ.get('GOOGLE_VISION_API_KEY')
        
        if self.api_key:
            print("✓ Google Vision API key configured")
        else:
            print("⚠ Google Vision API key not found")
        
        # Food-related labels mapping to our database
        self.food_mappings = {
            "pizza": ["pizza", "pepperoni pizza", "cheese pizza", "pizza slice"],
            "burger": ["hamburger", "burger", "cheeseburger", "beef burger"],
            "pasta": ["pasta", "spaghetti", "noodles", "fettuccine", "penne"],
            "salad": ["salad", "green salad", "caesar salad", "garden salad"],
            "sushi": ["sushi", "sashimi", "maki", "nigiri", "sushi roll"],
            "rice": ["rice", "fried rice", "white rice", "brown rice"],
            "chicken": ["chicken", "grilled chicken", "fried chicken", "roasted chicken"],
            "steak": ["steak", "beef", "ribeye", "sirloin", "grilled beef"],
            "fish": ["fish", "grilled fish", "salmon", "tuna", "seafood"],
            "sandwich": ["sandwich", "sub", "panini", "wrap"],
            "soup": ["soup", "broth", "stew", "chowder"],
            "fruit": ["fruit", "fruit salad", "fruit bowl", "apple", "banana"],
            "vegetables": ["vegetables", "vegetable", "veggies", "greens"],
            "bread": ["bread", "toast", "baguette", "roll"],
            "eggs": ["eggs", "egg", "scrambled eggs", "fried egg", "omelet"],
            "pancakes": ["pancake", "pancakes", "waffle", "french toast"],
            "french fries": ["french fries", "fries", "chips", "potato fries"],
            "tacos": ["taco", "tacos", "burrito", "quesadilla"],
            "curry": ["curry", "indian food", "masala", "tikka"],
            "smoothie": ["smoothie", "juice", "shake", "beverage"]
        }
        
    def detect_food(self, image_b64: str) -> Tuple[str, float, Dict]:
        """Detect food using Google Vision API"""
        if not self.api_key:
            return self._fallback_detection(image_b64)
        
        try:
            # Call Google Vision API
            url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
            
            request_json = {
                "requests": [{
                    "image": {"content": image_b64},
                    "features": [
                        {"type": "LABEL_DETECTION", "maxResults": 25},
                        {"type": "OBJECT_LOCALIZATION", "maxResults": 15},
                        {"type": "WEB_DETECTION", "maxResults": 15}
                    ]
                }]
            }
            
            response = requests.post(url, json=request_json, timeout=15)
            
            if response.status_code != 200:
                print(f"Google Vision API error: {response.status_code}")
                return self._fallback_detection(image_b64)
            
            result = response.json()
            if 'responses' not in result or not result['responses']:
                return self._fallback_detection(image_b64)
            
            data = result['responses'][0]
            
            # Check for API errors
            if 'error' in data:
                print(f"Google Vision API error: {data['error']['message']}") 
                return self._fallback_detection(image_b64)
            
            # Extract detection results
            labels = data.get('labelAnnotations', [])
            objects = data.get('localizedObjectAnnotations', [])
            web_detection = data.get('webDetection', {})
            
            # Analyze and find best food match
            food_name, confidence = self._analyze_google_results(labels, objects, web_detection)
            
            # Extract additional features
            features = self._extract_features(image_b64, labels, objects)
            
            return (food_name, confidence, features)
            
        except Exception as e:
            print(f"Google Vision API error: {e}")
            return self._fallback_detection(image_b64)
    
    def _analyze_google_results(self, labels, objects, web_detection) -> Tuple[str, float]:
        """Analyze Google Vision results to identify food"""
        
        all_detections = []
        
        # Collect all food-related detections
        for label in labels:
            name = label.get('description', '').lower()
            score = label.get('score', 0)
            
            if self._is_food_related(name):
                all_detections.append({
                    'name': name,
                    'confidence': score,
                    'type': 'label'
                })
        
        for obj in objects:
            name = obj.get('name', '').lower()
            score = obj.get('score', 0)
            
            if self._is_food_related(name):
                all_detections.append({
                    'name': name,
                    'confidence': score,
                    'type': 'object'
                })
        
        # Web entities (often very accurate for food)
        web_entities = web_detection.get('webEntities', [])
        for entity in web_entities[:5]:  # Top 5 web entities
            name = entity.get('description', '').lower()
            score = entity.get('score', 0.8)  # Web entities are usually reliable
            
            if self._is_food_related(name):
                all_detections.append({
                    'name': name,
                    'confidence': score,
                    'type': 'web'
                })
        
        # Sort by confidence
        all_detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Find the best match
        for detection in all_detections:
            mapped_food = self._map_to_database_food(detection['name'])
            if mapped_food:
                confidence = min(detection['confidence'] * 1.1, 0.95)  # Boost mapped foods
                return (mapped_food, confidence)
        
        # If no direct mapping, use the most confident food label
        if all_detections:
            best = all_detections[0]
            clean_name = self._clean_food_name(best['name'])
            return (clean_name, best['confidence'])
        
        # Fallback to general analysis
        return self._analyze_general_labels(labels)
    
    def _is_food_related(self, text: str) -> bool:
        """Check if detected label is food-related"""
        food_keywords = [
            'food', 'dish', 'meal', 'cuisine', 'recipe', 'ingredient',
            'breakfast', 'lunch', 'dinner', 'snack', 'dessert', 'beverage',
            'fruit', 'vegetable', 'meat', 'seafood', 'dairy', 'grain',
            'pizza', 'burger', 'pasta', 'salad', 'sushi', 'rice', 'bread',
            'chicken', 'beef', 'pork', 'fish', 'egg', 'cheese', 'soup',
            'sandwich', 'taco', 'curry', 'noodle', 'cake', 'cookie'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in food_keywords)
    
    def _map_to_database_food(self, detected_name: str) -> Optional[str]:
        """Map Google Vision detection to foods in our database"""
        detected_lower = detected_name.lower()
        
        # Direct mapping
        for db_food, variations in self.food_mappings.items():
            for variation in variations:
                if variation in detected_lower or detected_lower in variation:
                    return db_food
        
        # Partial word matching
        detected_words = detected_lower.split()
        for db_food, variations in self.food_mappings.items():
            for variation in variations:
                variation_words = variation.split()
                if any(word in variation_words for word in detected_words):
                    return db_food
        
        return None
    
    def _clean_food_name(self, name: str) -> str:
        """Clean detected name to be database-friendly"""
        # Remove common non-food descriptors
        remove_words = ['food', 'dish', 'plate', 'bowl', 'cuisine', 'meal', 'recipe']
        
        name_lower = name.lower()
        for word in remove_words:
            name_lower = name_lower.replace(word, '').strip()
        
        # Check if cleaned name maps to database
        mapped = self._map_to_database_food(name_lower)
        return mapped or name_lower or "mixed dish"
    
    def _analyze_general_labels(self, labels) -> Tuple[str, float]:
        """Analyze general labels when no food-specific detection found"""
        if not labels:
            return ("unidentified dish", 0.5)
        
        # Use the most confident label
        top_label = labels[0]
        name = self._clean_food_name(top_label.get('description', ''))
        confidence = top_label.get('score', 0.5) * 0.7  # Reduce confidence for non-specific
        
        return (name, confidence)
    
    def _extract_features(self, image_b64: str, labels, objects) -> Dict:
        """Extract features from image and Google Vision results"""
        try:
            # Basic image features
            img_bytes = base64.b64decode(image_b64)
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            img_array = np.array(img.resize((224, 224)))
            
            features = {
                'google_vision_labels': [l.get('description') for l in labels[:10]],
                'google_vision_objects': [o.get('name') for o in objects[:5]],
                'label_scores': [l.get('score') for l in labels[:5]],
                'avg_color': img_array.mean(axis=(0, 1)).tolist(),
                'brightness': float(img_array.mean()),
                'contrast': float(img_array.std()),
                'api_available': True
            }
            
            return features
            
        except Exception as e:
            return {'api_available': True, 'feature_error': str(e)}
    
    def _fallback_detection(self, image_b64: str) -> Tuple[str, float, Dict]:
        """Fallback when Google Vision is not available"""
        try:
            # Simple image analysis
            img_bytes = base64.b64decode(image_b64)
            img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            img_array = np.array(img.resize((224, 224)))
            
            avg_color = img_array.mean(axis=(0, 1))
            features = {
                'avg_color': avg_color.tolist(),
                'brightness': float(img_array.mean()),
                'api_available': False
            }
            
            # Simple color-based classification
            if avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:  # Green
                return ("salad", 0.65, features)
            elif avg_color[0] > 150:  # Red
                return ("pizza", 0.60, features)
            elif all(c > 200 for c in avg_color):  # White
                return ("rice", 0.60, features)
            else:
                return ("mixed dish", 0.55, features)
                
        except Exception:
            return ("unidentified food", 0.50, {'api_available': False})

# Global instance
google_recognizer = GoogleVisionFoodRecognizer()

def detect_food_with_google_vision(image_b64: str) -> Tuple[str, float, Dict]:
    """Public API for Google Vision food detection"""
    return google_recognizer.detect_food(image_b64)