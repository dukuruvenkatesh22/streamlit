import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(scenario_based_questions, job_description):
    prompt = (
        f"You are an AI assistant to help students regarding scenario-based questions based on the job description:\n\n"
        f"generate_questions: {json.dumps(scenario_based_questions, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please generate scenario-based questions based on the topic or context, strictly following the job description."
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
st.title("Scenario-Based Questions Generator")

# Inputs for question generation
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic = st.text_input("Topic:", "Artificial Intelligence")
context = st.text_area("Context (optional):")

job_description = st.text_area("Job Description:", 
    "Questions created by AI that present a specific situation or problem to students, requiring them to apply their knowledge, skills, and critical thinking to propose solutions or responses. These questions are commonly used in various disciplines to simulate real-life challenges and assess a student’s ability to handle complex and dynamic situations.")

if st.button("Generate Scenario-Based Questions"):
    scenario_based_questions = {
        "Grade Level:": grade_level,
        "topic": topic,
        "context(optional)": context,
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(scenario_based_questions, job_description)
            st.success("Generation Complete!")
            st.text_area("Generated Scenario-Based Questions:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
