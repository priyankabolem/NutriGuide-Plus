import streamlit as st
import base64
import requests
import os
import json

# Page config
st.set_page_config(
    page_title="NutriGuide+ | AI Nutrition Analyzer",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: 600;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1976D2;
    }
    .upload-text {
        font-size: 1.1rem;
        color: #424242;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .metric-container {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #E0E0E0;
    }
    h1 {
        color: #1A1A1A;
        font-weight: 700;
    }
    h3 {
        color: #333333;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Get API URL from environment or secrets
def get_api_url():
    # Check Streamlit secrets first
    if "api_url" in st.secrets:
        return st.secrets["api_url"].rstrip('/')  # Remove trailing slash
    # Fall back to environment variable
    api_url = os.getenv("API_URL", "http://localhost:8000")
    return api_url.rstrip('/')  # Remove trailing slash

API_URL = get_api_url()

# Header
st.markdown("# NutriGuide+")
st.markdown("### AI-Powered Nutrition Analysis & Recipe Recommendations")
st.markdown("---")

# Debug info removed for production

# File upload section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="upload-text">Upload a photo of your food</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="food_upload")

with col2:
    st.markdown('<p class="upload-text">Add notes (optional)</p>', unsafe_allow_html=True)
    notes = st.text_input("", placeholder="e.g., allergies, preferences", key="notes_input")

# Analysis section
if uploaded_file:
    # Display uploaded image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Uploaded food image", use_column_width=True)
    
    # Analyze button
    if st.button("Analyze Nutrition", key="analyze_btn", use_container_width=True):
        try:
            with st.spinner("Analyzing your food..."):
                # Encode image
                uploaded_file.seek(0)  # Reset file pointer
                b64_image = base64.b64encode(uploaded_file.read()).decode()
                
                # Prepare request
                analyze_url = f"{API_URL}/analyze"
                payload = {"image_b64": b64_image, "notes": notes}
                
                # Call analyze endpoint
                analyze_response = requests.post(
                    analyze_url,
                    json=payload,
                    timeout=30
                )
                
                if analyze_response.status_code == 200:
                    recommendation = analyze_response.json()
                    
                    # Display nutrition profile
                    st.markdown("### Nutrition Profile")
                    profile = recommendation["profile"]
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Food", profile["name"].title())
                    with col2:
                        st.metric("Calories", f"{profile['calories']:.0f}")
                    with col3:
                        st.metric("Serving", f"{profile['serving_grams']}g")
                    with col4:
                        st.metric("Protein", f"{profile['macros']['protein_g']}g")
                    
                    # Macros breakdown
                    st.markdown("#### Macronutrients")
                    macro_cols = st.columns(3)
                    with macro_cols[0]:
                        st.info(f"Protein: {profile['macros']['protein_g']}g")
                    with macro_cols[1]:
                        st.info(f"Carbohydrates: {profile['macros']['carbs_g']}g")
                    with macro_cols[2]:
                        st.info(f"Fat: {profile['macros']['fat_g']}g")
                    
                    # Verify nutrition data
                    with st.spinner("Verifying nutrition data..."):
                        verify_response = requests.post(
                            f"{API_URL}/verify",
                            json=profile,
                            timeout=30
                        )
                        
                        if verify_response.status_code == 200:
                            verification = verify_response.json()
                            
                            st.markdown("### Verification Report")
                            confidence = verification["overall_confidence"]
                            
                            if confidence > 0.7:
                                st.success(f"High confidence: {confidence:.0%}")
                            elif confidence > 0.5:
                                st.warning(f"Medium confidence: {confidence:.0%}")
                            else:
                                st.error(f"Low confidence: {confidence:.0%}")
                            
                            # Show verification details
                            with st.container():
                                for item in verification["items"]:
                                    if item["status"] == "supported":
                                        st.markdown(f"**Supported:** {item['claim']}")
                                    else:
                                        st.markdown(f"**Flagged:** {item['claim']}")
                                    if item.get("evidence"):
                                        st.caption(f"Evidence: {item['evidence']}")
                    
                    # Recipe recommendations
                    st.markdown("### Recipe Recommendations")
                    recipes = recommendation["recipes"]
                    
                    for i, recipe in enumerate(recipes):
                        with st.expander(f"{recipe['title']} - {recipe['time_minutes']} mins | ${recipe['cost_estimate_usd']:.2f}"):
                            st.markdown("**Ingredients:**")
                            for ingredient in recipe["ingredients"]:
                                st.markdown(f"• {ingredient}")
                            
                            st.markdown("**Steps:**")
                            for j, step in enumerate(recipe["steps"]):
                                st.markdown(f"{j+1}. {step}")
                
                else:
                    st.error(f"Error analyzing image: {analyze_response.status_code}")
                    st.error(f"Response: {analyze_response.text}")
                    
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError as e:
            st.error(f"Could not connect to the analysis service at {API_URL}")
            st.error(f"Error details: {str(e)}")
            st.error("Please check that the API URL is correct in Streamlit secrets.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #757575; font-size: 0.875rem;'>
        <p>NutriGuide+ - Advanced AI Nutrition Analysis Platform</p>
        <p>Developed by Priyanka Bolem</p>
    </div>
    """,
    unsafe_allow_html=True
)