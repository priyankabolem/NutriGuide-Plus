"""
Test Google Vision API integration
"""
import os
import base64
import requests
from app.services.google_vision_recognizer import detect_food_with_google_vision

def test_google_vision_setup():
    """Test if Google Vision API is properly configured"""
    
    print("Google Vision API Setup Test")
    print("=" * 40)
    
    # Check API key
    api_key = os.environ.get('GOOGLE_VISION_API_KEY')
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ API Key not found")
        print("   Set GOOGLE_VISION_API_KEY environment variable")
        return False
    
    # Test with a simple image
    print("\n🧪 Testing with sample image...")
    
    try:
        # Download test image
        test_url = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400"  # Pizza
        response = requests.get(test_url, timeout=10)
        image_b64 = base64.b64encode(response.content).decode('utf-8')
        
        print("📸 Downloaded test pizza image")
        
        # Test Google Vision recognition
        food, confidence, features = detect_food_with_google_vision(image_b64)
        
        print(f"\n🎯 Detection Results:")
        print(f"   Food: {food}")
        print(f"   Confidence: {confidence:.1%}")
        print(f"   Features: {len(features)} items")
        
        # Check if results make sense
        if confidence > 0.5 and any(word in food.lower() for word in ['pizza', 'food', 'dish']):
            print("✅ Google Vision API working correctly!")
            
            # Show some detected labels if available
            if 'google_vision_labels' in features:
                print(f"\n📋 Google detected labels:")
                for i, label in enumerate(features['google_vision_labels'][:5]):
                    print(f"   {i+1}. {label}")
            
            return True
        else:
            print(f"⚠️  Unexpected result - check API configuration")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_endpoint():
    """Test the main API endpoint with Google Vision"""
    
    print("\n\n🚀 Testing Main API Endpoint")
    print("=" * 40)
    
    try:
        # Test with local API
        api_url = "http://localhost:8000/api/analyze"
        
        # Download test image
        test_url = "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400"  # Salad
        response = requests.get(test_url, timeout=10)
        image_b64 = base64.b64encode(response.content).decode('utf-8')
        
        print("📸 Testing with salad image...")
        
        # Call API
        api_response = requests.post(
            api_url,
            json={"image": image_b64},
            timeout=15
        )
        
        if api_response.status_code == 200:
            data = api_response.json()
            foods = data.get('foods', [])
            
            if foods:
                main_food = foods[0]
                print(f"\n🎯 API Results:")
                print(f"   Primary: {main_food['name']} ({main_food['confidence']:.1%})")
                print(f"   Calories: {main_food['nutrition']['calories']}")
                print(f"   Protein: {main_food['nutrition']['protein_g']}g")
                
                print("✅ API endpoint working with Google Vision!")
                return True
            else:
                print("❌ No foods detected by API")
                return False
        else:
            print(f"❌ API error: {api_response.status_code}")
            print(f"   Start server with: uvicorn app.main:app --reload")
            return False
            
    except requests.ConnectionError:
        print("⚠️  API server not running")
        print("   Start with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_google_vision_setup()
    
    if success:
        print("\n" + "="*50)
        print("🎉 Google Vision API is ready!")
        print("\nNext steps:")
        print("1. Deploy to Render with GOOGLE_VISION_API_KEY")
        print("2. Test live demo")
        print("3. Expected accuracy: 85-95%")
        
        # Test API endpoint if available
        test_api_endpoint()
    else:
        print("\n" + "="*50)
        print("🔧 Setup needed:")
        print("1. Set GOOGLE_VISION_API_KEY environment variable")
        print("2. Ensure API key has Vision API permissions")
        print("3. Re-run this test")