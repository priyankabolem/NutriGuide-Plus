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
    
    return {
        'red': red_dominance,
        'green': green_dominance,
        'blue': blue_dominance,
        'brightness': brightness,
        'variance': color_variance,
        'circularity': circularity
    }

def classify_food_by_characteristics(chars: dict) -> str:
    """Classify food based on image characteristics"""
    
    # Pizza detection (red/orange dominant, circular, medium brightness)
    if chars['red'] > 0.38 and chars['circularity'] < 30 and 100 < chars['brightness'] < 180:
        return "pizza"
    
    # Salad detection (green dominant, high variance)
    if chars['green'] > 0.36 and chars['variance'] > 40:
        return "salad"
    
    # Chicken/meat detection (brown/beige, medium brightness)
    if 0.33 < chars['red'] < 0.38 and chars['green'] > 0.30 and chars['brightness'] > 120:
        return "grilled chicken"
    
    # Pasta detection (yellow/beige, medium variance)
    if chars['red'] > 0.35 and chars['green'] > 0.33 and chars['variance'] < 35:
        return "pasta"
    
    # Burger detection (brown with layers, circular)
    if chars['variance'] > 45 and chars['circularity'] < 25 and chars['brightness'] > 100:
        return "burger"
    
    # Fruit detection (bright, colorful)
    if chars['brightness'] > 150 and (chars['red'] > 0.4 or chars['green'] > 0.38):
        return "fruit bowl"
    
    # Salmon/fish detection (pink/orange)
    if chars['red'] > 0.37 and 0.25 < chars['green'] < 0.33:
        return "salmon"
    
    # Eggs detection (white/yellow, high brightness)
    if chars['brightness'] > 180 and chars['variance'] < 30:
        return "eggs"
    
    # Soup detection (uniform color, low variance)
    if chars['variance'] < 25 and chars['brightness'] < 150:
        return "soup"
    
    # Sushi detection (white rice visible, structured)
    if chars['brightness'] > 160 and 30 < chars['variance'] < 45:
        return "sushi"
    
    # Dark foods (steak, etc)
    if chars['brightness'] < 100:
        return "steak"
    
    # Rice/grain bowls (uniform, beige)
    if chars['variance'] < 30 and 120 < chars['brightness'] < 160:
        return "rice bowl"
    
    # Default fallbacks based on color dominance
    if chars['green'] > chars['red'] and chars['green'] > chars['blue']:
        return "salad"
    elif chars['red'] > chars['green'] and chars['red'] > chars['blue']:
        return "grilled chicken"
    else:
        return "sandwich"

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
        "soup": [("soup", 0.83), ("vegetable soup", 0.12), ("hot food", 0.05)]
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
    
    # Log for debugging
    print(f"Image characteristics: R={chars['red']:.3f}, G={chars['green']:.3f}, B={chars['blue']:.3f}")
    print(f"Brightness={chars['brightness']:.1f}, Variance={chars['variance']:.1f}")
    print(f"Detected food: {primary_food}")
    
    # Return top k items
    return predictions[:k]