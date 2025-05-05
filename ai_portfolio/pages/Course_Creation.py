import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("API key not found. Please set the OPENAI_API_KEY in your .env file.")
    st.stop()

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

st.title("Course and Question Generator")

# Section for course generation
st.header("Generate Course Outlines")

with st.form("course_form"):
    num_courses = st.number_input("Number of Courses", min_value=1, step=1)
    
    courses = []
    for i in range(num_courses):
        st.subheader(f"Course {i + 1}")
        course_name = st.text_input(f"Course Name {i + 1}", key=f"course_name_{i}")
        course_length = st.text_input(f"Course Length {i + 1} (e.g., 10 pages)", key=f"course_length_{i}")
        number_of_chapters = st.number_input(f"Number of Chapters {i + 1}", min_value=1, step=1, key=f"number_of_chapters_{i}")
        courses.append({
            "course_name": course_name,
            "course_length": course_length,
            "number_of_chapters": number_of_chapters,
        })
    
    submitted = st.form_submit_button("Generate Courses")

    if submitted:
        for idx, course in enumerate(courses):
            if course["course_name"] and course["course_length"] and course["number_of_chapters"]:
                # Call OpenAI API to generate course outline
                prompt = (
                            f"You are like link a senior content creator and Generate detailed content for a course titled '{course_name}' with a length of {course_length}. "
                            f"The course should consist of {number_of_chapters} chapters "
                            f"Each chapter should have a title, headings, subheadings, and a brief description."
                         )
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                course_outline = response.choices[0].message['content'].strip()
                st.success(f"Course '{course['course_name']}' generated!")
                st.text_area(f"Course Outline {idx + 1}", value=course_outline, height=200)

# Section for question generation
st.header("Generate Questions")

with st.form("question_form"):
    chapter_number = st.number_input("Chapter Number", min_value=1, step=1)
    number_of_activity = st.number_input("Number of Activities", min_value=1, step=1)
    activity_type = st.selectbox("Activity Type", ["Multiple Choice", "True/False", "Matching", "Short Answer"])
    number_of_questions = st.number_input("Number of Questions per Activity", min_value=1, step=1)
    submitted_q = st.form_submit_button("Generate Questions")

    if submitted_q:
        # Call OpenAI API to generate questions
        prompt = (
            f"Generate {number_of_activity} sets of {number_of_questions} {activity_type} questions "
            f"for chapter {chapter_number}."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        questions = response.choices[0].message['content'].strip()
        st.success(f"{number_of_activity} {activity_type} activities generated!")
        st.text_area("Generated Activities", value=questions, height=200)
