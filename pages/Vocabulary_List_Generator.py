import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(vocabulary_list_generator, job_description):
    prompt = (
        f"Generate a list of key vocab words with definitions based on any subject, topic, standard, or even text for students to learn:\n\n"
        f"generate_questions: {json.dumps(vocabulary_list_generator, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please generate a list of key vocab words with definitions based on any subject, topic, standard, or even text for students to learn, strictly following the prompt."
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
st.title("Vocabulary List Generator")

# Inputs for vocabulary list generation
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
num_words = st.text_input("Number of Vocabulary Words to Define:", "10")
subject_text = st.text_input("Subject or Text:", "Laws of Motion")

job_description = "Generate a list of key vocab words based on any subject, topic, standard, or even text for students to learn."

if st.button("Generate Vocabulary List"):
    vocabulary_list_generator = {
        "Grade Level:": grade_level,
        "Vocabulary Words to Define": num_words,
        "Subject or text": subject_text,
    }

    if api_key:
        with st.spinner("Generating vocabulary list..."):
            result = call_openai_api(vocabulary_list_generator, job_description)
            st.success("Vocabulary List Generation Complete!")
            st.text_area("Generated Vocabulary List:", result, height=400)
    else:
        st.error("API key not found. Please add it to the .env file.")
