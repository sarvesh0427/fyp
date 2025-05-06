import streamlit as st

def chatbot_display():
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