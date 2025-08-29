"""
Hybrid Food Recognition System
Combines Google Vision API, Color Histogram Analysis, and Feature Matching
for maximum accuracy in food detection
"""
import base64
import os
from typing import Dict, List, Tuple, Optional
import numpy as np
from PIL import Image
import json

# Import our recognition modules
from .google_vision_recognizer import detect_food_with_google_vision
from .color_histogram_analyzer import analyze_food_with_color_histograms
from .robust_food_detection import get_robust_food_detection
from .food_recognizer import get_free_food_recognition

class HybridFoodRecognizer:
    def __init__(self):
        pass
        
        # Weight configuration for different methods
        self.method_weights = {
            'google_vision': 0.40,  # Highest weight for professional API
            'color_histogram': 0.25,  # Advanced color analysis
            'huggingface': 0.20,     # ML models
            'feature_matching': 0.15  # Basic feature matching
        }
        
        # Confidence thresholds
        self.high_confidence = 0.85
        self.medium_confidence = 0.70
        self.low_confidence = 0.60
        
        # Food name normalization mapping
        self.food_aliases = {
            "hamburger": "burger",
            "cheeseburger": "burger", 
            "beef burger": "burger",
            "french fries": "french fries",
            "fries": "french fries",
            "chips": "french fries",
            "spaghetti": "pasta",
            "noodles": "pasta",
            "fettuccine": "pasta",
            "linguine": "pasta",
            "beef": "steak",
            "ribeye": "steak",
            "sirloin": "steak",
            "chicken breast": "grilled chicken",
            "roasted chicken": "grilled chicken",
            "green salad": "salad",
            "caesar salad": "salad",
            "garden salad": "salad",
            "fruit salad": "fruit bowl",
            "mixed fruit": "fruit bowl",
            "white rice": "rice",
            "brown rice": "rice",
            "fried rice": "rice"
        }
        
    def recognize_food(self, image_b64: str) -> Tuple[str, float, Dict]:
        """
        Main recognition method that combines multiple approaches
        Returns: (food_name, confidence, detailed_results)
        """
        results = {}
        
        # 1. Try Google Vision API (if available)
        google_api_key = os.environ.get('GOOGLE_VISION_API_KEY')
        if google_api_key or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                gv_result = detect_food_with_google_vision(image_b64)
                results['google_vision'] = {
                    'food': self._normalize_food_name(gv_result[0]),
                    'confidence': gv_result[1],
                    'features': gv_result[2]
                }
                print(f"✓ Google Vision detected: {gv_result[0]} ({gv_result[1]:.2f})")
            except Exception as e:
                print(f"Google Vision error: {e}")
                results['google_vision'] = None
        else:
            print("⚠ Google Vision API not configured")
            results['google_vision'] = None
        
        # 2. Advanced Color Histogram Analysis
        try:
            color_result = analyze_food_with_color_histograms(image_b64)
            results['color_histogram'] = {
                'food': self._normalize_food_name(color_result[0]),
                'confidence': color_result[1],
                'features': color_result[2]
            }
        except Exception as e:
            print(f"Color histogram error: {e}")
            results['color_histogram'] = None
        
        # 3. HuggingFace ML Models
        try:
            hf_result = get_free_food_recognition(image_b64)
            results['huggingface'] = {
                'food': self._normalize_food_name(hf_result[0]),
                'confidence': hf_result[1],
                'features': hf_result[2] if len(hf_result) > 2 else {}
            }
        except Exception as e:
            print(f"HuggingFace error: {e}")
            results['huggingface'] = None
        
        # 4. Feature-based Detection
        try:
            feature_result = get_robust_food_detection(image_b64)
            results['feature_matching'] = {
                'food': self._normalize_food_name(feature_result[0]),
                'confidence': feature_result[1],
                'features': feature_result[2]
            }
        except Exception as e:
            print(f"Feature matching error: {e}")
            results['feature_matching'] = None
        
        # Combine results using weighted voting
        final_food, final_confidence = self._combine_results(results)
        
        # Prepare detailed results
        detailed_results = {
            'individual_results': results,
            'final_decision': {
                'food': final_food,
                'confidence': final_confidence,
                'method': self._get_primary_method(results, final_food)
            },
            'consensus_level': self._calculate_consensus(results),
            'all_predictions': self._get_all_predictions(results)
        }
        
        return (final_food, final_confidence, detailed_results)
    
    def _check_google_auth(self) -> bool:
        """Check if Google Cloud authentication is available"""
        try:
            from google.auth import default
            credentials, project = default()
            return credentials is not None
        except:
            return False
    
    def _normalize_food_name(self, food_name: str) -> str:
        """Normalize food names to consistent format"""
        if not food_name:
            return "unidentified food"
        
        food_lower = food_name.lower().strip()
        
        # Check aliases
        for alias, normalized in self.food_aliases.items():
            if alias in food_lower:
                return normalized
        
        # Remove common suffixes
        for suffix in [" dish", " plate", " bowl", " item", " food"]:
            if food_lower.endswith(suffix):
                food_lower = food_lower[:-len(suffix)].strip()
        
        return food_lower or food_name
    
    def _combine_results(self, results: Dict) -> Tuple[str, float]:
        """Combine results from multiple methods using weighted voting"""
        vote_scores = {}
        total_weight = 0
        
        # Collect weighted votes
        for method, weight in self.method_weights.items():
            if results.get(method) and results[method]:
                food = results[method]['food']
                confidence = results[method]['confidence']
                
                # Apply weight to confidence score
                weighted_score = confidence * weight
                
                if food not in vote_scores:
                    vote_scores[food] = 0
                vote_scores[food] += weighted_score
                total_weight += weight
        
        # Handle case where no methods succeeded
        if not vote_scores:
            return ("unidentified food", 0.50)
        
        # Normalize scores
        if total_weight > 0:
            for food in vote_scores:
                vote_scores[food] /= total_weight
        
        # Find best match
        best_food = max(vote_scores, key=vote_scores.get)
        base_confidence = vote_scores[best_food]
        
        # Boost confidence if multiple methods agree
        agreement_bonus = self._calculate_agreement_bonus(results, best_food)
        final_confidence = min(0.98, base_confidence + agreement_bonus)
        
        # Apply confidence threshold adjustments
        if final_confidence < self.low_confidence:
            # Low confidence - return generic category
            return self._get_generic_category(results), final_confidence
        
        return (best_food, final_confidence)
    
    def _calculate_agreement_bonus(self, results: Dict, target_food: str) -> float:
        """Calculate bonus confidence based on method agreement"""
        agreements = 0
        total_methods = 0
        
        for method, result in results.items():
            if result and result['confidence'] > 0.6:
                total_methods += 1
                if result['food'] == target_food:
                    agreements += 1
        
        if total_methods == 0:
            return 0.0
        
        agreement_rate = agreements / total_methods
        
        # Bonus structure
        if agreement_rate >= 0.75:  # 3/4 or 4/4 methods agree
            return 0.10
        elif agreement_rate >= 0.5:  # 2/4 methods agree
            return 0.05
        else:
            return 0.0
    
    def _get_primary_method(self, results: Dict, final_food: str) -> str:
        """Determine which method contributed most to final decision"""
        best_method = "ensemble"
        best_confidence = 0
        
        for method, result in results.items():
            if result and result['food'] == final_food:
                if result['confidence'] > best_confidence:
                    best_confidence = result['confidence']
                    best_method = method
        
        return best_method
    
    def _calculate_consensus(self, results: Dict) -> str:
        """Calculate consensus level among methods"""
        valid_results = [r for r in results.values() if r and r['confidence'] > 0.6]
        
        if len(valid_results) < 2:
            return "low"
        
        # Get all predicted foods
        foods = [r['food'] for r in valid_results]
        unique_foods = set(foods)
        
        if len(unique_foods) == 1:
            return "high"
        elif len(unique_foods) == 2:
            return "medium"
        else:
            return "low"
    
    def _get_all_predictions(self, results: Dict) -> List[Dict]:
        """Get all predictions sorted by confidence"""
        all_predictions = []
        
        for method, result in results.items():
            if result:
                all_predictions.append({
                    'method': method,
                    'food': result['food'],
                    'confidence': result['confidence']
                })
        
        # Sort by confidence
        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return all_predictions
    
    def _get_generic_category(self, results: Dict) -> str:
        """Return generic food category when confidence is low"""
        # Analyze features from all methods to determine category
        all_features = {}
        
        for method, result in results.items():
            if result and 'features' in result:
                all_features.update(result['features'])
        
        # Use dominant colors to guess category
        if 'dominant_colors' in all_features:
            colors = all_features['dominant_colors']
            if colors and len(colors) > 0:
                top_hsv = colors[0]['hsv']
                hue = top_hsv[0]
                
                if 80 <= hue <= 140:
                    return "vegetable dish"
                elif (0 <= hue <= 20) or (340 <= hue <= 360):
                    return "meat dish"
                elif 40 <= hue <= 60:
                    return "grain dish"
        
        # Default fallback
        return "mixed dish"

# Global instance
hybrid_recognizer = HybridFoodRecognizer()

def recognize_food_hybrid(image_b64: str) -> Tuple[str, float, Dict]:
    """
    Public API for hybrid food recognition
    Combines multiple methods for best accuracy
    """
    return hybrid_recognizer.recognize_food(image_b64)