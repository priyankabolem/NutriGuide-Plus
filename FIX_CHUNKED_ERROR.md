# Fixing ChunkedEncodingError in NutriGuide+

## Problem
The ChunkedEncodingError occurs when Streamlit cannot properly receive the response from the API. This typically happens due to:
1. Large response payloads
2. Network timeouts
3. Unstable connections between Streamlit and API
4. Server-side processing taking too long

## Solutions Implemented

### 1. **Response Compression**
Added GZip middleware to compress API responses:
```python
# In app/main.py
from fastapi.middleware.gzip import GZipMiddleware
api.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 2. **Request Session with Retry Logic**
Implemented automatic retry for failed requests:
```python
# In web/app.py
session = requests.Session()
retry = Retry(
    total=3,
    read=3,
    connect=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504)
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 3. **Image Optimization**
Automatically resize and compress large images before sending:
```python
# Resize if too large (max 1024px)
max_size = 1024
if max(img.size) > max_size:
    ratio = max_size / max(img.size)
    new_size = tuple(int(dim * ratio) for dim in img.size)
    img = img.resize(new_size, Image.Resampling.LANCZOS)

# Save with optimization
img.save(img_buffer, format='JPEG', quality=85, optimize=True)
```

### 4. **Improved Error Handling**
Added specific handling for ChunkedEncodingError:
```python
except requests.exceptions.ChunkedEncodingError as e:
    st.error("Network error: The connection was interrupted.")
    st.info("This usually happens with unstable connections. Please try again.")
    if st.button("Retry Analysis", key="retry_chunked"):
        st.experimental_rerun()
```

### 5. **Increased Timeouts**
Extended timeout from 30s to 45s for both analyze and verify endpoints.

## Testing the Fix

1. **Run the test script**:
   ```bash
   python test_api_chunked.py
   ```

2. **Test with Streamlit locally**:
   ```bash
   # Terminal 1 - Start API
   uvicorn app.main:api --reload --port 8000
   
   # Terminal 2 - Start Streamlit
   streamlit run web/app.py
   ```

3. **Upload various image sizes**:
   - Small image (< 1MB)
   - Medium image (1-5MB)
   - Large image (> 5MB) - should auto-resize

## Deployment Considerations

### For Render Deployment

1. **Update environment variables**:
   ```
   PYTHON_VERSION=3.11.9
   API_URL=https://your-api.onrender.com
   GOOGLE_VISION_API_KEY=your-key-here
   ```

2. **Ensure proper CORS settings** in production.

3. **Monitor server logs** for any timeout issues.

### For Streamlit Cloud

1. **Set secrets** in Streamlit Cloud:
   ```toml
   api_url = "https://your-api.onrender.com"
   ```

2. **Ensure requirements.txt includes**:
   ```
   requests==2.32.3
   Pillow==10.4.0
   ```

## Additional Troubleshooting

If the error persists:

1. **Check API server logs**:
   - Look for timeout errors
   - Check for memory issues
   - Verify Google Vision API is working

2. **Network diagnostics**:
   ```bash
   # Test API endpoint directly
   curl -X GET https://your-api.onrender.com/health
   ```

3. **Reduce payload size further**:
   - Lower image quality to 70%
   - Reduce max size to 800px
   - Implement progressive loading

4. **Use CDN for static assets** if response includes large data.

## Prevention

1. **Monitor API performance** regularly
2. **Set up alerts** for timeout errors
3. **Implement caching** for repeated requests
4. **Use background tasks** for long-running operations

The implemented fixes should resolve most ChunkedEncodingError issues. If problems persist in production, check server resources and network stability between services.