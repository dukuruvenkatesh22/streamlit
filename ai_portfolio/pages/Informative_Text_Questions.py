import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Informative Text Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
topic = st.text_input("Topic (e.g., Artificial Intelligence):")

if st.button("Generate Informative Text"):
    if topic:
        # Prepare the input for the API
        Informative_text_questions = {
            "Grade Level:": grade_level,
            "topic": topic,
        }

        job_description = (
            "Leverage AI to instantly create a short text designed to add context to existing lessons "
            "or help inform students about any topic. All factual information should be reviewed by the "
            "professional educator prior to introduction to the student."
        )

        # Prepare the prompt for the API
        prompt = (
            f"Generate and leverage AI to instantly create a short text designed to add context to existing lessons or "
            f"help inform students about any topic. All factual information should be reviewed by the professional educator "
            f"prior to introduction to the student:\n\n"
            f"generate_questions: {json.dumps(Informative_text_questions, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate this informative text strictly following the prompt."
        )

        # API request payload
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 1,
            "max_tokens": 500,  # Adjust as necessary for length
        }

        # API request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # Send the request to the OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        # Process the response
        data = response.json()
        if response.status_code == 200:
            informative_text = data["choices"][0]["message"]["content"]
            st.write("### Informative Text:")
            st.write(informative_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a topic.")

