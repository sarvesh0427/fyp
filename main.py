import streamlit as st

st.set_page_config(
page_title="Mind Mantra",  # 👈 This is the name in the browser tab
page_icon="img.png",            # 👈 This is the icon (can be emoji or URL to .ico/.png)
layout="centered",         # Optional: "wide" or "centered"
initial_sidebar_state="expanded"  # Optional
)
import home
import chatbot
import confession
import about


# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Home", "Chatbot","Anonymous Confession Wall","About"])

if section == 'Home':
    home.home_show()

elif section == 'Chatbot':
    chatbot.chatbot_display()

elif section == 'Anonymous Confession Wall':
    confession.confess()

elif section == 'About':
    about.about_show()

# footer
st.markdown("---------")
# Centered footer using Markdown hack
st.markdown(
    "<p style='text-align: center;'>© 2025 Final Year Project | School of Engineering, Pokhara University - Nepal</p>",
    unsafe_allow_html=True
)