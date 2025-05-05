import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("True/False Question Generator")

# Inputs for the user
grade_level = st.selectbox("Grade Level:", ["8th", "9th", "10th"])
subject = st.text_input("Subject (e.g., Chemistry):")
topic = st.text_input("Topic (optional, e.g., Periodic Table):")
no_of_questions = st.number_input("Number of Questions:", min_value=1, max_value=100, value=10)

if st.button("Generate Questions"):
    if subject:
        # Prepare the prompt for the API
        True_false_questions = {
            "Grade Level": grade_level,
            "Subject": subject,
            "Topic (optional)": topic,
            "No of Questions": no_of_questions,
        }

        job_description = ("Generate unlimited objective assessment items used to test students' knowledge, comprehension, "
                           "and understanding of a topic or concept or context. In these questions, students are presented "
                           "with a statement, and they must determine whether the statement is true or false based on their "
                           "understanding of the subject matter.")

        prompt = (
            f"You are an assistant to generate unlimited objective assessment items used to test students' knowledge, "
            f"comprehension, and understanding of a topic or concept or context. In these questions, students are presented "
            f"with a statement, and they must determine whether the statement is true or false based on their understanding "
            f"of the subject matter. Please follow the number of questions.\n\n"
            f"Generate questions: {json.dumps(True_false_questions, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate the questions followed by options (True or False). After completion of generating questions, "
            "generate answers for the questions you generated, strictly following this instruction."
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
            "temperature": 1,
            "max_tokens": 4096,
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
            st.write("### True/False Questions:")
            st.write(questions_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a subject.")

