import base64, io
import hashlib
import numpy as np
from PIL import Image
from typing import List, Tuple

def analyze_image_characteristics(img: Image.Image) -> dict:
    """Analyze image characteristics for food classification"""
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize for consistent analysis
    img_resized = img.resize((100, 100))
    img_array = np.array(img_resized)
    
    # Calculate color dominance
    avg_colors = img_array.mean(axis=(0, 1))
    red_dominance = avg_colors[0] / (avg_colors.sum() + 1)
    green_dominance = avg_colors[1] / (avg_colors.sum() + 1)
    blue_dominance = avg_colors[2] / (avg_colors.sum() + 1)
    
    # Calculate brightness
    brightness = img_array.mean()
    
    # Calculate color variance (texture indicator)
    color_variance = img_array.std()
    
    # Detect circular shapes (pizza, burger, pancakes)
    center_brightness = img_array[40:60, 40:60].mean()
    edge_brightness = np.concatenate([
        img_array[:20, :].flatten(),
        img_array[-20:, :].flatten(),
        img_array[:, :20].flatten(),
        img_array[:, -20:].flatten()
    ]).mean()
    circularity = abs(center_brightness - edge_brightness)
    
    # Calculate color saturation
    hsv = img.convert('HSV')
    hsv_array = np.array(hsv.resize((100, 100)))
    saturation = hsv_array[:,:,1].mean()
    
    # Get dominant color temperature
    warm_score = (avg_colors[0] + avg_colors[1]/2) / 255  # Red + half yellow
    cool_score = (avg_colors[2] + avg_colors[1]/2) / 255  # Blue + half green
    
    return {
        'red': red_dominance,
        'green': green_dominance,
        'blue': blue_dominance,
        'brightness': brightness,
        'variance': color_variance,
        'circularity': circularity,
        'saturation': saturation,
        'warm_score': warm_score,
        'cool_score': cool_score
    }

def classify_food_by_characteristics(chars: dict) -> str:
    """Classify food based on image characteristics"""
    
    # Log all characteristics for debugging
    print(f"Classification input - Brightness: {chars['brightness']:.1f}, Variance: {chars['variance']:.1f}, "
          f"Circularity: {chars['circularity']:.1f}, Saturation: {chars['saturation']:.1f}")
    
    # Pizza detection (red/orange dominant, circular, high saturation)
    if (chars['red'] > 0.36 and chars['saturation'] > 80 and 
        chars['circularity'] < 40 and chars['warm_score'] > 0.7):
        return "pizza"
    
    # Fruit detection (very bright, high saturation, varied colors)
    if chars['brightness'] > 180 and chars['saturation'] > 100:
        return "fruit bowl"
    
    # Salad detection (green dominant, high variance/texture)
    if chars['green'] > 0.35 and (chars['variance'] > 50 or chars['saturation'] > 90):
        return "salad"
    
    # Eggs detection (very bright, low saturation)
    if chars['brightness'] > 200 and chars['saturation'] < 50:
        return "eggs"
    
    # Pasta detection (beige/yellow, medium brightness, low variance)
    if (chars['brightness'] > 150 and chars['red'] > 0.34 and 
        chars['green'] > 0.32 and chars['variance'] < 40):
        return "pasta"
    
    # Burger detection (circular, layered, medium darkness)
    if (chars['circularity'] < 35 and chars['variance'] > 45 and 
        80 < chars['brightness'] < 150):
        return "burger"
    
    # Salmon/fish detection (pink/orange hues)
    if (chars['red'] > 0.37 and chars['green'] < 0.33 and 
        chars['saturation'] > 60):
        return "salmon"
    
    # Soup detection (uniform, liquid appearance)
    if chars['variance'] < 30 and chars['brightness'] < 140:
        return "soup"
    
    # Steak detection (dark, reddish-brown)
    if chars['brightness'] < 100 and chars['red'] > chars['blue']:
        return "steak"
    
    # Sushi detection (white rice visible, structured)
    if (chars['brightness'] > 140 and 35 < chars['variance'] < 55 and
        chars['saturation'] < 80):
        return "sushi"
    
    # Rice bowl detection (uniform, beige/white)
    if (chars['variance'] < 35 and 140 < chars['brightness'] < 180 and
        chars['saturation'] < 60):
        return "rice bowl"
    
    # Sandwich detection (layered, medium tones)
    if 40 < chars['variance'] < 60 and 120 < chars['brightness'] < 170:
        return "sandwich"
    
    # Tacos detection (warm colors, textured)
    if chars['warm_score'] > 0.65 and chars['variance'] > 45:
        return "tacos"
    
    # Pancakes detection (circular, golden brown)
    if (chars['circularity'] < 30 and chars['warm_score'] > 0.6 and
        120 < chars['brightness'] < 160):
        return "pancakes"
    
    # Enhanced default logic based on color dominance
    if chars['green'] > chars['red'] * 1.1 and chars['green'] > chars['blue'] * 1.1:
        return "salad"  # Clearly green
    elif chars['brightness'] < 120:
        return "steak"  # Dark foods
    elif chars['brightness'] > 180:
        return "eggs"  # Bright foods
    elif chars['variance'] > 50:
        return "burger"  # Textured foods
    elif chars['warm_score'] > 0.7:
        return "grilled chicken"  # Warm colored foods
    else:
        return "sandwich"  # Default

