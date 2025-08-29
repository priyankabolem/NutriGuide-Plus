# Deployment Guide for NutriGuide+

This guide provides step-by-step instructions for deploying NutriGuide+ to production using Render (API) and Streamlit Cloud (UI).

## Prerequisites

- GitHub account with the code repository
- Render account (free tier available)
- Streamlit Cloud account (free tier available)

**Note**: This project uses 100% free services. No API keys or paid subscriptions required!

## Step 1: Prepare Your Repository

1. Ensure all code is committed and pushed to GitHub
2. Verify the following files exist in your repository:
   - `render.yaml` (Render configuration)
   - `requirements.txt` (Python dependencies)
   - `.streamlit/config.toml` (Streamlit configuration)
   - `runtime.txt` (Python version specification)

## Step 2: Deploy API to Render

### 2.1 Create Render Account
1. Visit [render.com](https://render.com)
2. Sign up with your GitHub account

### 2.2 Deploy the API
1. Click "New +" in the Render dashboard
2. Select "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` configuration
5. Review the settings:
   - Name: `nutriguide-plus-api`
   - Environment: Python 3.11
   - Build Command: `./build.sh`
   - Start Command: `uvicorn app.main:api --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service" (No environment variables needed!)
7. Wait for the deployment to complete (5-10 minutes)
8. Copy your API URL (format: `https://nutriguide-plus-api.onrender.com`)

### 2.3 Verify API Deployment
1. Visit `https://your-api-url.onrender.com/docs`
2. You should see the FastAPI interactive documentation
3. Test the `/analyze` endpoint with a sample image

## Step 3: Deploy UI to Streamlit Cloud

### 3.1 Create Streamlit Cloud Account
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub

### 3.2 Deploy the UI
1. Click "New app"
2. Select your repository
3. Configure deployment:
   - Repository: `yourusername/NutriGuide-Plus`
   - Branch: `main`
   - Main file path: `web/app.py`
4. Click "Advanced settings"
5. Add secrets:
   ```toml
   api_url = "https://nutriguide-plus-api.onrender.com"
   ```
   (Replace with your actual Render API URL)
6. Click "Deploy"
7. Wait for deployment (2-5 minutes)

### 3.3 Access Your Live Application
Your app will be available at:
`https://yourusername-nutriguide-plus-web-app-xxxxx.streamlit.app`

## Step 4: Post-Deployment Configuration

### 4.1 Update CORS Settings (if needed)
If you encounter CORS issues, update `app/main.py`:
```python
allow_origins=["https://your-streamlit-app-url.streamlit.app"]
```

### 4.2 Monitor Your Services
- **Render Dashboard**: Monitor API health, logs, and metrics
- **Streamlit Cloud Dashboard**: View app usage and logs
- **Hugging Face**: Check inference API usage (optional)

## Step 5: Testing Your Deployment

1. Visit your Streamlit app URL
2. Upload a food image
3. Verify that:
   - Image uploads successfully
   - Food is correctly identified (should be accurate with Google Vision)
   - Nutrition information is realistic and accurate
   - Analysis returns results
   - Verification works correctly
   - Recipe recommendations display

## Troubleshooting

### API Not Responding
1. Check Render logs for errors
2. Verify the API URL in Streamlit secrets
3. Ensure health check endpoint responds: `https://your-api.onrender.com/health`

### Streamlit App Errors
1. Check Streamlit logs
2. Verify secrets are correctly configured
3. Ensure API URL doesn't have trailing slash

### Performance Issues
- Render free tier may sleep after inactivity (first request takes ~30s)
- Consider upgrading to paid tier for better performance

## Security Considerations

1. Never commit secrets to repository
2. Use environment variables for sensitive data
3. Configure CORS appropriately for production
4. Enable HTTPS (automatic on both platforms)

## Maintenance

### Updating the Application
1. Push changes to GitHub
2. Both services auto-deploy on push to main branch
3. Monitor deployment logs for issues

### Scaling
- **Render**: Upgrade to paid plans for more resources
- **Streamlit**: Contact for custom deployment options

## Support

For deployment issues:
- Render: [render.com/docs](https://render.com/docs)
- Streamlit: [docs.streamlit.io](https://docs.streamlit.io)

---

Developed by Priyanka Bolem