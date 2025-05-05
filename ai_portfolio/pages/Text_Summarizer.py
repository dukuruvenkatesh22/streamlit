import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(text_summarizer, job_description):
    prompt = (
        f"Summarise any given input_text to the length you desire based on user requirement:\n\n"
        f"generate_questions: {json.dumps(text_summarizer, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please summarise any given text to the length you desire, strictly follow the prompt."
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
st.title("Text Summarizer")

# Inputs for summarization
input_text = st.text_area("Input Text:", 
    "Two simple experimental facts characterize the friction of sliding solids. First, the amount of friction is nearly independent of the area of contact... (Your text here)")
length = st.text_input("Desired Summary Length:", "70 words 1 paragraph")

job_description = "Summarise any given text to the length you desire."

if st.button("Generate Summary"):
    text_summarizer = {
        "input_text": input_text,
        "length": length,
    }

    if api_key:
        with st.spinner("Generating summary..."):
            result = call_openai_api(text_summarizer, job_description)
            st.success("Summary Generation Complete!")
            st.text_area("Generated Summary:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
