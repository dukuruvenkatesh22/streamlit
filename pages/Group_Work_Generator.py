import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(group_work_generator, job_description):
    prompt = (
        f"Generate a group work activity for students to collaborate on for any subject, topic or objective:\n\n"
        f"generate_questions: {json.dumps(group_work_generator, indent=4)}\n\n"
        f"Job Description: {job_description}\n\n"
        "Please generate a group work activity for students to collaborate on for any subject, topic or objective. Every group should have 4 students, and the total students should be divided into groups. Strictly follow the prompt."
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
st.title("Group Work Activity Generator")

# Inputs for group work activity
grade_level = st.selectbox("Grade Level:", ["10th", "9th", "8th", "7th", "6th"])
total_students = st.number_input("Total Students:", min_value=1, value=30)
group_size = st.number_input("Group Size:", min_value=1, value=4)
activity_duration = st.text_input("Activity Duration:", "30 minutes")
topic_objective = st.text_input("Topic or Objective:", "science")

job_description = st.text_area("Job Description:", 
    "Create a group work activity for students to collaborate on for any subject, topic, or objective.")

if st.button("Generate Group Work Activity"):
    group_work_generator = {
        "Grade Level:": grade_level,
        "total students:": total_students,
        "Group Size:": group_size,
        "Activity duration:": activity_duration,
        "Topic or objective:": topic_objective,
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(group_work_generator, job_description)
            st.success("Generation Complete!")
            st.text_area("Generated Group Work Activity:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
