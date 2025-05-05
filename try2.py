import streamlit as st
import joblib
import re

# Load model and label encoder
model = joblib.load('mental_health_model.pkl')
le = joblib.load('label_encoder.pkl')

# Known symptom feature list (must match training)
all_symptoms = [
    'low_mood', 'loss_of_interest', 'fatigue', 'sleep_disturbance',
    'feeling_worthless', 'appetite_changes', 'restlessness',
    'excessive_worry', 'irritability', 'muscle_tension','trouble_concentrating',
    'sleep_problems','rapid_heartbeat','shortness_of_breath','sweating',
    'chest_pain','dizziness','fear_of_losing_control','fear_of_dying','avoidance_behavior',
    'persistent_fear_of_attacks','mood_swing','elevated_mood','reduced_need_for_sleep',
    'impulsive_behavior','racing_thoughts'
]

# Page configuration
st.set_page_config(page_title="Mental Health Assistant", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Chatbot"])

# Function to match text input to known symptoms
def map_text_to_symptoms(text):
    symptoms_found = []
    for symptom in all_symptoms:
        if re.search(symptom.replace('_', ' '), text.lower()):
            symptoms_found.append(symptom)
    return symptoms_found

# Prediction function
def predict_disease(symptom_list):
    input_data = [1 if symptom in symptom_list else 0 for symptom in all_symptoms]
    prediction = model.predict([input_data])
    return le.inverse_transform(prediction)[0]

# Simple chatbot response logic
def get_chatbot_response(user_input):
    user_input = user_input.lower()
    if any(word in user_input for word in ["sad", "depressed", "down"]):
        return "I'm sorry you're feeling this way. Would you like to talk more about what's been bothering you?"
    elif any(word in user_input for word in ["anxious", "nervous", "worried"]):
        return "Anxiety can be really tough. Deep breaths can help. Do you want some techniques to manage it?"
    elif any(word in user_input for word in ["angry", "mad", "frustrated"]):
        return "It's okay to feel angry sometimes. Want to share what triggered it?"
    else:
        return "I'm here for you. Can you tell me a bit more about how you're feeling?"

# ------------------ Streamlit Home Section ------------------
section = "Home"  # This would usually come from a sidebar or nav if you had sections

if section == "Home":
    st.title("Mental Health Assistant")
    st.write("### Enter your symptoms below:")

    user_input = st.text_area("Symptoms", placeholder="e.g., feeling sad, anxious, trouble sleeping...")

    if st.button("Predict"):
        if user_input.strip():
            symptoms = map_text_to_symptoms(user_input)
            if not symptoms:
                st.warning("Couldn't detect any known symptoms. Try using words like 'fatigue', 'low mood', 'restlessness', etc.")
            else:
                prediction = predict_disease(symptoms)
                st.success(f"🧠 Predicted Condition: **{prediction}**")
        else:
            st.warning("Please enter some symptoms to get a prediction.")

# Chatbot section
elif section == "Chatbot":
    st.title("Mental Health Chatbot")
    st.write("Let's talk. How are you feeling today?")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Text input box always visible
    user_message = st.text_input("You:", key="chat_input", placeholder="Type your message here...")

    # Handle new message
    if user_message and st.session_state.get("last_message") != user_message:
        st.session_state.chat_history.append(("You", user_message))
        bot_reply = get_chatbot_response(user_message)
        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.last_message = user_message

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**🧠 Mental Health Bot:** {message}")