import streamlit as st
import time

import streamlit as st
from decouple import config

# api_key = config("OPENAI_API_KEY")
questions = [
    "What is your name?",
    "How old are you?",
    "What is your current occupation?",
    "Where are you located (city/country)?",
    "What is your marital status?",
    # "Is this your first pregnancy?",
    # "Do you have children? If yes, how many?",
    # "What is your expected due date?",
    # "What trimester are you currently in?",
    # "How would you rate your current overall health?",
    # "Do you have any pre-existing medical conditions (e.g., diabetes, hypertension)?",
    # "Have you experienced any complications in this pregnancy (e.g., gestational diabetes, preeclampsia)?",
    # "Have you had any previous pregnancies? If yes, were there any complications in those pregnancies?",
    # "Do you have any allergies, especially to medication or food?",
    # "Are you currently taking any medications or supplements? If yes, please specify.",
    # "Have you had any surgeries in the past (related to fertility or otherwise)?",
    # "Have you experienced any miscarriages in the past?",
    # "Are there any hereditary conditions in your family that you are aware of?",
    # "Have you had regular prenatal checkups? If yes, when was your last checkup?",
    # "Have you undergone any fertility treatments (e.g., IVF, IUI)?",
    # "How would you describe your diet? Do you follow any specific diet plans (e.g., vegetarian, vegan)?",
    # "Do you exercise regularly? If yes, what type of exercises do you prefer?",
    # "How many hours of sleep do you get on average?",
    # "Do you smoke or drink alcohol? If yes, how often?",
    # "How do you manage stress during pregnancy?",
    # "Do you have any specific cultural or religious practices related to pregnancy or childbirth?",
    # "Do you have a birth plan or any specific preferences for childbirth (e.g., natural birth, C-section, epidural)?",
    # "Are you working with a midwife, obstetrician, or doula during your pregnancy?",
    # "What type of prenatal classes or resources are you currently using (e.g., birthing classes, lactation consultants)?",
    # "What are your concerns or fears about pregnancy and childbirth?",
]


# # API request headers
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {api_key}",
# }


st.title("Pregnancy Assistant")

if "user_details" not in st.session_state:
    st.session_state.user_details = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if len(st.session_state.user_details) < len(questions):

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display the current question
    with st.chat_message("assistant"):
        st.markdown(questions[st.session_state.current_question_index])

    # Get the user response
    prompt = st.chat_input("Your response", key="user_response")

    if prompt:
        # Save the user's answer
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.user_details.append(
            {
                "question": questions[st.session_state.current_question_index],
                "user_response": prompt,
            }
        )

        # Add to the message history

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": questions[st.session_state.current_question_index],
            }
        )

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Increment the question index for the next question
        st.session_state.current_question_index += 1

        if st.session_state.current_question_index == len(questions):
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Thank you for providing all the details! I now have all the necessary information to assist you during your pregnancy. If you have any specific questions, concerns, or topics you'd like more guidance on, feel free to ask, and I’ll be happy to help!",
                }
            )

        st.rerun()

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ensure the key for this chat_input is unique
    prompt = st.chat_input("Your query", key="final_query")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        # # API request payload
        # payload = {
        #     "model": "gpt-4o",
        #     "messages": [
        #         {
        #             "role": "system",
        #             "content": f"You are a helpful and compassionate pregnancy assistant. Your role is to assist users by answering their pregnancy-related questions and providing accurate, supportive, and personalized information. Use the following Q&A to understand the user's needs, health conditions, and preferences, and tailor your responses accordingly. {st.session_state.user_details}",
        #         },
        #         {"role": "user", "content": prompt},
        #     ],
        #     "max_tokens": 1500,
        # }

        # # Send the request to the OpenAI API to generate the legal document
        # response = requests.post(
        #     "https://api.openai.com/v1/chat/completions",
        #     headers=headers,
        #     json=payload,
        # )

        # # Process the response
        # data = response.json()
        # if response.status_code == 200:
        #     ai_response = data["choices"][0]["message"]["content"]
        # else:
        #     ai_response = ""
        time.sleep(5)
        with st.chat_message("assistant"):
            st.markdown("sample ai answer")

        st.session_state.messages.append({"role": "user", "content": prompt})

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "sample ai answer",
            }
        )
