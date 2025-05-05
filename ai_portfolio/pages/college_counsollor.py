import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Career and College Counselor")

# Inputs
Career_counselor = {
    "grade_level": "10th",
    "Career or college counselor": "how to become data scientist",
}

job_description = "AI language tutor who can help you learn a new language on your own."

# Ask the user for a question about college or careers
user_question = st.text_input("Ask me a question about college or careers:")

if st.button("Get Answer"):
    if user_question:
        # Prepare the prompt for the API
        prompt = (
            "You are acting as a Career and College Counselor. The user will ask questions related to college or career paths. "
            "Your task is to provide informative and helpful responses to their questions. If you do not know the answer, respond with: "
            "'I do not know, please give me more details about that.'\n\n"
            f"Context:\n{json.dumps(Career_counselor, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            f"User Question: {user_question}\n\n"
            "Please answer the user's question based on the user requirement. you must answer carefully"
        )

        # API request payload
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
            st.write("Response:")
            st.write(response_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please enter a question.")
