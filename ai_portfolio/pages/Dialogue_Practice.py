import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(dialogue_practice, job_description):
    prompt = (
        f"Develop a skit of a two-person dialogue in an educational setting serves as a valuable tool for language learning, communication development, and interpersonal growth:\n\n"
        f"generate_questions: {json.dumps(dialogue_practice, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please develop a skit of a two-person dialogue in an educational setting, strictly following the prompt and acting as the second person."
    )

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
st.title("Dialogue Practice Generator")

# Inputs for dialogue generation
grade_level = st.selectbox("Grade Level:", ["10th", "11th", "12th"])
topic = st.text_input("Topic:", "About Machine Learning")
person_1 = st.text_input("Person 1 Name:", "Dukuru Venkatesh")
person_2 = st.text_input("Person 2 Name:", "Anushka Sharma")
num_dialogues = st.text_input("Number of Dialogues:", "6")

job_description = "Develop a skit of a two-person dialogue in an educational setting that serves as a valuable tool for language learning, communication development, and interpersonal growth."

if st.button("Generate Dialogue"):
    dialogue_practice = {
        "Grade Level:": grade_level,
        "topic": topic,
        "person 1": person_1,
        "person 2": person_2,
        "no of dialogues": num_dialogues,
    }

    if api_key:
        with st.spinner("Generating dialogue skit..."):
            result = call_openai_api(dialogue_practice, job_description)
            st.success("Dialogue Generation Complete!")
            st.text_area("Generated Dialogue:", result, height=400)
    else:
        st.error("API key not found. Please add it to the .env file.")
