import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(idea_generator, job_description):
    prompt = (
        f"Generate innovative and creative ideas related to the topic provided by the user:\n\n"
        f"Input Details: {json.dumps(idea_generator, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please generate unique ideas that align with the specified topic. After generating the ideas, provide answers or explanations for each idea."
    )

    payload = {
        "model": "gpt-4",
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
st.title("Idea Generator")

# Inputs for idea generation
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic = st.text_input("Topic to be Specific:", "Artificial Intelligence")
num_ideas = st.number_input("Number of Ideas:", min_value=1, max_value=20, value=6)

job_description = st.text_area("Job Description:", 
    "Get help coming up with ideas on any topic.")

if st.button("Generate Ideas"):
    idea_generator = {
        "Grade Level:": grade_level,
        "topic to be specific": topic,
        "num_ideas": str(num_ideas),
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(idea_generator, job_description)
            st.success("Generation Complete!")
            st.text_area("Generated Ideas:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
