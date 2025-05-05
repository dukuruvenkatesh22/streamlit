import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(poem_request):
    prompt = (
        "You are acting like a teacher. The user will provide keywords or topics based on that generate poems:\n\n"
        f"generate_keywords: {json.dumps(poem_request, indent=4)}\n\n"
        "Job Description: A poem often captures a brief yet profound moment, emotion, or thought. It’s a concise form of expression that can evoke deep imagery or subtle reflection. "
        "Each word carries weight, contributing to the poem’s rhythm, tone, and meaning. Whether it explores themes of love, nature, loss, or introspection, the limited word count challenges the poet to distill complex feelings into a tightly woven, impactful narrative.\n\n"
        "Generate the poems based on the topic or keyword and grade level, and convert user requirements to the specified language (generate both languages: English and Telugu)."
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
st.title("Poem Generator")

# Inputs for poem generation
grade_level = st.selectbox("Grade Level:", ["1st", "2nd", "3rd", "4th", "5th"])
topic_keywords = st.text_input("Topic or Keywords:", "feeling happy")
language = st.selectbox("Language:", ["English", "Telugu"])

if st.button("Generate Poem"):
    poem_request = {
        "grade_level": grade_level,
        "topic or keywords": topic_keywords,
        "language": language,
    }

    if api_key:
        with st.spinner("Generating poem..."):
            result = call_openai_api(poem_request)
            st.success("Poem Generation Complete!")
            st.text_area("Generated Poem:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
