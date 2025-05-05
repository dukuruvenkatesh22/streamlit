import streamlit as st
import requests
import json
import os
import pandas as pd  # Importing pandas
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to call OpenAI API
def call_openai_api(email_details):
    prompt = (
        "You are a professional email generator. Based on the following details, compose a formal and professional email:\n\n"
        f"Recipient Details:\n"
        f"To: {email_details['to']}\n"
        f"Name: {email_details['name']}\n"
        f"Topic: {email_details['topic']}\n"
        f"Additional Information: {email_details['other_details']}\n\n"
        f"Sender Details:\n"
        f"From: {email_details['from']}\n"
        f"Class: {email_details['class']}\n"
        f"School: {email_details['school']}\n"
        f"Location: {email_details['place']}\n"
        f"Date: {email_details['date']}\n"
        f"Subject: {email_details['subject']}\n\n"
        "Ensure the email includes a proper salutation, a clear introduction mentioning the topic, the main message, "
        "a closing statement, and a professional sign-off. Format the email appropriately."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
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
st.title("Formal Email Generator")

# Inputs for email details
to = st.text_input("Recipient Email:", "colleague@example.com")
name = st.text_input("Recipient Name:", "John Doe")
other_details = st.text_input("Additional Information:", "None")
from_name = st.text_input("Your Name:", "Jane Smith")
class_name = st.text_input("Class:", "10th Grade")
school = st.text_input("School:", "ABC High School")
place = st.text_input("Location:", "Cityville")
date = st.date_input("Date:", value=pd.to_datetime("2024-10-08"))
subject = st.text_input("Subject:", "Report Submission")
topic = st.text_input("Topic:", "Monthly Report")

if st.button("Generate Email"):
    email_details = {
        "to": to,
        "name": name,
        "other_details": other_details,
        "from": from_name,
        "class": class_name,
        "school": school,
        "place": place,
        "date": date.strftime("%B %d, %Y"),
        "subject": subject,
        "topic": topic
    }

    if api_key:
        with st.spinner("Generating..."):
            result = call_openai_api(email_details)
            st.success("Email Generation Complete!")
            st.text_area("Generated Email:", result, height=300)
    else:
        st.error("API key not found. Please add it to the .env file.")
