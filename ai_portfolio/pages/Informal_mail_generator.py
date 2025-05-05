import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(email_details):
    prompt = (
        "You are an informal email generator. Based on the following details, compose a casual email. Stop generating subject and don't give unnecessary data:\n"
        f"Recipient Details:\n"
        f"To: {email_details['to']}\n"
        f"Name: {email_details['name']}\n"
        f"Topic: {email_details['topic']}\n"
        f"Additional Information: {email_details['other_details']}\n\n"
        f"Sender Details:\n"
        f"From: {email_details['from']}\n"
        f"School: {email_details['school/college']}\n"
        f"Location: {email_details['place']}\n"
        f"Date: {email_details['date']}\n"
        "Make sure to include a friendly greeting, a brief introduction, the main message related to the topic, and a casual sign-off. Avoid any unnecessary details."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
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
st.title("Informal Email Generator")

# Inputs for email generation
to_email = st.text_input("Recipient Email:", "colleague@example.com")
name = st.text_input("Recipient Name:", "Amma")
from_email = st.text_input("Your Name:", "Venkatesh")
school_college = st.text_input("School/College Name:", "ABC High School")
place = st.text_input("Location:", "Cityville")
date = st.date_input("Date:", value=None)
topic = st.text_input("Topic:", "Pongal wishes to my mother")
other_details = st.text_area("Additional Information:", "None")

if st.button("Generate Email"):
    email_details = {
        "to": to_email,
        "name": name,
        "other_details": other_details,
        "from": from_email,
        "school/college": school_college,
        "place": place,
        "date": date.strftime("%B %d, %Y") if date else "Not specified",
        "topic": topic
    }

    if api_key:
        with st.spinner("Generating email..."):
            result = call_openai_api(email_details)
            st.success("Email Generation Complete!")
            st.text_area("Generated Email:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
