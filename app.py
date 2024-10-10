import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    response=model.generate_content(question)
    return response.text

st.set_page_config(page_title = ("Flick and Cook"))
st.header("Gemini LLM APplication")

input = st.text_input("input: ", key = "input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(input)
    st.write(response)