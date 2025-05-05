import os
import requests
import streamlit as st
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Math Story Problem Generator")

# Inputs for the user
topic = st.text_input("Topic (e.g., Geometry):", "geometry")
standard = st.selectbox("Standard:", ["10th standard", "11th standard", "12th standard"])
num_questions = st.number_input("Number of Questions:", min_value=1, max_value=10, value=5)
story_scenario = st.text_input("Story Scenario (e.g., Football):", "football")

if st.button("Generate Math Story Problems"):
    if topic and story_scenario:
        # Prepare the input for the API
        Math_story_problems = {
            "topic": topic,
            "standard": standard,
            "num_questions": str(num_questions),
            "story_scenario": story_scenario,
        }

        job_description = (
            "Generate customised maths story / word problems, connecting it to a particular story on any concept you're teaching."
        )

        # Prepare the prompt for the API
        prompt = (
            f"Generate a number of questions for customised maths story / word problems, connecting it to a particular story on any concept you're teaching:\n\n"
            f"generate_questions: {json.dumps(Math_story_problems, indent=4)}\n\n"
            f"Job Description: {job_description}\n\n"
            "Please generate questions for customised maths story / word problems, connecting it to a particular story on any concept you're teaching."
        )

        # API request payload
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
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
            agreement_text = data["choices"][0]["message"]["content"]
            st.write("### Math Story Problems:")
            st.write(agreement_text)
        else:
            st.error(f"Error: {response.status_code} - {data.get('error', {}).get('message', 'No message')}")
    else:
        st.warning("Please fill in all fields.")
