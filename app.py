import os
import streamlit as st
import google.generativeai as genai


genai.configure(api_key="") #enter your api key


model = genai.GenerativeModel(model_name="gemini-1.5-flash")
generation_config = {
    "temperature": 0,  #
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Survey Data 
survey_data = {
    "mental_state": None,
    "living_situation": None,
    "challenges": None,
}


def create_survey():
    st.header("Post-Disaster Mental Health Check-In")
    st.write("Please answer the following questions to help us understand your situation.")

    # Mental State
    mental_state = st.selectbox(
        "How would you describe your current mental state?",
        ["Anxious", "Depressed", "Angry", "Scared", "Overwhelmed", "Calm", "Hopeful"],
    )

    # Living Situation
    living_situation = st.selectbox(
        "What is your current living situation?",
        ["At home", "In temporary housing", "With family/friends", "Sheltered", "Other"],
    )

    # Current Challenges
    challenges = st.text_area(
        "What are some of the biggest challenges you're facing right now?"
    )

    if st.button("Submit Survey"):
        st.session_state.survey_data = {
            "mental_state": mental_state,
            "living_situation": living_situation,
            "challenges": challenges,
        }
        st.success("Thank you for completing the survey!")
        st.write("Now, ask me a question about your current situation.")

def personalized_advice():
    if "survey_data" not in st.session_state:
        st.warning("Please complete the survey first.")
        return

    user_question = st.text_input("Ask me a question:")

    if user_question:
        
        chat_session = model.start_chat()

        
        prompt = f"""
        User: {user_question}
        User's Mental State: {st.session_state.survey_data['mental_state']}
        User's Living Situation: {st.session_state.survey_data['living_situation']}
        User's Challenges: {st.session_state.survey_data['challenges']}

        Provide a helpful and empathetic response to the user's question, taking into account their current mental state, living situation, and challenges.
        """

        
        response = chat_session.send_message(prompt)
        advice = response.text

        st.write(advice)


st.title("Post-Disaster Mental Health Support")
create_survey()
personalized_advice()