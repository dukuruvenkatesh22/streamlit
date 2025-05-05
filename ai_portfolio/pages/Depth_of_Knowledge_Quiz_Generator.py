import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json
import PyPDF2

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Depth of Knowledge Quiz Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
topic = st.text_input("Topic (e.g., Geometry):")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if st.button("Generate Questions"):
    if uploaded_file is not None and topic:
        # Read the uploaded PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"

        # Prepare the prompt for the API
        Depth_knowledge_quiz_generator = {
            "grade_level": grade_level,
            "topic": topic,
        }

        job_description = "Create questions for all 4 Depth of Knowledge (DOK) levels for any topic or standard."

        prompt = (
            f"Generate a number of 4 Depth of Knowledge questions for the subject at the grade level, "
            f"covering the topics based on the provided PDF:\n\n"
            f"generate_questions: {json.dumps(Depth_knowledge_quiz_generator, indent=4)}\n\n"
            f"PDF Content: {pdf_text}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate questions for all 4 Depth of Knowledge (DOK) levels based on the above details."
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
            questions_text = data["choices"][0]["message"]["content"]
            st.write("### Depth of Knowledge Questions:")
            st.write(questions_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please upload a PDF and enter a topic.")