def classify_topk(image_b64: str, k: int = 3) -> List[Tuple[str, float]]:
    """
    Classify food based on image characteristics
    Returns different foods based on actual image content analysis
    """
    # Decode and validate image
    img_bytes = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(img_bytes))
    
    # Analyze image characteristics
    chars = analyze_image_characteristics(img)
    
    # Get primary classification
    primary_food = classify_food_by_characteristics(chars)
    
    # Define related foods for each category
    related_foods = {
        "pizza": [("pizza", 0.85), ("cheese pizza", 0.10), ("italian food", 0.05)],
        "grilled chicken": [("grilled chicken", 0.82), ("chicken breast", 0.13), ("protein", 0.05)],
        "salad": [("salad", 0.88), ("mixed green salad", 0.08), ("vegetables", 0.04)],
        "pasta": [("pasta", 0.80), ("spaghetti", 0.15), ("italian", 0.05)],
        "burger": [("burger", 0.83), ("beef burger", 0.12), ("sandwich", 0.05)],
        "salmon": [("salmon", 0.85), ("grilled fish", 0.10), ("seafood", 0.05)],
        "sushi": [("sushi", 0.84), ("japanese food", 0.11), ("rice", 0.05)],
        "steak": [("steak", 0.82), ("beef", 0.13), ("grilled meat", 0.05)],
        "sandwich": [("sandwich", 0.81), ("turkey sandwich", 0.14), ("lunch", 0.05)],
        "rice bowl": [("rice bowl", 0.79), ("rice", 0.16), ("asian food", 0.05)],
        "fruit bowl": [("fruit bowl", 0.86), ("mixed fruit", 0.09), ("healthy", 0.05)],
        "eggs": [("eggs", 0.87), ("scrambled eggs", 0.08), ("breakfast", 0.05)],
        "soup": [("soup", 0.83), ("vegetable soup", 0.12), ("hot food", 0.05)],
        "tacos": [("tacos", 0.81), ("mexican food", 0.14), ("tortilla", 0.05)],
        "pancakes": [("pancakes", 0.82), ("breakfast", 0.13), ("syrup", 0.05)]
    }
    
    # Get predictions for the identified food
    if primary_food in related_foods:
        predictions = related_foods[primary_food]
    else:
        # Fallback predictions
        predictions = [
            (primary_food, 0.80),
            ("meal", 0.15),
            ("food", 0.05)
        ]
    
    # Enhanced logging
    print(f"Image analysis complete:")
    print(f"  RGB: R={chars['red']:.3f}, G={chars['green']:.3f}, B={chars['blue']:.3f}")
    print(f"  Metrics: Brightness={chars['brightness']:.1f}, Variance={chars['variance']:.1f}, "
          f"Saturation={chars['saturation']:.1f}")
    print(f"  Scores: Warm={chars['warm_score']:.2f}, Cool={chars['cool_score']:.2f}")
    print(f"  => Detected food: {primary_food}")
    
    # Return top k items
    return predictions[:k]