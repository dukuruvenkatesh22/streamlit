import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(keyword_list):
    prompt = (
        "You are acting like a teacher. The user will provide keywords or topics based on that generate important keywords for examination:\n\n"
        f"generate_keywords: {json.dumps(keyword_list, indent=4)}\n\n"
        "Job Description: Instantly create valuable organizational tools with a depth of information. Lists can be used for a wide variety of learning opportunities or reinforcement.\n\n"
        "Please follow the user topic or keyword with descriptions to generate important keywords based on the grade level."
    )

    payload = {
        "model": "gpt-4o-mini",
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
st.title("Important Keywords Generator")

# Inputs for keyword generation
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic_keywords = st.text_input("Topic or Keywords:", "temperature")

if st.button("Generate Keywords"):
    keyword_list = {
        "grade_level": grade_level,
        "topic or keywords": topic_keywords,
    }

    if api_key:
        with st.spinner("Generating keywords..."):
            result = call_openai_api(keyword_list)
            st.success("Keyword Generation Complete!")
            st.text_area("Generated Keywords:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
