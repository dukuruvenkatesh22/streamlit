import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Language Learning Plan Generator")

# Inputs for the user
learning_language = st.text_input("Language being learned (e.g., English):")
native_language = st.text_input("Your native language (e.g., Hindi):")
tutor_help = st.text_input("Specific tutor assistance needed (e.g., food items):")
cefr_level = st.selectbox("CEFR Level:", ["basic", "A1", "A2", "B1", "B2", "C1", "C2"])

if st.button("Generate Learning Plan"):
    if learning_language and native_language and tutor_help:
        # Prepare the prompt for the API
        prompt = (
            f"You are acting as a senior language tutor, and the user will provide their learning language details, "
            f"their native language, and CEFR level. Based on this information, generate a learning plan that includes "
            f"basic vocabulary, common phrases, practical exercises, and tips for further learning. Strictly follow the "
            f"input and output format.\n\n"
            f"Input:\n"
            f"Language being learned: {learning_language}\n"
            f"Native language: {native_language}\n"
            f"Specific tutor assistance needed: {tutor_help}\n"
            f"CEFR Level: {cefr_level}\n\n"
            f"Please generate a learning plan based on the provided details that includes a study topic with practical "
            f"exercises such as translations, fill-in-the-blanks, and matching words. Additionally, provide a tip for "
            f"further learning based on the user's CEFR level."
        )

        # API request payload
        payload = {
            "model": "gpt-4",  # Use the correct model name for GPT-4
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 1,
            "max_tokens": 4095,
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
            learning_plan = data["choices"][0]["message"]["content"]
            st.write("### Learning Plan:")
            st.write(learning_plan)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please fill in all fields.")

