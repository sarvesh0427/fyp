import streamlit as st

import about
import confession

# Page configuration
st.set_page_config(page_title="Mental Health Assistant")

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Chatbot","Anonymous Confession Wall","About"])

# Simulated prediction function (can be replaced with a real ML model)
def simulate_prediction(symptoms):
    return "Based on your symptoms, you might be experiencing anxiety. Please consult a professional for proper diagnosis."

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

# Home section
if section == "Home":
    st.title("Mental Health Assistant")
    st.write("### Enter your symptoms below:")

    user_input = st.text_area("Symptoms", placeholder="e.g., feeling sad, anxious, trouble sleeping...")

    if st.button("Predict"):
        if user_input.strip():
            prediction = simulate_prediction(user_input)
            st.success(prediction)
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

elif section == "Anonymous Confession Wall":
    confession.confess()

elif section == "About":
    about.about_show()

# footer
st.markdown("---------")
# Centered footer using Markdown hack
st.markdown(
    "<p style='text-align: center;'>© 2025 Final Year Project | School of Engineering, Pokhara University - Nepal</p>",
    unsafe_allow_html=True
)
