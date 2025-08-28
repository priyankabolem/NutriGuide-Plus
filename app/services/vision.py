import base64, io
import hashlib
from PIL import Image
from typing import List, Tuple

def classify_topk(image_b64: str, k: int = 3) -> List[Tuple[str, float]]:
    """
    Simulate food classification based on image hash
    Returns different foods based on image content
    """
    # Decode and validate image
    img_bytes = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(img_bytes))
    
    # Create hash from image to generate consistent but varied results
    img_hash = hashlib.md5(img_bytes).hexdigest()
    hash_int = int(img_hash[:8], 16)
    
    # Log for debugging (remove in production)
    print(f"Image hash: {img_hash[:8]}, hash_int: {hash_int}")
    
    # Food database with nutrition-appropriate items
    food_options = [
        [("grilled chicken", 0.85), ("chicken breast", 0.12), ("protein", 0.03)],
        [("pizza", 0.78), ("cheese pizza", 0.15), ("italian food", 0.07)],
        [("salmon", 0.82), ("grilled fish", 0.14), ("seafood", 0.04)],
        [("pasta", 0.75), ("spaghetti", 0.18), ("italian", 0.07)],
        [("burger", 0.80), ("beef burger", 0.15), ("fast food", 0.05)],
        [("salad", 0.88), ("green salad", 0.09), ("vegetables", 0.03)],
        [("sushi", 0.83), ("japanese food", 0.12), ("rice", 0.05)],
        [("steak", 0.79), ("beef", 0.16), ("grilled meat", 0.05)],
        [("sandwich", 0.84), ("turkey sandwich", 0.11), ("lunch", 0.05)],
        [("rice bowl", 0.76), ("rice", 0.19), ("asian food", 0.05)],
        [("tacos", 0.81), ("mexican food", 0.14), ("tortilla", 0.05)],
        [("soup", 0.77), ("vegetable soup", 0.18), ("hot food", 0.05)],
        [("eggs", 0.86), ("scrambled eggs", 0.10), ("breakfast", 0.04)],
        [("pancakes", 0.82), ("breakfast", 0.13), ("syrup", 0.05)],
        [("fruit bowl", 0.84), ("mixed fruit", 0.11), ("healthy", 0.05)]
    ]
    
    # Select food based on hash
    selected_idx = hash_int % len(food_options)
    selected_foods = food_options[selected_idx]
    
    # Log selected food for debugging
    print(f"Selected index: {selected_idx}, food: {selected_foods[0][0]}")
    
    # Return top k items
    return selected_foods[:k]