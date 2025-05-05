import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Multiple Choice Question Generator")

# Inputs for the user
topic = st.text_input("Topic (e.g., Energy and Work):", "Energy and Work")
standard = st.selectbox("Standard:", ["10th standard", "11th standard", "12th standard"])
num_questions = st.number_input("Number of Questions:", min_value=1, max_value=10, value=5)
context = st.text_input("Context (optional):", "None")

if st.button("Generate Multiple Choice Questions"):
    if topic:
        # Prepare the input for the API
        multiple_choice = {
            "topic": topic,
            "context(optional)": context,
            "standard": standard,
            "num_questions": str(num_questions)
        }

        job_description = (
            "You are acting like a teacher to create a multiple choice assessment based on any topic, standard(s), or criteria!"
        )

        # Prepare the prompt for the API
        prompt = (
            f"Generate multiple choice questions on the topic. After generating all the MCQs, provide the correct answers for each question:\n\n"
            f"generate_questions: {json.dumps(multiple_choice, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate multiple choice questions based on the above details."
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
            agreement_text = data["choices"][0]["message"]["content"]
            st.write("### Multiple Choice Questions:")
            st.write(agreement_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please fill in all fields.")
