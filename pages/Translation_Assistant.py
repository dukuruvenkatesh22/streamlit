import streamlit as st
import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API for translation
def translate_text(translation_request):
    text_to_translate = translation_request["text"]
    source_language = translation_request["source_language"]
    target_language = translation_request["target_language"]

    prompt = (
        f"Translate the following text from {source_language} to {target_language}:\n\n"
        f"{text_to_translate}\n\n"
        f"Please provide the translation in {target_language}."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 150,
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
st.title("Language Translator")

# Inputs for translation
text_to_translate = st.text_area("Text to Translate:", "Hello, how are you?")
source_language = st.selectbox("Source Language:", ["English", "Hindi", "Spanish", "French", "German"])
target_language = st.selectbox("Target Language:", ["Hindi", "English", "Spanish", "French", "German"])

if st.button("Translate"):
    translation_request = {
        "text": text_to_translate,
        "source_language": source_language,
        "target_language": target_language,
    }

    if api_key:
        with st.spinner("Translating..."):
            result = translate_text(translation_request)
            st.success("Translation Complete!")
            st.text_area("Translated Text:", result, height=200)
    else:
        st.error("API key not found. Please add it to the .env file.")
