import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.title("Syllabus Generator")

# User input section
course_name = st.text_input("Enter the course name:")
num_chapters = st.number_input("Enter the number of chapters:", min_value=1, step=1)

if st.button("Generate Syllabus"):
    if course_name and num_chapters:
        try:
            prompt = (
                f"Generate a syllabus for the course '{course_name}' with {num_chapters} chapters. "
                f"Include a brief description for each chapter."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            syllabus = response['choices'][0]['message']['content']
            st.subheader("Generated Syllabus:")
            st.write(syllabus)

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please fill in both fields.")
