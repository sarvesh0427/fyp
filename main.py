import streamlit as st

import home
import chatbot
import confession
import about


st.set_page_config(
    page_title="Mind Mitra",
    page_icon= "img.png",
    layout="wide"
)

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