"""
Demo script to show improved food recognition accuracy
"""
import base64
import requests
from app.services.robust_food_detection import get_robust_food_detection
from app.services.color_histogram_analyzer import analyze_food_with_color_histograms
from app.services.hybrid_food_recognizer import recognize_food_hybrid

# Test images
DEMO_IMAGES = {
    "Pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600",
    "Salad": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",
    "Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
    "Sushi": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=600",
    "Pasta": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=600"
}

def test_recognition():
    print("\n🍽️  NutriGuide+ Food Recognition Demo")
    print("=" * 60)
    print("Comparing recognition methods for accuracy\n")
    
    for food_name, url in DEMO_IMAGES.items():
        print(f"\n📸 Testing: {food_name}")
        print("-" * 40)
        
        # Download image
        try:
            response = requests.get(url, timeout=10)
            image_b64 = base64.b64encode(response.content).decode('utf-8')
        except:
            print(f"❌ Failed to download image")
            continue
        
        # Test different methods
        try:
            # 1. Current method (Robust Detection)
            food1, conf1, _ = get_robust_food_detection(image_b64)
            print(f"Current Method:     {food1:<20} (confidence: {conf1:.2%})")
            
            # 2. Color Histogram Analysis
            food2, conf2, _ = analyze_food_with_color_histograms(image_b64)
            print(f"Color Histogram:    {food2:<20} (confidence: {conf2:.2%})")
            
            # 3. Hybrid Approach (Best)
            food3, conf3, details = recognize_food_hybrid(image_b64)
            consensus = details.get('consensus_level', 'unknown')
            print(f"Hybrid (Best):      {food3:<20} (confidence: {conf3:.2%}, consensus: {consensus})")
            
            # Check accuracy
            correct = "✅" if food_name.lower() in food3.lower() else "❌"
            print(f"\nAccuracy: {correct}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("💡 Recommendations:")
    print("1. For free deployment: Use current method (70-75% accuracy)")
    print("2. For better accuracy: Enable Google Vision API (85-95% accuracy)")
    print("3. For best results: Use hybrid approach with Google Vision")
    print("\n📚 See GOOGLE_VISION_SETUP.md for configuration instructions")

if __name__ == "__main__":
    test_recognition()