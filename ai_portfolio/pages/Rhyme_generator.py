import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(rhyme_generator):
    job_description = (
        "With Artificial Intelligence, instantly create the linguistic phenomenon where two or more words end with the same or similar sounds. "
        "Rhymes are often used for their pleasing or rhythmic effect and are a common feature in various forms of literature and oral tradition. "
        "They serve to create patterns, establish a sense of musicality, and enhance the overall aesthetic appeal of the text."
    )

    prompt = (
        f"You act like a teacher. The user will provide keywords or topics; based on that, generate rhymes:\n\n"
        f"generate_keywords: {json.dumps(rhyme_generator, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Generate the rhymes based on the topic or keyword and grade level. "
        "Convert the generated content into the user's required language (generate both English and the specified language). "
        "Strictly follow the prompt."
    )

    payload = {
        "model": "gpt-4o-mini",
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
st.title("Rhyme Generator")

# Inputs for rhyme generation
grade_level = st.selectbox("Grade Level:", ["1st", "2nd", "3rd", "4th", "5th"])
topic = st.text_input("Topic or Keywords:", "Feeling happy")
language = st.text_input("Language:", "Telugu")

if st.button("Generate Rhymes"):
    rhyme_generator = {
        "grade_level": grade_level,
        "topic or keywords": topic,
        "language": language,
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(rhyme_generator)
            st.success("Rhyme Generation Complete!")
            st.text_area("Generated Rhymes:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
