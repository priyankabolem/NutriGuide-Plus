"""
Test script to debug ChunkedEncodingError
"""
import requests
import base64
from PIL import Image
import io
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure session with retry
session = requests.Session()
retry = Retry(total=3, read=3, connect=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def test_api_connection():
    """Test API with a small sample image to isolate the issue"""
    
    print("Testing API Connection for ChunkedEncodingError")
    print("=" * 50)
    
    # Test 1: Health check
    api_url = "http://localhost:8000"
    try:
        print(f"\n1. Testing health endpoint...")
        response = session.get(f"{api_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Small image test
    print(f"\n2. Testing with small test image...")
    try:
        # Create a small test image (100x100 red square)
        test_img = Image.new('RGB', (100, 100), color='red')
        img_buffer = io.BytesIO()
        test_img.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)
        b64_image = base64.b64encode(img_buffer.read()).decode()
        
        print(f"   Image size: {len(b64_image)} bytes (base64)")
        
        # Test analyze endpoint
        payload = {"image_b64": b64_image, "notes": "test"}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }
        
        print(f"   Calling /analyze endpoint...")
        response = session.post(
            f"{api_url}/analyze",
            json=payload,
            headers=headers,
            timeout=30,
            stream=False
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Food detected: {data['profile']['name']}")
            print(f"   Response size: {len(response.content)} bytes")
        else:
            print(f"   Error: {response.text[:200]}...")
            
    except requests.exceptions.ChunkedEncodingError as e:
        print(f"   ChunkedEncodingError: {e}")
        print("   This is the error we're debugging!")
    except Exception as e:
        print(f"   Other error: {type(e).__name__}: {e}")
    
    # Test 3: Larger image test
    print(f"\n3. Testing with larger image from URL...")
    try:
        # Download a real food image
        img_url = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800"
        img_response = requests.get(img_url)
        img = Image.open(io.BytesIO(img_response.content))
        
        # Resize to moderate size
        img = img.resize((800, 600), Image.Resampling.LANCZOS)
        
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)
        b64_image = base64.b64encode(img_buffer.read()).decode()
        
        print(f"   Image size: {len(b64_image)} bytes (base64)")
        
        payload = {"image_b64": b64_image, "notes": ""}
        
        print(f"   Calling /analyze endpoint...")
        response = session.post(
            f"{api_url}/analyze",
            json=payload,
            headers=headers,
            timeout=45,
            stream=False
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Food detected: {data['profile']['name']}")
            print(f"   Calories: {data['profile']['calories']}")
        else:
            print(f"   Error: {response.text[:200]}...")
            
    except requests.exceptions.ChunkedEncodingError as e:
        print(f"   ChunkedEncodingError: {e}")
        print("\n   Possible causes:")
        print("   - Server closing connection prematurely")
        print("   - Response size too large")
        print("   - Network instability")
        print("   - Server timeout during processing")
    except Exception as e:
        print(f"   Other error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_api_connection()
    
    print("\n\n💡 If you see ChunkedEncodingError:")
    print("1. Check if API server is running properly")
    print("2. Check server logs for errors")
    print("3. Try smaller images")
    print("4. Ensure stable network connection")