import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(reading_comprehension, job_description):
    prompt = (
        f"Generate a short text with a variety of questions that are directly related to the text. Great for formative assessments or adding supplemental context:\n\n"
        f"generate_questions: {json.dumps(reading_comprehension, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please generate a short text with a variety of questions that are directly related to the text. Great for formative assessments or adding supplemental context. Strictly follow the prompt and generate accordingly. After completing the generation of questions, generate answers for the questions you generated, strictly following these instructions."
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
st.title("Reading Comprehension Generator")

# Inputs for reading comprehension
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic = st.text_input("Topic or Keyword:", "Artificial Intelligence")
num_questions = st.number_input("Number of Questions:", min_value=1, max_value=20, value=10)

job_description = st.text_area("Job Description:", 
    "Generate a short text with a variety of questions that are directly related to the text. Great for formative assessments or adding supplemental context.")

if st.button("Generate Reading Comprehension"):
    reading_comprehension = {
        "Grade Level:": grade_level,
        "topic or keyword": topic,
        "num of questions": num_questions,
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(reading_comprehension, job_description)
            st.success("Generation Complete!")
            st.text_area("Generated Reading Comprehension Material:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
