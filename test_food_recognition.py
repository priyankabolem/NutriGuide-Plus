"""
Test food recognition accuracy with different approaches
"""
import base64
import requests
from pathlib import Path
import json
from typing import Dict, List, Tuple
import time

# Test with sample food images
TEST_IMAGES = {
    "pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
    "salad": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", 
    "burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
    "sushi": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400",
    "pasta": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400",
    "steak": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400",
    "rice": "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400",
    "fruit": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400",
    "chicken": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400",
    "soup": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"
}

def download_and_encode_image(url: str) -> str:
    """Download image from URL and encode to base64"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def test_recognition_methods():
    """Test different recognition methods and compare accuracy"""
    
    # Import recognition methods
    try:
        from app.services.robust_food_detection import get_robust_food_detection
        from app.services.google_vision_recognizer import detect_food_with_google_vision
        from app.services.color_histogram_analyzer import analyze_food_with_color_histograms
        from app.services.hybrid_food_recognizer import recognize_food_hybrid
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running from the project root directory")
        return
    
    results = {}
    
    print("Testing Food Recognition Methods")
    print("=" * 50)
    
    for expected_food, image_url in TEST_IMAGES.items():
        print(f"\nTesting: {expected_food}")
        print("-" * 30)
        
        # Download and encode image
        image_b64 = download_and_encode_image(image_url)
        if not image_b64:
            continue
        
        results[expected_food] = {}
        
        # Test 1: Robust Detection (current)
        try:
            start = time.time()
            food, confidence, features = get_robust_food_detection(image_b64)
            elapsed = time.time() - start
            results[expected_food]['robust'] = {
                'detected': food,
                'confidence': confidence,
                'time': elapsed,
                'correct': expected_food in food.lower()
            }
            print(f"Robust Detection: {food} ({confidence:.2f}) - {elapsed:.2f}s")
        except Exception as e:
            print(f"Robust Detection Error: {e}")
            results[expected_food]['robust'] = {'error': str(e)}
        
        # Test 2: Google Vision (if available)
        try:
            start = time.time()
            food, confidence, features = detect_food_with_google_vision(image_b64)
            elapsed = time.time() - start
            results[expected_food]['google_vision'] = {
                'detected': food,
                'confidence': confidence,
                'time': elapsed,
                'correct': expected_food in food.lower()
            }
            print(f"Google Vision: {food} ({confidence:.2f}) - {elapsed:.2f}s")
        except Exception as e:
            print(f"Google Vision Error: {e}")
            results[expected_food]['google_vision'] = {'error': str(e)}
        
        # Test 3: Color Histogram
        try:
            start = time.time()
            food, confidence, features = analyze_food_with_color_histograms(image_b64)
            elapsed = time.time() - start
            results[expected_food]['color_histogram'] = {
                'detected': food,
                'confidence': confidence,
                'time': elapsed,
                'correct': expected_food in food.lower()
            }
            print(f"Color Histogram: {food} ({confidence:.2f}) - {elapsed:.2f}s")
        except Exception as e:
            print(f"Color Histogram Error: {e}")
            results[expected_food]['color_histogram'] = {'error': str(e)}
        
        # Test 4: Hybrid Approach
        try:
            start = time.time()
            food, confidence, detailed = recognize_food_hybrid(image_b64)
            elapsed = time.time() - start
            results[expected_food]['hybrid'] = {
                'detected': food,
                'confidence': confidence,
                'time': elapsed,
                'correct': expected_food in food.lower(),
                'consensus': detailed.get('consensus_level', 'unknown')
            }
            print(f"Hybrid: {food} ({confidence:.2f}) - {elapsed:.2f}s")
            print(f"  Consensus: {detailed.get('consensus_level', 'unknown')}")
        except Exception as e:
            print(f"Hybrid Error: {e}")
            results[expected_food]['hybrid'] = {'error': str(e)}
    
    # Calculate accuracy statistics
    print("\n\nAccuracy Summary")
    print("=" * 50)
    
    methods = ['robust', 'google_vision', 'color_histogram', 'hybrid']
    for method in methods:
        correct = 0
        total = 0
        total_confidence = 0
        total_time = 0
        
        for food, method_results in results.items():
            if method in method_results and 'correct' in method_results[method]:
                total += 1
                if method_results[method]['correct']:
                    correct += 1
                total_confidence += method_results[method]['confidence']
                total_time += method_results[method]['time']
        
        if total > 0:
            accuracy = (correct / total) * 100
            avg_confidence = total_confidence / total
            avg_time = total_time / total
            
            print(f"\n{method.upper()}:")
            print(f"  Accuracy: {accuracy:.1f}% ({correct}/{total})")
            print(f"  Avg Confidence: {avg_confidence:.2f}")
            print(f"  Avg Time: {avg_time:.2f}s")
    
    # Save detailed results
    with open('recognition_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nDetailed results saved to recognition_test_results.json")

def test_local_api():
    """Test the local API endpoint"""
    print("\n\nTesting Local API")
    print("=" * 50)
    
    api_url = "http://localhost:8000/api/analyze"
    
    for expected_food, image_url in list(TEST_IMAGES.items())[:3]:  # Test first 3
        print(f"\nTesting API with: {expected_food}")
        
        # Download image
        image_b64 = download_and_encode_image(image_url)
        if not image_b64:
            continue
        
        # Call API
        try:
            response = requests.post(
                api_url,
                json={"image": image_b64},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                foods = data.get('foods', [])
                if foods:
                    print(f"  Detected: {foods[0]['name']} ({foods[0]['confidence']:.2f})")
                    print(f"  Calories: {foods[0]['nutrition']['calories']}")
            else:
                print(f"  API Error: {response.status_code}")
                
        except Exception as e:
            print(f"  API Error: {e}")

if __name__ == "__main__":
    test_recognition_methods()
    
    # Uncomment to test API
    # test_local_api()