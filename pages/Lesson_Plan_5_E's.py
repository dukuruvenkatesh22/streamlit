import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("5E's Lesson Plan Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["5th", "6th", "7th", "8th"])
topic = st.text_input("Lesson Topic (e.g., Physics Temperature):")

if st.button("Generate Lesson Plan"):
    if topic:
        # Prepare the prompt for the API
        lesson_planner = {
            "grade_level": grade_level,
            "topic": topic,
        }

        job_description = "Create a 5E's lesson plan that promotes student engagement, inquiry-based learning, and conceptual understanding."

        prompt = (
            f"Using AI, generate a detailed 5E's lesson plan for {lesson_planner['grade_level']} grade students on the topic of {lesson_planner['topic']}.\n\n"
            f"The 5E's stand for Engage, Explore, Explain, Elaborate, and Evaluate, representing the sequential phases of the lesson.\n\n"
            f"Ensure the lesson plan includes activities and strategies that promote student engagement and inquiry-based learning. "
            f"Here is the job description for context: {job_description}\n\n"
            f"Please follow these guidelines and create an effective lesson plan."
        )

        # API request payload
        payload = {
            "model": "gpt-4",  # Correct model name for GPT-4
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,  # Slightly lower temperature for more focused responses
            "max_tokens": 1500,  # Adjust as needed for longer responses
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
            lesson_plan = data["choices"][0]["message"]["content"]
            st.write("### 5E's Lesson Plan:")
            st.write(lesson_plan)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a lesson topic.")

