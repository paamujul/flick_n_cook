import streamlit as st
import google.generativeai as genai
from PIL import Image
from pymongo import MongoClient
from datetime import datetime

import collections

if not hasattr(collections, "MutableMapping"):
    import collections.abc

    collections.MutableMapping = collections.abc.MutableMapping


# Configure Gemini Pro Model with API key
genai.configure(api_key="AIzaSyBrxhz_lJ34ufi1sJPi2n_b5RpSILB5Nas")

# Function to load Gemini Pro Model and get a response
model = genai.GenerativeModel("gemini-1.5-flash")

# MongoDB setup
client = MongoClient(
    "mongodb+srv://sainathaashritha:<Omsai@2004>@cluster0.jydht.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["recipe_database"]  # Database name
recipes_collection = db["recipes"]  # Collection name


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


def save_recipe_to_db(
    cooking_time, meal_type, diet_preference, recipe, image_path=None
):
    recipe_entry = {
        "cooking_time": cooking_time,
        "meal_type": meal_type,
        "diet_preference": diet_preference,
        "recipe": recipe,
        "image_path": image_path,
        "generated_at": datetime.utcnow(),
    }
    recipes_collection.insert_one(recipe_entry)


# Initialize Streamlit app
st.set_page_config(page_title="Gemini Recipe App with MongoDB")
st.header("Gemini Recipe Generator with MongoDB Storage")

# Option 1: Slider for cooking time
cooking_time = st.slider("Select Cooking Time (minutes):", 5, 60, step=5)

# Option 2: Single select for meal type
meal_type = st.selectbox("Select Meal Type:", options=["Breakfast", "Lunch", "Dinner"])

# Option 3: Single select for dietary preference
diet_preference = st.selectbox(
    "Select Dietary Preference:",
    options=["Vegetarian with Egg", "Only Chicken", "Only Sea Food", "Pure Vegetarian"],
)

# File uploader for image
uploaded_file = st.file_uploader(
    "Choose an image (optional):", type=["jpg", "jpeg", "png"]
)
image = None
image_path = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    image_path = uploaded_file.name  # Optional: Store image path in MongoDB

# Submit button for initial recipe generation
submit = st.button("Generate Recipe")
regenerate = st.button("Regenerate Recipe")

# Function to handle both 'Generate' and 'Regenerate' buttons
if submit or regenerate:
    response = get_gemini_response(cooking_time, meal_type, diet_preference, image)

    st.subheader("Gemini Recipe:")
    st.write(response)

    # Save the generated recipe to MongoDB
    save_recipe_to_db(cooking_time, meal_type, diet_preference, response, image_path)

    st.success("Recipe saved to MongoDB!")
