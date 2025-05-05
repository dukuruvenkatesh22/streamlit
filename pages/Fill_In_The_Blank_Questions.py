import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(fill_in_the_blanks, job_description):
    prompt = (
        f"You are an assistant to develop fill-in-the-blanks based on the job description and the number of questions strictly follow this:\n\n"
        f"generate_questions: {json.dumps(fill_in_the_blanks, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "You are an assistant to develop fill-in-the-blanks based on the job description and the number of questions strictly follow the prompt and generate the fill-in-the-blanks based on context or topic. After completion of generating questions, generate answers for the questions you generated. Strictly follow these instructions."
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
st.title("Fill-in-the-Blanks Generator")

# Inputs for fill-in-the-blanks
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic = st.text_input("Topic (optional):", "Machine Learning")
context = st.text_area("Context (optional):", 
    "Machine Learning tutorial covers basic and advanced concepts, specially designed to cater to both students and experienced working professionals. This machine learning tutorial helps you gain a solid introduction to the fundamentals of machine learning and explore a wide range of techniques, including supervised, unsupervised, and reinforcement learning.")
no_of_questions = st.number_input("Number of Questions:", min_value=1, max_value=20, value=10)

job_description = st.text_area("Job Description:", 
    "Type of assessment item where students are presented with a statement, sentence, or passage with one or more blanks, and they are required to fill in the missing words or phrases. Fill-in-the-blank questions are commonly used in quizzes, tests, worksheets, and other forms of assessment to evaluate students' understanding of key concepts, vocabulary, and factual knowledge.")

if st.button("Generate Fill-in-the-Blanks"):
    fill_in_the_blanks = {
        "Grade Level:": grade_level,
        "topic(optional)": topic,
        "context(optional)": context,
        "no of questions": str(no_of_questions),
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(fill_in_the_blanks, job_description)
            st.success("Generation Complete!")
            st.text_area("Generated Fill-in-the-Blanks and Answers:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
