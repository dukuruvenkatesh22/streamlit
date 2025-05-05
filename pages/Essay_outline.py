import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Essay Outline Generator")

# Inputs for the user
topic = st.text_input("Essay Topic (e.g., The Importance of Friendship):")
grade_level = st.selectbox("Grade Level:", ["5th", "6th", "7th", "8th"])
guidelines = st.text_area("Guidelines (e.g., Include main ideas, arguments, and supporting evidence):")

if st.button("Generate Essay Outline"):
    if topic and guidelines:
        # Prepare the prompt for the API
        essay_planner = {
            "topic": topic,
            "grade_level": grade_level,
            "guidelines": guidelines,
        }

        prompt = (
            f"Generate a structured essay outline for a {essay_planner['grade_level']} grade student on the topic of '{essay_planner['topic']}'.\n\n"
            f"The outline should include the main ideas, arguments, and supporting evidence. It should serve as a roadmap for the writing process, helping students clarify their thoughts, establish logical connections between ideas, and ensure a clear and coherent structure.\n\n"
            f"Guidelines: {essay_planner['guidelines']}\n\n"
            "Please provide a detailed outline."
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
            "temperature": 0.7,  # Adjusted for clarity
            "max_tokens": 1000,  # Adjust as needed for the length of the outline
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
            essay_outline = data["choices"][0]["message"]["content"]
            st.write("### Essay Outline:")
            st.write(essay_outline)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please fill in all fields.")

