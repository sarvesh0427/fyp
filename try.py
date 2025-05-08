import streamlit as st

import about
import confession
import pickle

with open('label_encoder.pkl', 'rb') as file:
    data = pickle.load(file)
# Page configuration
# st.set_page_config(page_title="Mental Health Assistant")
st.set_page_config(
    page_title="Mind Mitra",           # Title shown in browser tab
    page_icon= "img.png",  # You can use an emoji or image
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Chatbot","Anonymous Confession Wall","About"])

# Simulated prediction function (can be replaced with a real ML model)
def simulate_prediction():
    prediction = model.predict([user_text])  # Wrap in a list to match expected input shape
    return prediction[0]

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
    st.title("Mind Mitra-AI Mental Health Assistant")
    st.write("### Enter your symptoms below:")

    user_input = st.text_area("Symptoms", placeholder="e.g., feeling sad, anxious, trouble sleeping...")

    if st.button("Predict"):
        if user_input.strip():
            # Static prediction for demonstration
            prediction = "Anxiety"
            st.success(f"Possible Illness: {prediction}")

            # Precautions or tips for anxiety
            st.markdown("### 🧘 Precautions and Tips for Managing Anxiety:")
            st.markdown("""
            - 💤 Ensure you get enough **sleep** and maintain a consistent sleep schedule.
            - 🏃‍♀️ **Exercise** regularly to help reduce stress hormones.
            - 🍎 Eat a **balanced diet** and stay hydrated.
            - 🧘 Practice **deep breathing**, **meditation**, or **yoga**.
            - 📵 Limit **caffeine**, **alcohol**, and **screen time**.
            - 🗣 Talk to a **trusted friend** or a **mental health professional**.
            - 📝 Try **journaling** to express your thoughts and emotions.
            """)
        else:
            st.warning("Please enter some symptoms to get a prediction.")

# Chatbot section
elif section == "Chatbot":
    import chatbot
    chatbot.chatbot_display()

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
