import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Project-Based Learning Plan Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
project_description = st.text_input("Project Topic or Description (e.g., OCR):")

if st.button("Generate Project Plan"):
    if project_description:
        # Prepare the prompt for the API
        Project_based_learning = {
            "grade_level": grade_level,
            "topic or project description": project_description,
        }

        prompt = (
            f"You are acting like a senior software engineer. The user will provide keywords or a description of a project. "
            f"Generate a plan on how to create the entire project:\n\n"
            f"generate_keywords: {json.dumps(Project_based_learning, indent=4)}\n\n"
            "Job Description: AI language tutor who can help you learn a new language on your own.\n\n"
            "Please generate a project plan based on the user topics or project description. You must strictly follow the prompt and description. "
            "Provide a project description on how to plan the project, followed by implementation steps with explanations."
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
            project_plan = data["choices"][0]["message"]["content"]
            st.write("### Project Plan:")
            st.write(project_plan)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a project description.")

