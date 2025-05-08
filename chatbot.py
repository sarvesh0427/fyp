import streamlit as st

def chatbot_display():
    st.title("Mental Health Chatbot")
    st.write("Let's talk. How are you feeling today?")

    # Initialize chat history and step counter
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_step" not in st.session_state:
        st.session_state.chat_step = 0

    # Input box for user
    user_message = st.text_input("You:", key="chat_input", placeholder="Type your message here...")

    if user_message and st.session_state.get("last_message") != user_message:
        st.session_state.chat_history.append(("You", user_message))
        st.session_state.last_message = user_message

        # Basic hardcoded conversation steps
        step = st.session_state.chat_step
        if step == 0:
            bot_reply = "Hi there! I'm here to listen. Can you tell me how you're feeling?"
        elif step == 1:
            bot_reply = "I'm sorry you're going through this. What's been on your mind lately?"
        elif step == 2:
            bot_reply = "It’s okay to feel overwhelmed. Talking helps. Remember, you’re not alone."
        else:
            bot_reply = "Thank you for sharing. If you’d like to continue, consider speaking with a counselor."

        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.chat_step += 1

    # Show chat history
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**🧠 Mental Health Bot:** {message}")