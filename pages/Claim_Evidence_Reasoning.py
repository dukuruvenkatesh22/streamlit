import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(claim_reasoning, job_description):
    prompt = (
        f"Generate AI generated Claim-Evidence-Reasoning (CER) structured approach used to guide students in constructing and communicating scientific explanations for phenomena, observations, or experimental results. It helps students develop critical thinking skills, scientific reasoning abilities, and proficiency in communicating their understanding of scientific concepts.:\n\n"
        f"generate_questions: {json.dumps(claim_reasoning, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please Generate AI generated Claim-Evidence-Reasoning (CER) structured approach used to guide students in constructing and communicating scientific explanations for phenomena, observations, or experimental results. It helps students develop critical thinking skills, scientific reasoning abilities, and proficiency in communicating their understanding of scientific concepts, strictly follow the prompt and generate."
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
st.title("Claim-Evidence-Reasoning Generator")

# Inputs for claim reasoning
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
topic = st.text_input("Topic:", "statistics")
problem = st.text_area("Problem Statement:", "x=4,y=7,z=x*6+y+4+1, x+y+z=?")

job_description = st.text_area("Job Description:", 
    "AI generated Claim-Evidence-Reasoning (CER) structured approach used to guide students in constructing and communicating scientific explanations for phenomena, observations, or experimental results. It helps students develop critical thinking skills, scientific reasoning abilities, and proficiency in communicating their understanding of scientific concepts.")

if st.button("Generate Claim-Evidence-Reasoning"):
    claim_reasoning = {
        "Grade Level:": grade_level,
        "topic": topic,
        "problem": problem
    }

    if api_key:
        with st.spinner("Generating..."):
            cer_result = call_openai_api(claim_reasoning, job_description)
            st.success("Generation Complete!")
            st.text_area("Claim, Evidence, Reasoning:", cer_result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
