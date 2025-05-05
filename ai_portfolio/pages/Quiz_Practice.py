import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Quiz Practice Question Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
topic = st.text_input("Topic (e.g., Artificial Intelligence):", "Artificial Intelligence")
num_questions = st.number_input("Number of Questions:", min_value=1, max_value=20, value=10)

if st.button("Generate Quiz Questions"):
    if topic:
        # Prepare the input for the API
        Quiz_practice = {
            "Grade Level:": grade_level,
            "topic": topic,
            "num of questions": str(num_questions),
        }

        job_description = "Generate questions based on the given quiz topic."

        # Prepare the prompt for the API
        prompt = (
            f"Generate Quiz practice questions based on the given topic:\n\n"
            f"generate_questions: {json.dumps(Quiz_practice, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate Quiz practice questions based on the given topic. The questions should be multiple choice. After generating the questions, provide the correct answers."
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
            questions_text = data["choices"][0]["message"]["content"]
            st.write("### Generated Quiz Questions:")
            st.write(questions_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a topic.")
