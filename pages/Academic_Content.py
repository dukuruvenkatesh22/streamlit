import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(academic_content):
    prompt = (
        "Generate a genre piece of content for grade level.\n\n"
        f"On the topic of {academic_content['topic']} with the following context: "
        f"{academic_content['context']}.\n"
        f"The text length should be approximately {academic_content['text_length']} words."
        f"\n\nJob Description: Create custom academic material for your class tailored to your topic and requirements."
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
st.title("Academic Content Generator")

# Inputs for academic content
grade_level = st.selectbox("Grade Level:", ["5th", "6th", "7th", "8th"])
text_length = st.number_input("Text Length (words):", min_value=50, max_value=500, value=200)
genre = st.selectbox("Genre:", ["fiction", "non-fiction", "poetry", "drama"])
topic = st.text_input("Topic:", "friendship")
context = st.text_area("Context:", "A story about two friends overcoming challenges together")

if st.button("Generate Content"):
    academic_content = {
        "grade_level": grade_level,
        "text_length": text_length,
        "genre": genre,
        "topic": topic,
        "context": context,
    }

    if api_key:
        with st.spinner("Generating content..."):
            result = call_openai_api(academic_content)
            st.success("Content Generation Complete!")
            st.text_area("Generated Content:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
