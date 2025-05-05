import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Coding Tutor")

# Inputs for the user
experience_level = st.selectbox("Experience Level:", ["beginner", "intermediate", "advanced"])
coding_language = st.text_input("The Coding Language(s) You Want Assistance With (e.g., Python):")

if st.button("Get Coding Assistance"):
    if coding_language:
        # Prepare the prompt for the API
        Learn_coding = {
            "Experience Level": experience_level,
            "The Coding Language(s) You Want Assistance With": coding_language,
        }

        prompt = (
            "You are acting as a Coding Tutor. You must work on user The Coding Language(s) You Want Assistance With experience level. "
            "Your task is to provide informative and helpful responses, including important coding concepts, relevant code snippets, and examples to help the user understand better. "
            "If you do not know the answer, respond with: 'I do not know, please give me more details about that.'\n\n"
            f"Context:\n{json.dumps(Learn_coding, indent=4)}\n\n"
            "Please answer the user's question based on the user requirements and provide examples where applicable."
        )

        # API request payload
        payload = {
            "model": "gpt-4",  # Use the correct model name for GPT-4
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 1,
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
            response_text = data["choices"][0]["message"]["content"]
            st.write("### Response:")
            st.write(response_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a coding language.")

