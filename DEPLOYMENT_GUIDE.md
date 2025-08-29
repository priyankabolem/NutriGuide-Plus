# NutriGuide+ Complete Deployment Guide

## Prerequisites
- Google Cloud account with Vision API enabled
- Render account
- Streamlit Cloud account
- Google Vision API key

## Step 1: Verify Google Vision API Setup

### 1.1 Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Navigate to **APIs & Services > Library**
4. Search for "Cloud Vision API"
5. Ensure it's **ENABLED**
6. Go to **APIs & Services > Credentials**
7. Copy your API key

### 1.2 Test API Key Locally
```bash
# Set environment variable
export GOOGLE_VISION_API_KEY="your-api-key-here"

# Test the key
curl -X POST \
  "https://vision.googleapis.com/v1/images:annotate?key=$GOOGLE_VISION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"requests":[]}'
```
You should get a 400 error (expected for empty request), NOT a 403 (forbidden).

## Step 2: Deploy API to Render

### 2.1 Environment Variables in Render
1. Go to your Render dashboard
2. Select your **nutriguide-plus-api** service
3. Go to **Environment** tab
4. Add/Update these variables:
   ```
   GOOGLE_VISION_API_KEY = your-actual-api-key-here
   PYTHON_VERSION = 3.11.9
   ENV = production
   ```
5. Click **Save Changes**

### 2.2 Verify Deployment
1. Wait for the service to redeploy (takes 5-10 minutes)
2. Check the deploy logs for:
   ```
   ✓ Google Vision API key configured
   ```

### 2.3 Test Production API
```bash
# Replace with your actual Render URL
API_URL="https://nutriguide-plus-api.onrender.com"

# Test health
curl $API_URL/health

# Test Google Vision status
curl $API_URL/debug/status

# Test vision methods
curl -X POST $API_URL/debug/test-vision
```

## Step 3: Configure Streamlit

### 3.1 Update Streamlit Secrets
1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Select your NutriGuide+ app
3. Go to **Settings > Secrets**
4. Add:
   ```toml
   api_url = "https://nutriguide-plus-api.onrender.com"
   ```
   (Replace with your actual Render API URL)

### 3.2 Verify Streamlit Configuration
The Streamlit app should show your API URL in the console when running.

## Step 4: Troubleshooting

### 4.1 Run Production Verification
```bash
python verify_production.py
```
Enter your production API URL when prompted.

### 4.2 Check Debug Endpoints
Visit these URLs in your browser:
- `https://your-api.onrender.com/health`
- `https://your-api.onrender.com/debug/status`
- `https://your-api.onrender.com/docs` (API documentation)

### 4.3 Common Issues and Solutions

#### Issue: "Google Vision API not configured"
**Solution:**
1. Ensure `GOOGLE_VISION_API_KEY` is set in Render environment
2. Redeploy the service after setting the variable
3. Check logs for confirmation message

#### Issue: API key valid but still using fallback methods
**Solution:**
1. Check that the latest code is deployed
2. Verify no syntax errors in logs
3. Ensure imports are working correctly

#### Issue: 403 Forbidden from Google Vision
**Solution:**
1. Enable Vision API in Google Cloud Console
2. Check API key restrictions
3. Verify billing is enabled

#### Issue: ChunkedEncodingError in Streamlit
**Solution:**
1. Already fixed with retry logic and compression
2. Ensure both API and Streamlit are using latest code

### 4.4 Monitor Logs

#### Render Logs
Look for these key messages:
```
✓ Google Vision API key configured
🚀 Using Google Vision API for professional-grade accuracy
✓ Google Vision detected: pizza (0.92)
```

#### What You Should See
When working correctly:
1. Upload food image in Streamlit
2. API logs show "Using Google Vision API"
3. High confidence scores (>0.75)
4. Accurate food detection

## Step 5: Verify Everything is Working

### Expected Behavior with Google Vision:
- **Pizza image** → "pizza" (85-95% confidence)
- **Salad image** → "salad" or specific salad type (80-90% confidence)
- **Burger image** → "burger" or "hamburger" (85-95% confidence)

### Without Google Vision (fallback):
- Lower confidence scores (50-70%)
- More generic results ("mixed dish", "food item")

## Final Checklist

- [ ] Google Vision API enabled in Google Cloud Console
- [ ] API key has no restrictions or correct restrictions
- [ ] GOOGLE_VISION_API_KEY set in Render environment
- [ ] API redeployed after setting environment variable
- [ ] Streamlit secrets updated with correct API URL
- [ ] Debug endpoints confirm Google Vision is configured
- [ ] Test image returns high confidence results

## Support

If issues persist after following this guide:
1. Check Render deploy logs
2. Use `/debug/status` endpoint
3. Run `verify_production.py` script
4. Check Google Cloud Console for API usage/errors