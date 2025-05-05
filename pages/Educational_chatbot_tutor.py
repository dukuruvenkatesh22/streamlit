import streamlit as st
import openai
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate responses using GPT-4
def generate_response(user_input, mode):
    if mode == "Step-by-Step Guidance":
        prompt = f"Provide a step-by-step guidance for: {user_input}"
    else:
        prompt = f"Answer the following question: {user_input}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio, can you repeat again."
    except sr.RequestError:
        return "Could not request results."

# Streamlit app layout
st.title("Educational Tutor Chatbot")

# Mode selection
mode = st.radio("Select Response Mode:", ("Step-by-Step Guidance", "Full Answer"))

# User input
user_input = st.text_input("Ask your question:")

if st.button("Submit"):
    if user_input:
        response = generate_response(user_input, mode)
        st.write("Chatbot: ", response)
    else:
        st.write("Please enter a question.")

# Voice input button
if st.button("Speak"):
    user_input = recognize_speech()
    st.write("You said: ", user_input)
    if user_input:  # If speech was recognized, generate a response
        response = generate_response(user_input, mode)
        st.write("Chatbot: ", response)
