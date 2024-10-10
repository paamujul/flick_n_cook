import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini Pro Model with API key
genai.configure(api_key="AIzaSyBrxhz_lJ34ufi1sJPi2n_b5RpSILB5Nas")

# Function to load Gemini Pro Model and get a response
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(cooking_time, meal_type, diet_preference, image):
    prompt = f"""
    Devise a recipe that can be cooked in {cooking_time} minutes.
    The recipe should be for {meal_type} and should match the dietary preference of {diet_preference}.
    If an image is provided, analyze it for available ingredients and use them in the recipe.
    """
    if image is not None:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Recipe App")
st.header("Gemini Recipe Generator")

# Option 1: Slider for cooking time
cooking_time = st.slider("Select Cooking Time (minutes):", 5, 60, step=5)

# Option 2: Single select for meal type
meal_type = st.selectbox("Select Meal Type:", options=["Breakfast", "Lunch", "Dinner"])

# Option 3: Single select for dietary preference
diet_preference = st.selectbox("Select Dietary Preference:", options=["Vegetarian with Egg", "Only Chicken", "Only Sea Food", "Pure Vegetarian"])

# File uploader for image
uploaded_file = st.file_uploader("Choose an image (optional):", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button for initial recipe generation
submit = st.button("Generate Recipe")
regenerate = st.button("Regenerate Recipe")

# Function to handle both 'Generate' and 'Regenerate' buttons
if submit or regenerate:
    response = get_gemini_response(cooking_time, meal_type, diet_preference, image)
    st.subheader("Gemini Recipe:")
    st.write(response)
