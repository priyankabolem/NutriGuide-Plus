# Deployment Guide

This guide covers deploying NutriGuide+ to production environments using Render (API) and Streamlit Cloud (UI).

## Architecture Overview

```
┌─────────────────────┐    ┌──────────────────────┐
│   Streamlit Cloud   │───▶│      Render API      │
│   (UI Frontend)     │    │   (Backend Service)  │
│                     │    │                      │
│  - Global CDN       │    │  - Auto-scaling      │
│  - HTTPS enabled    │    │  - Health checks     │
│  - Custom domain    │    │  - Environment vars  │
└─────────────────────┘    └──────────────────────┘
```

## Prerequisites

### Required Accounts
- [GitHub](https://github.com) - Source code repository
- [Render](https://render.com) - API backend hosting
- [Streamlit Cloud](https://share.streamlit.io) - UI frontend hosting

### Repository Setup
Ensure your repository contains:
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies
- `.streamlit/secrets.toml` - Configuration template
- `.python-version` - Python version specification

## Backend Deployment (Render)

### Step 1: Create Render Service

1. **Login to Render Dashboard**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub account

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Select `NutriGuide-Plus` repository

3. **Configure Service**
   - **Name**: `nutriguide-plus`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:api --host 0.0.0.0 --port $PORT`

### Step 2: Environment Configuration

Render automatically detects `render.yaml` with these settings:
```yaml
services:
  - type: web
    name: nutriguide-plus
    env: python
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:api --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
```

### Step 3: Deployment Process

1. **Automatic Build**
   - Render detects configuration
   - Installs Python 3.11
   - Installs project dependencies
   - Builds computer vision models

2. **Health Checks**
   - API responds at `/health`
   - Computer vision models load successfully
   - Database connections verified

3. **Live Service**
   - Service available at: `https://nutriguide-plus.onrender.com`
   - API docs: `https://nutriguide-plus.onrender.com/docs`

## Frontend Deployment (Streamlit Cloud)

### Step 1: Create Streamlit App

1. **Access Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub account

2. **Deploy New App**
   - Click "Deploy an app"
   - Select GitHub repository: `NutriGuide-Plus`
   - Set main file path: `web/app.py`
   - Choose branch: `main`

### Step 2: Configure Secrets

1. **Access App Settings**
   - Go to app dashboard
   - Click "Settings" → "Secrets"

2. **Add API Configuration**
```toml
# Replace with your actual Render URL
api_url = "https://nutriguide-plus.onrender.com"
```

### Step 3: Launch Application

1. **Deploy Process**
   - Streamlit Cloud builds the app
   - Installs dependencies automatically
   - Connects to Render API backend

2. **Access Live App**
   - App URL: `https://nutriguide-plus.streamlit.app`
   - Fully functional food analysis
   - Real-time computer vision processing

## Monitoring and Maintenance

### Health Monitoring

**Render Service:**
```bash
# Check API health
curl https://nutriguide-plus.onrender.com/health

# Monitor logs
# Available in Render dashboard → Logs
```

**Streamlit App:**
```bash
# Check UI health
curl https://nutriguide-plus.streamlit.app

# Monitor via Streamlit Cloud dashboard
```

### Performance Metrics

**Target Performance:**
- API Response Time: < 3 seconds
- Image Processing: < 2 seconds
- UI Load Time: < 1 second
- Uptime: 99.9%

### Troubleshooting

#### Common Issues

**Connection Refused Error:**
- Verify Streamlit secrets contain correct Render URL
- Check Render service is running and healthy
- Validate API endpoints respond correctly

**Slow Performance:**
- Monitor computer vision model loading
- Check image size and processing time
- Verify database query efficiency

**Build Failures:**
- Review Python version compatibility
- Check dependency conflicts in requirements.txt
- Validate Render build logs

#### Debug Tools

**API Debugging:**
```python
# Test API endpoint directly
import requests

response = requests.get("https://nutriguide-plus.onrender.com/health")
print(response.json())
```

**UI Debugging:**
- Streamlit Cloud provides real-time logs
- Use browser developer tools for frontend issues
- Check network tab for API call failures

## Scaling Considerations

### Horizontal Scaling
- Render auto-scales based on CPU usage
- Multiple instance deployment supported
- Load balancer automatically configured

### Performance Optimization
- Computer vision model caching
- Database query optimization
- Image preprocessing efficiency
- Response compression enabled

### Cost Management
- Render free tier: 750 hours/month
- Streamlit Cloud: Free for public repositories
- Monitor usage through dashboards

## Security Best Practices

### Data Protection
- No user data stored permanently
- Images processed in memory only
- HTTPS enforced for all communications
- Environment variables for sensitive config

### API Security
- Input validation for all endpoints
- Image size and format restrictions
- Error handling without information leakage
- CORS properly configured

## Continuous Deployment

### Automated Workflow
1. **Code Push** → GitHub repository
2. **Auto-Deploy** → Render builds and deploys API
3. **Auto-Update** → Streamlit Cloud updates UI
4. **Health Check** → Services verify functionality

### Deployment Pipeline
```bash
git add .
git commit -m "feature: enhance food recognition accuracy"
git push origin main
# Render and Streamlit automatically deploy
```

---

**Deployment Guide by NutriGuide+ Team**