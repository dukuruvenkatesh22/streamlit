import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(rubric_details):
    prompt = (
        f"Generate a rubric based on the following details:\n\n"
        f"{json.dumps(rubric_details, indent=4)}\n\n"
        "Please provide clear criteria, levels of achievement, and descriptors for each level."
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
st.title("Rubric Generator")

# Inputs for rubric generation
assignment_name = st.text_input("Assignment Name:", "Research Paper")
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
criteria = st.text_input("Criteria (comma-separated):", "Content, Organization, Mechanics")
num_levels = st.number_input("Number of Levels of Achievement:", min_value=1, max_value=10, value=4)

if st.button("Generate Rubric"):
    rubric_details = {
        "Assignment Name": assignment_name,
        "Grade Level": grade_level,
        "Criteria": [criterion.strip() for criterion in criteria.split(',')],
        "Number of Levels": num_levels,
    }

    if api_key:
        with st.spinner("Generating Rubric..."):
            result = call_openai_api(rubric_details)
            st.success("Rubric Generation Complete!")
            st.text_area("Generated Rubric:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
