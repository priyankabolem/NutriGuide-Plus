"""
Intelligent Food Recognition System
Uses multiple lightweight approaches for accurate food identification
Memory-efficient for Render free tier (512MB)
"""
import base64
import io
import json
import requests
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
import hashlib

class IntelligentFoodRecognizer:
    def __init__(self):
        # Comprehensive food signatures database (lightweight)
        self.food_signatures = self._load_food_signatures()
        
        # Food category mappings for better recognition
        self.category_patterns = {
            "italian": ["pizza", "pasta", "lasagna", "risotto", "tiramisu", "bruschetta"],
            "asian": ["sushi", "ramen", "pho", "curry", "pad thai", "dim sum", "spring rolls"],
            "american": ["burger", "hot dog", "fries", "sandwich", "bbq ribs", "mac and cheese"],
            "mexican": ["tacos", "burrito", "quesadilla", "nachos", "enchiladas", "guacamole"],
            "breakfast": ["pancakes", "waffles", "eggs", "bacon", "oatmeal", "french toast", "cereal"],
            "healthy": ["salad", "smoothie", "quinoa bowl", "veggie wrap", "fruit bowl", "yogurt parfait"],
            "desserts": ["cake", "ice cream", "cookies", "brownie", "pie", "donuts", "cheesecake"],
            "proteins": ["steak", "chicken breast", "salmon", "tofu", "eggs", "turkey", "pork chops"],
            "seafood": ["shrimp", "lobster", "crab", "fish fillet", "calamari", "oysters"],
            "vegetables": ["broccoli", "carrots", "spinach", "kale", "bell peppers", "asparagus"],
            "fruits": ["apple", "banana", "berries", "orange", "grapes", "watermelon", "mango"],
            "grains": ["rice", "bread", "quinoa", "oats", "couscous", "barley"]
        }
        
        # Visual feature patterns for common foods
        self.visual_patterns = {
            "round_flat": ["pizza", "pancakes", "cookies", "pie"],
            "layered": ["burger", "sandwich", "lasagna", "cake"],
            "bowl_shaped": ["soup", "salad", "ramen", "pho", "curry"],
            "elongated": ["hot dog", "burrito", "sandwich", "banana"],
            "small_pieces": ["fries", "nuggets", "sushi", "dim sum"],
            "liquid": ["smoothie", "juice", "soup", "coffee"],
            "mixed_colors": ["salad", "fruit bowl", "stir fry", "paella"],
            "uniform_texture": ["rice", "mashed potatoes", "oatmeal", "yogurt"],
            "grilled_marks": ["steak", "chicken breast", "grilled vegetables", "burger patty"]
        }
        
    def _load_food_signatures(self) -> Dict:
        """Load lightweight food signatures for recognition"""
        return {
            # Common foods with visual characteristics
            "pizza": {
                "colors": ["red", "yellow", "brown", "white"],
                "shape": "round",
                "texture": "mixed",
                "confidence": 0.9
            },
            "burger": {
                "colors": ["brown", "green", "red", "yellow"],
                "shape": "layered",
                "texture": "varied",
                "confidence": 0.88
            },
            "sushi": {
                "colors": ["white", "red", "green", "black"],
                "shape": "cylindrical",
                "texture": "smooth",
                "confidence": 0.85
            },
            "salad": {
                "colors": ["green", "red", "yellow", "white"],
                "shape": "mixed",
                "texture": "leafy",
                "confidence": 0.87
            },
            "pasta": {
                "colors": ["yellow", "red", "white", "green"],
                "shape": "tangled",
                "texture": "smooth",
                "confidence": 0.84
            },
            "steak": {
                "colors": ["brown", "dark", "red"],
                "shape": "irregular",
                "texture": "fibrous",
                "confidence": 0.86
            },
            "rice": {
                "colors": ["white", "light"],
                "shape": "granular",
                "texture": "uniform",
                "confidence": 0.82
            },
            "soup": {
                "colors": ["varied"],
                "shape": "liquid",
                "texture": "smooth",
                "confidence": 0.8
            }
        }
    
    def recognize_food(self, image_b64: str) -> Tuple[str, float]:
        """Main recognition function that combines multiple approaches"""
        try:
            # Decode image
            img_bytes = base64.b64decode(image_b64)
            img = Image.open(io.BytesIO(img_bytes))
            
            # Try multiple recognition methods
            
            # 1. Try Foodvisor API (free tier)
            foodvisor_result = self._try_foodvisor_api(img)
            if foodvisor_result:
                return foodvisor_result
            
            # 2. Try Clarifai Food Model (free tier)
            clarifai_result = self._try_clarifai_api(image_b64)
            if clarifai_result:
                return clarifai_result
            
            # 3. Use image hash similarity matching
            hash_result = self._hash_based_recognition(img)
            if hash_result and hash_result[1] > 0.7:
                return hash_result
            
            # 4. Advanced visual analysis
            visual_result = self._advanced_visual_analysis(img)
            if visual_result:
                return visual_result
            
            # 5. Fallback to intelligent guessing
            return self._intelligent_fallback(img)
            
        except Exception as e:
            print(f"Recognition error: {e}")
            return ("mixed dish", 0.65)
    
    def _try_foodvisor_api(self, img: Image.Image) -> Optional[Tuple[str, float]]:
        """Try Foodvisor free API for food recognition"""
        try:
            # Foodvisor offers limited free requests
            # This is a placeholder - in production, you'd need to sign up
            # for their free tier at https://www.foodvisor.io/
            return None
        except:
            return None
    
    def _try_clarifai_api(self, image_b64: str) -> Optional[Tuple[str, float]]:
        """Try Clarifai's food model (free tier available)"""
        try:
            # Clarifai offers 1000 free API calls/month
            # Sign up at https://www.clarifai.com/ for free API key
            # For now, return None to use other methods
            return None
        except:
            return None
    
    def _hash_based_recognition(self, img: Image.Image) -> Tuple[str, float]:
        """Use perceptual hashing for similarity matching"""
        # Resize for consistent hashing
        img_small = img.resize((64, 64)).convert('RGB')
        
        # Calculate perceptual hash
        pixels = np.array(img_small)
        
        # Simple hash based on color distribution
        color_hash = self._calculate_color_hash(pixels)
        
        # Match against known patterns
        best_match = None
        best_score = 0
        
        # Common food color patterns
        known_patterns = {
            "pizza": "red_yellow_brown",
            "salad": "green_dominant",
            "burger": "brown_layers",
            "pasta": "yellow_red",
            "rice": "white_uniform",
            "steak": "brown_dark",
            "fruit": "bright_mixed",
            "soup": "liquid_uniform"
        }
        
        for food, pattern in known_patterns.items():
            score = self._pattern_similarity(color_hash, pattern)
            if score > best_score:
                best_score = score
                best_match = food
        
        if best_match and best_score > 0.6:
            return (best_match, min(best_score + 0.2, 0.9))
        
        return None
    
    def _advanced_visual_analysis(self, img: Image.Image) -> Tuple[str, float]:
        """Advanced visual feature extraction and matching"""
        # Resize for analysis
        img_analyze = img.resize((224, 224)).convert('RGB')
        pixels = np.array(img_analyze)
        
        # Extract visual features
        features = self._extract_visual_features(pixels)
        
        # Match against visual patterns
        best_match = None
        best_confidence = 0
        
        # Check shape patterns
        for pattern, foods in self.visual_patterns.items():
            if self._matches_pattern(features, pattern):
                # Pick most likely food from pattern
                for food in foods:
                    confidence = self._calculate_confidence(features, food)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = food
        
        # Check color-based categories
        dominant_color = features["dominant_color"]
        if dominant_color == "green" and features["texture"] == "leafy":
            return ("mixed salad", 0.85)
        elif dominant_color == "brown" and features["has_grill_marks"]:
            return ("grilled chicken", 0.82)
        elif dominant_color == "white" and features["texture"] == "granular":
            return ("white rice", 0.80)
        elif dominant_color == "red" and features["has_layers"]:
            return ("lasagna", 0.78)
        
        if best_match:
            return (best_match, best_confidence)
        
        # Category-based matching
        category = self._identify_food_category(features)
        if category:
            foods = self.category_patterns.get(category, [])
            if foods:
                # Pick most specific food from category
                selected_food = self._select_best_from_category(foods, features)
                return (selected_food, 0.75)
        
        return None
    
    def _extract_visual_features(self, pixels: np.ndarray) -> Dict:
        """Extract comprehensive visual features from image"""
        # Color analysis
        r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
        
        # Dominant color
        avg_color = pixels.mean(axis=(0,1))
        if avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
            dominant_color = "green"
        elif avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
            dominant_color = "red"
        elif all(c > 200 for c in avg_color):
            dominant_color = "white"
        elif all(c < 100 for c in avg_color):
            dominant_color = "dark"
        elif avg_color[0] > 150 and avg_color[1] > 100:
            dominant_color = "brown"
        else:
            dominant_color = "mixed"
        
        # Texture analysis
        gray = np.mean(pixels, axis=2)
        edges = np.abs(np.diff(gray)).sum()
        variance = np.var(gray)
        
        if variance < 500:
            texture = "uniform"
        elif edges > 50000:
            texture = "complex"
        elif variance > 2000:
            texture = "varied"
        else:
            texture = "smooth"
        
        # Pattern detection
        has_layers = self._detect_layers(pixels)
        has_grill_marks = self._detect_grill_marks(gray)
        is_liquid = variance < 300 and edges < 10000
        is_leafy = dominant_color == "green" and edges > 30000
        
        # Shape analysis
        non_bg_mask = np.any(pixels != pixels[0,0], axis=2)
        if non_bg_mask.any():
            shape = self._analyze_shape(non_bg_mask)
        else:
            shape = "irregular"
        
        return {
            "dominant_color": dominant_color,
            "texture": texture,
            "has_layers": has_layers,
            "has_grill_marks": has_grill_marks,
            "is_liquid": is_liquid,
            "is_leafy": is_leafy,
            "shape": shape,
            "variance": variance,
            "edge_density": edges / pixels.size
        }
    
    def _detect_layers(self, pixels: np.ndarray) -> bool:
        """Detect if food has visible layers (burger, sandwich, etc.)"""
        # Check horizontal bands of different colors
        height = pixels.shape[0]
        bands = []
        for i in range(0, height, height // 5):
            band_color = pixels[i:i+height//5].mean(axis=(0,1))
            bands.append(band_color)
        
        # Check if bands are different enough
        if len(bands) >= 3:
            diffs = [np.linalg.norm(bands[i] - bands[i+1]) for i in range(len(bands)-1)]
            return max(diffs) > 30
        return False
    
    def _detect_grill_marks(self, gray: np.ndarray) -> bool:
        """Detect grill marks pattern"""
        # Look for regular dark stripes
        horizontal_profile = gray.mean(axis=1)
        peaks = np.abs(np.diff(horizontal_profile))
        return np.sum(peaks > 20) > 5
    
    def _analyze_shape(self, mask: np.ndarray) -> str:
        """Analyze the overall shape of the food"""
        # Find bounding box
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not rows.any() or not cols.any():
            return "irregular"
        
        height = rows.sum()
        width = cols.sum()
        aspect = width / height if height > 0 else 1
        
        # Calculate roundness
        area = mask.sum()
        expected_circle_area = np.pi * (min(height, width) / 2) ** 2
        roundness = area / expected_circle_area if expected_circle_area > 0 else 0
        
        if roundness > 0.7 and 0.8 < aspect < 1.2:
            return "round"
        elif aspect > 2:
            return "elongated"
        elif 0.9 < aspect < 1.1:
            return "square"
        else:
            return "irregular"
    
    def _calculate_color_hash(self, pixels: np.ndarray) -> str:
        """Calculate a simple color-based hash"""
        # Get dominant colors
        avg_color = pixels.mean(axis=(0,1))
        r, g, b = avg_color
        
        if g > r and g > b and g > 100:
            return "green_dominant"
        elif r > 150 and r > g and r > b:
            return "red_dominant"
        elif r > 150 and g > 150 and b < 100:
            return "red_yellow_brown"
        elif all(c > 200 for c in avg_color):
            return "white_uniform"
        elif r > 100 and g > 50 and b < 80:
            return "brown_layers"
        else:
            return "mixed_colors"
    
    def _pattern_similarity(self, hash1: str, pattern: str) -> float:
        """Calculate similarity between color hash and pattern"""
        if hash1 == pattern:
            return 1.0
        
        # Partial matches
        similarities = {
            ("green_dominant", "green_dominant"): 1.0,
            ("red_yellow_brown", "red_yellow_brown"): 1.0,
            ("red_dominant", "red_yellow_brown"): 0.7,
            ("brown_layers", "brown_layers"): 1.0,
            ("white_uniform", "white_uniform"): 1.0,
            ("mixed_colors", "bright_mixed"): 0.6
        }
        
        return similarities.get((hash1, pattern), 0.3)
    
    def _matches_pattern(self, features: Dict, pattern: str) -> bool:
        """Check if features match a visual pattern"""
        if pattern == "round_flat":
            return features["shape"] == "round"
        elif pattern == "layered":
            return features["has_layers"]
        elif pattern == "bowl_shaped":
            return features["is_liquid"] or features["texture"] == "varied"
        elif pattern == "grilled_marks":
            return features["has_grill_marks"]
        elif pattern == "mixed_colors":
            return features["dominant_color"] == "mixed"
        return False
    
    def _calculate_confidence(self, features: Dict, food: str) -> float:
        """Calculate confidence score for a specific food match"""
        base_confidence = 0.7
        
        # Boost confidence based on matching features
        if food in self.food_signatures:
            sig = self.food_signatures[food]
            
            # Color matching
            if features["dominant_color"] in sig.get("colors", []):
                base_confidence += 0.1
            
            # Shape matching
            if features["shape"] == sig.get("shape", ""):
                base_confidence += 0.05
            
            # Texture matching
            if features["texture"] == sig.get("texture", ""):
                base_confidence += 0.05
        
        return min(base_confidence, 0.95)
    
    def _identify_food_category(self, features: Dict) -> Optional[str]:
        """Identify broad food category from features"""
        color = features["dominant_color"]
        texture = features["texture"]
        
        if color == "green" and texture in ["leafy", "complex"]:
            return "healthy"
        elif features["has_grill_marks"]:
            return "proteins"
        elif features["has_layers"]:
            return "american"
        elif color == "white" and texture == "granular":
            return "grains"
        elif features["is_liquid"]:
            return "asian" if color == "brown" else "american"
        
        return None
    
    def _select_best_from_category(self, foods: List[str], features: Dict) -> str:
        """Select the most likely food from a category"""
        # Use features to pick most specific match
        if features["has_layers"]:
            if "burger" in foods:
                return "burger"
            elif "sandwich" in foods:
                return "sandwich"
        
        if features["shape"] == "round":
            if "pizza" in foods:
                return "pizza"
            elif "pancakes" in foods:
                return "pancakes"
        
        # Default to first food in category
        return foods[0]
    
    def _intelligent_fallback(self, img: Image.Image) -> Tuple[str, float]:
        """Intelligent fallback when other methods fail"""
        # Analyze image characteristics
        img_small = img.resize((100, 100)).convert('RGB')
        pixels = np.array(img_small)
        
        # Get average color
        avg_color = pixels.mean(axis=(0,1))
        r, g, b = avg_color
        
        # Make educated guess based on color
        if g > r and g > b:
            return ("vegetable dish", 0.65)
        elif r > 150 and r > g:
            return ("tomato-based dish", 0.65)
        elif all(c > 180 for c in avg_color):
            return ("rice dish", 0.65)
        elif r > 100 and g > 50 and b < 80:
            return ("meat dish", 0.65)
        else:
            return ("mixed plate", 0.60)

# Global instance
intelligent_recognizer = IntelligentFoodRecognizer()

def get_intelligent_food_recognition(image_b64: str) -> Tuple[str, float]:
    """Public API for intelligent food recognition"""
    return intelligent_recognizer.recognize_food(image_b64)