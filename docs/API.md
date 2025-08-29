# NutriGuide+ API Documentation

## Overview

The NutriGuide+ API provides advanced computer vision-powered food recognition and nutrition analysis capabilities. This RESTful API processes food images and returns comprehensive nutritional information, recipe recommendations, and dietary insights.

## Base URL

**Production:** `https://nutriguide-plus.onrender.com`  
**Local Development:** `http://localhost:8000`

## Authentication

Currently, the API is publicly accessible and does not require authentication. Rate limiting may be implemented in future versions.

## Endpoints

### Health Check

#### GET /
Basic health status endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "NutriGuide+ API",
  "version": "3.0.0"
}
```

#### GET /health
Detailed health information with system status.

**Response:**
```json
{
  "status": "healthy",
  "service": "NutriGuide+ API",
  "version": "3.0.0",
  "build": "2025-01-real-cv",
  "timestamp": "2025-01-29T12:00:00.000Z",
  "endpoints": [
    "/analyze - Food analysis endpoint",
    "/verify - Nutrition verification endpoint"
  ],
  "features": {
    "real_computer_vision": true,
    "usda_nutrition_database": true,
    "confidence_scoring": true,
    "image_validation": true,
    "unlimited_food_types": true
  }
}
```

### Food Analysis

#### POST /analyze

Analyzes food images using computer vision and returns comprehensive nutrition information.

**Request Body:**
```json
{
  "image_b64": "base64_encoded_image_string",
  "notes": "optional dietary preferences or restrictions"
}
```

**Parameters:**
- `image_b64` (string, required): Base64-encoded image data
- `notes` (string, optional): Dietary notes, preferences, or restrictions

**Response:**
```json
{
  "profile": {
    "name": "grilled chicken breast",
    "serving_grams": 150,
    "calories": 280,
    "macros": {
      "protein_g": 40.0,
      "carbs_g": 0.0,
      "fat_g": 12.0
    },
    "micronutrients": {
      "fiber_g": 0.0,
      "sugar_g": 0.0,
      "sodium_mg": 95,
      "cholesterol_mg": 120
    }
  },
  "recipes": [
    {
      "title": "Healthier Grilled Chicken Breast",
      "steps": [
        "Start with fresh, high-quality chicken breast",
        "Use minimal oil or opt for air-frying/grilling",
        "Add plenty of vegetables for extra nutrients",
        "Season with herbs and spices instead of excess salt",
        "Serve with a side of whole grains or salad"
      ],
      "time_minutes": 25,
      "cost_estimate_usd": 12.40,
      "ingredients": [
        "chicken breast",
        "vegetables",
        "olive oil",
        "herbs",
        "whole grains"
      ]
    }
  ]
}
```

**Error Responses:**

- `400 Bad Request`: Invalid image format
- `422 Unprocessable Entity`: Image too small or unclear
- `500 Internal Server Error`: Analysis processing failed

### Nutrition Verification

#### POST /verify

Verifies nutritional information against canonical food database.

**Request Body:**
```json
{
  "food_name": "grilled chicken breast",
  "provided_nutrition": {
    "calories": 280,
    "protein_g": 40.0,
    "carbs_g": 0.0,
    "fat_g": 12.0
  }
}
```

**Response:**
```json
{
  "verification_status": "verified",
  "accuracy_score": 0.95,
  "canonical_data": {
    "name": "grilled chicken breast",
    "serving_grams": 150,
    "calories": 280,
    "macros": {
      "protein_g": 40.0,
      "carbs_g": 0.0,
      "fat_g": 12.0
    }
  },
  "differences": []
}
```

## Computer Vision Features

### Image Requirements

**Supported Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- Base64 encoded images

**Recommended Specifications:**
- Minimum size: 224x224 pixels
- Maximum size: 4096x4096 pixels (auto-resized)
- Clear, well-lit food images
- Single food item or dish focus

### Recognition Capabilities

**Food Categories:**
- Proteins (chicken, beef, fish, eggs, etc.)
- Carbohydrates (rice, pasta, bread, potatoes)
- Vegetables (salads, cooked vegetables, greens)
- Fruits (fresh fruits, fruit salads, berries)
- Complex dishes (pizza, burgers, tacos, soups)
- Desserts (cakes, ice cream, pastries)

**Analysis Features:**
- Color distribution analysis
- Texture complexity detection
- Pattern recognition algorithms
- Confidence scoring (0.0-1.0)
- Visual characteristic extraction

## Data Sources

### USDA Nutrition Database
- Verified nutritional data
- Comprehensive macro/micronutrient profiles
- Standardized serving sizes
- Regular database updates

### Recipe Generation
- Context-aware recipe creation
- Preparation method optimization
- Cost estimation algorithms
- Time-based meal planning

## Rate Limits

Current rate limits:
- **Development**: No limits
- **Production**: 1000 requests per hour per IP

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request format
- `422 Unprocessable Entity`: Valid request, invalid data
- `500 Internal Server Error`: Server processing error

Error responses include detailed messages:
```json
{
  "detail": "Image too small for analysis. Please upload a clearer image."
}
```

## SDK and Integration

### Python Integration
```python
import requests
import base64

# Encode image
with open("food_image.jpg", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

# Analyze food
response = requests.post(
    "https://nutriguide-plus.onrender.com/analyze",
    json={
        "image_b64": img_b64,
        "notes": "low carb diet"
    }
)

nutrition_data = response.json()
```

### JavaScript Integration
```javascript
// Convert image to base64
const fileToBase64 = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.readAsDataURL(file);
  });
};

// Analyze food
const analyzeFood = async (imageFile, notes = '') => {
  const imageB64 = await fileToBase64(imageFile);
  
  const response = await fetch('https://nutriguide-plus.onrender.com/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      image_b64: imageB64,
      notes: notes
    })
  });
  
  return await response.json();
};
```

## Performance Optimization

### Image Processing
- Images auto-resized for optimal processing
- Efficient color and texture analysis
- Parallel processing for multiple predictions
- Memory-efficient operations

### Response Time
- Average response: 1-3 seconds
- 95th percentile: < 5 seconds
- Global CDN distribution
- Optimized ML model inference

## Version History

### v3.0.0 (Current)
- Real computer vision implementation
- USDA nutrition database integration
- Enhanced accuracy and reliability
- Professional production deployment

### v2.0.0
- Dynamic food recognition system
- Expanded food vocabulary
- Improved recipe generation

### v1.0.0
- Initial API implementation
- Basic food recognition
- Core nutrition calculation

---

**API Documentation maintained by Priyanka Bolem**