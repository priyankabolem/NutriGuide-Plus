# Google Vision API Setup for NutriGuide+

## Overview

NutriGuide+ supports multiple food recognition methods:
1. **Default (Free)**: Color-based analysis and feature matching
2. **Enhanced (Free)**: Color histogram analysis with HSV and Lab color spaces
3. **Professional (Paid)**: Google Cloud Vision API
4. **Hybrid**: Combines all methods for maximum accuracy

## Accuracy Comparison

| Method | Accuracy | Speed | Cost |
|--------|----------|--------|------|
| Default | 70-75% | Fast (<1s) | Free |
| Color Histogram | 75-80% | Fast (<1s) | Free |
| Google Vision | 85-95% | Medium (1-2s) | Paid |
| Hybrid | 90-95% | Medium (2-3s) | Paid |

## Setting Up Google Vision API

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable billing (required for Vision API)

### Step 2: Enable Vision API

```bash
# Using gcloud CLI
gcloud services enable vision.googleapis.com

# Or enable in Console:
# APIs & Services > Enable APIs > Search "Vision API" > Enable
```

### Step 3: Create Service Account

1. Go to IAM & Admin > Service Accounts
2. Create new service account
3. Grant role: "Cloud Vision API User"
4. Create JSON key and download

### Step 4: Configure NutriGuide+

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Using Different Recognition Methods

### 1. Default Mode (No Configuration Needed)
```python
# Automatically uses free methods
from app.services.vision import classify_topk
results = classify_topk(image_base64)
```

### 2. Force Specific Method
```python
# Use only Google Vision
from app.services.google_vision_recognizer import detect_food_with_google_vision
food, confidence, features = detect_food_with_google_vision(image_base64)

# Use only Color Histogram
from app.services.color_histogram_analyzer import analyze_food_with_color_histograms
food, confidence, features = analyze_food_with_color_histograms(image_base64)

# Use Hybrid (best accuracy)
from app.services.hybrid_food_recognizer import recognize_food_hybrid
food, confidence, details = recognize_food_hybrid(image_base64)
```

## Testing Recognition Methods

Run the test script to compare accuracy:

```bash
python test_food_recognition.py
```

This will:
- Test each method with sample food images
- Compare accuracy and speed
- Save results to `recognition_test_results.json`

## Deployment Considerations

### For Free Deployment (Render/Streamlit Cloud)
- No configuration needed
- Uses default free methods
- 70-80% accuracy

### For Production Deployment with Google Vision
1. Set environment variable:
   ```bash
   heroku config:set GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type":"service_account",...}'
   ```

2. Or mount service account file:
   ```yaml
   # render.yaml
   envVars:
   - key: GOOGLE_APPLICATION_CREDENTIALS
     value: /etc/secrets/google-credentials.json
   ```

## Cost Estimation

Google Vision API Pricing (as of 2024):
- First 1,000 requests/month: Free
- 1,001-5,000,000 requests: $1.50 per 1,000
- Label Detection: 1 unit per image

For a demo with 100 daily users:
- ~3,000 requests/month
- Cost: ~$3/month

## Fallback Strategy

The hybrid recognizer implements smart fallbacks:
1. Try Google Vision API (if configured)
2. Fall back to Color Histogram Analysis
3. Fall back to Feature Matching
4. Always return a result (never fails)

This ensures your app works even if:
- Google Vision API is not configured
- API quota is exceeded
- Network issues occur

## Troubleshooting

### "Google Vision not available"
- Check GOOGLE_APPLICATION_CREDENTIALS path
- Verify service account has Vision API permissions
- Ensure billing is enabled

### Low accuracy with free methods
- Ensure good lighting in photos
- Center food in frame
- Avoid blurry images
- Use solid backgrounds

### API quota exceeded
- Monitor usage in Google Cloud Console
- Implement caching for repeated images
- Consider upgrading quota limits