"""
Verify Google Vision API is working in production
"""
import requests
import json

def test_production_api(api_url: str):
    """Test the production API endpoints"""
    
    print("🔍 NutriGuide+ Production Verification")
    print("=" * 50)
    
    # Remove trailing slash
    api_url = api_url.rstrip('/')
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Features: {json.dumps(data.get('features', {}), indent=6)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Debug status
    print("\n2. Checking Google Vision API status...")
    try:
        response = requests.get(f"{api_url}/debug/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # API Key Status
            api_key_status = data.get('api_key_status', {})
            print(f"   API Key Configured: {'✓' if api_key_status.get('configured') else '✗'}")
            if api_key_status.get('configured'):
                print(f"   API Key: {api_key_status.get('prefix')}...{api_key_status.get('suffix')}")
            
            # Google Vision Test
            gv_test = data.get('google_vision_test', {})
            if gv_test.get('status') == 'tested':
                print(f"   API Key Valid: {'✓' if gv_test.get('api_key_valid') else '✗'}")
                if gv_test.get('error'):
                    print(f"   Error: {gv_test['error']}")
            
            # Environment
            print(f"   Platform: {data.get('deployment_info', {}).get('platform')}")
            
    except Exception as e:
        print(f"   ❌ Error accessing debug endpoint: {e}")
    
    # Test 3: Test vision methods
    print("\n3. Testing vision methods with sample image...")
    try:
        response = requests.post(
            f"{api_url}/debug/test-vision",
            json={},  # Uses default test image
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            methods = data.get('methods_tested', {})
            
            # Google Vision results
            gv = methods.get('google_vision_direct', {})
            if gv.get('success'):
                print(f"   ✓ Google Vision: {gv['food']} ({gv['confidence']:.1%})")
                print(f"     API Available: {gv.get('api_available')}")
                if gv.get('labels'):
                    print(f"     Labels: {', '.join(gv['labels'][:3])}")
            else:
                print(f"   ✗ Google Vision: {gv.get('error', 'Failed')}")
            
            # Main classifier results
            main = methods.get('classify_topk', {})
            if main.get('success'):
                primary = main['results'][0] if main.get('results') else {}
                print(f"   ✓ Main Classifier: {primary.get('food')} ({primary.get('confidence', 0):.1%})")
            else:
                print(f"   ✗ Main Classifier: {main.get('error', 'Failed')}")
                
    except Exception as e:
        print(f"   ❌ Error testing vision: {e}")
    
    # Test 4: Live analysis
    print("\n4. Testing live analysis endpoint...")
    try:
        # Use a small test image
        test_payload = {
            "image_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "notes": "test"
        }
        
        response = requests.post(
            f"{api_url}/analyze",
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            profile = data.get('profile', {})
            print(f"   ✓ Analysis successful")
            print(f"     Food: {profile.get('name')}")
            print(f"     Method: Check logs above for details")
        else:
            print(f"   ✗ Analysis failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("\n📊 Summary:")
    print("If Google Vision is not being used despite API key being configured:")
    print("1. Check that GOOGLE_VISION_API_KEY is set in Render environment")
    print("2. Verify the API key has Vision API enabled in Google Cloud Console")
    print("3. Check server logs for any error messages")
    print("4. Ensure the latest code is deployed")

if __name__ == "__main__":
    # Test local
    print("Testing LOCAL API...")
    test_production_api("http://localhost:8000")
    
    print("\n\n")
    
    # Test production
    production_url = input("Enter your production API URL (e.g., https://nutriguide-plus-api.onrender.com): ").strip()
    if production_url:
        print(f"\nTesting PRODUCTION API at {production_url}...")
        test_production_api(production_url)