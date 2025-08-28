# NutriGuide+

**AI-Powered Nutrition Analysis & Recipe Recommendation Platform**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

NutriGuide+ is an advanced nutrition analysis platform that leverages artificial intelligence to provide instant nutritional insights from food images. Simply upload a photo of your meal, and receive comprehensive nutrition profiles, personalized recipe recommendations, and real-time verification of nutritional data.

### Key Features

- **Instant Food Recognition**: Advanced computer vision identifies food items from photos
- **Comprehensive Nutrition Profiles**: Detailed breakdown of calories, macros, and micronutrients
- **Smart Recipe Recommendations**: Personalized recipes based on identified ingredients
- **Real-Time Verification**: Cross-references nutritional data with verified databases
- **Modern UI/UX**: Clean, responsive interface optimized for all devices
- **Production-Ready**: Scalable architecture with API-first design

## Technology Stack

### Backend
- **FastAPI**: High-performance API framework with automatic documentation
- **Pydantic**: Data validation and settings management
- **Pandas**: Efficient data processing and analysis
- **Pillow**: Advanced image processing capabilities

### Frontend
- **Streamlit**: Interactive web application framework
- **Custom CSS**: Professional, responsive design
- **Real-time Updates**: Dynamic content rendering

### Infrastructure
- **Render**: Cloud hosting for API services
- **Streamlit Cloud**: Dedicated UI hosting
- **GitHub Actions**: CI/CD pipeline (coming soon)

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git for version control

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/NutriGuide-Plus.git
cd NutriGuide-Plus
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the API server**
```bash
make run
# Or directly: uvicorn app.main:api --reload --port 8000
```

5. **Launch the UI** (new terminal)
```bash
make ui
# Or directly: streamlit run web/app.py
```

6. **Access the application**
- API Documentation: http://localhost:8000/docs
- Web Interface: http://localhost:8501

## Deployment

### Deploy API to Render

1. **Connect GitHub repository to Render**
   - Create new Web Service on [Render](https://render.com)
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` configuration

2. **Environment setup is automatic**
   - Python 3.11 runtime
   - Auto-deploy on push to main branch
   - Health checks configured

### Deploy UI to Streamlit Cloud

1. **Connect to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set app file path: `web/app.py`

2. **Configure secrets**
   - In Streamlit Cloud settings, add:
   ```toml
   api_url = "https://your-api-name.onrender.com"
   ```

## Project Structure

```
NutriGuide-Plus/
├── app/                    # FastAPI backend
│   ├── main.py            # API entry point
│   ├── models.py          # Pydantic models
│   ├── routers/           # API endpoints
│   │   ├── analyze.py     # Food analysis endpoint
│   │   └── verify.py      # Verification endpoint
│   └── services/          # Business logic
│       ├── vision.py      # Image processing
│       ├── generator.py   # Profile generation
│       └── verifier.py    # Data verification
├── web/                   # Streamlit frontend
│   └── app.py            # UI application
├── data/                  # Reference data
│   └── canonical_foods.csv
├── tests/                 # Test suite
├── .streamlit/           # Streamlit config
├── requirements.txt      # Dependencies
├── render.yaml          # Render config
└── build.sh            # Build script
```

## API Endpoints

### POST /analyze
Analyzes food images and returns nutritional recommendations.

**Request Body:**
```json
{
  "image_b64": "base64_encoded_image",
  "notes": "optional dietary notes"
}
```

**Response:**
```json
{
  "profile": {
    "name": "grilled chicken",
    "serving_grams": 150,
    "calories": 280,
    "macros": {
      "protein_g": 40,
      "carbs_g": 0,
      "fat_g": 12
    }
  },
  "recipes": [...]
}
```

### POST /verify
Verifies nutritional data accuracy against canonical database.

## Testing

Run the test suite:
```bash
pytest -v
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- TensorFlow/Keras integration for enhanced food recognition
- Advanced LLM integration for recipe generation
- Expanded nutritional database
- Mobile application
- Multi-language support
- Allergen detection and warnings
- Meal planning features

## Team

**Priyanka Bolem** - Full Stack Developer

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI community for the excellent framework
- Streamlit team for the intuitive UI tools
- Open source nutrition databases

---

**Built by Priyanka Bolem**