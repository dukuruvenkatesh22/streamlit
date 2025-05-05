import streamlit as st
import openai
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = 'api'

def generate_questions(topic, count):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Generate {count} interview questions about {topic}."}
        ]
    )
    questions = response['choices'][0]['message']['content'].split('\n')
    return [question.strip() for question in questions if question.strip()]

def get_feedback(answer):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Provide feedback on this interview answer: {answer}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Initialize session state variables
if 'questions' not in st.session_state:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.current_question_index = 0
    st.session_state.score = 0

st.title("AI-Based Mock Interview")

# User input for topic and number of questions
topic = st.text_input("Enter a topic for the interview:")
num_questions = st.number_input("Select number of questions:", min_value=1, max_value=20, value=1)

if st.button("Start Interview"):
    st.session_state.questions = generate_questions(topic, num_questions)
    st.session_state.current_question_index = 0
    st.session_state.answers = []
    st.session_state.score = 0

if st.session_state.questions:
    question = st.session_state.questions[st.session_state.current_question_index]
    st.header("Question")
    st.write(question)

    # Microphone input for the answer
    st.header("Record Your Answer (15 seconds limit)")
    if st.button("Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening for 15 seconds...")
            try:
                audio = recognizer.listen(source, timeout=15)  # Set timeout to 15 seconds
                user_answer = recognizer.recognize_google(audio)
                st.success("You said: " + user_answer)
                
                # Store the answer
                st.session_state.answers.append(user_answer)
                
                # Get feedback
                feedback = get_feedback(user_answer)
                st.write("Feedback: ", feedback)
                st.session_state.score += 1  # Increment score for every answer provided
                
                st.session_state.current_question_index += 1  # Move to the next question
            except sr.WaitTimeoutError:
                st.warning("Recording stopped: No speech detected within 15 seconds.")
            except sr.UnknownValueError:
                st.error("Could not understand audio.")
            except sr.RequestError:
                st.error("Could not request results from Google Speech Recognition service.")

    # Check if all questions have been answered
    if st.session_state.current_question_index >= len(st.session_state.questions):
        st.success("Interview completed!")
        st.write(f"Your final score is: {st.session_state.score}/{len(st.session_state.questions)}")

# Display all previous questions and answers
if st.session_state.answers:
    st.header("Previous Questions and Feedback")
    for i in range(len(st.session_state.questions)):
        st.subheader("Question:")
        st.write(st.session_state.questions[i])
        st.subheader("Your Answer:")
        st.write(st.session_state.answers[i])
