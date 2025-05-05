import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(unit_plan_generator, job_description):
    prompt = (
        f"Generate a draft for a unit plan based on the subject and objective, based on length of the unit you’re teaching:\n\n"
        f"generate_questions: {json.dumps(unit_plan_generator, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please create a draft for a unit plan based on the subject and objective, strictly follow the prompt."
    )

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1,
        "max_tokens": 4095,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.json()}"

# Streamlit app layout
st.title("Unit Plan Generator")

# Inputs for unit plan generation
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
unit_length = st.text_input("Unit Length (e.g., '3 pages'):", "3 pages")
unit_plan_title = st.text_input("Unit Plan Title/Topic:", "Friction")
context = st.text_area("Context (optional):", 
    "Two simple experimental facts characterize the friction of sliding solids... (Your text here)")

job_description = "Create a draft for a unit plan based on the subject and objective, based on length of the unit you’re teaching."

if st.button("Generate Unit Plan"):
    unit_plan_generator = {
        "grade_level": grade_level,
        "unit_length": unit_length,
        "unit_plan_title/topic": unit_plan_title,
        "context(optional)": context,
    }

    if api_key:
        with st.spinner("Generating unit plan..."):
            result = call_openai_api(unit_plan_generator, job_description)
            st.success("Unit Plan Generation Complete!")
            st.text_area("Generated Unit Plan:", result, height=400)
    else:
        st.error("API key not found. Please add it to the .env file.")
