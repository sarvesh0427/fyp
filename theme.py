# theme.py
import streamlit as st

def apply_theme():
    theme = st.session_state.get("theme", "light")

    if theme == "dark":
        css = """
        <style>
        body { background-color: #1e1e1e; color: #ffffff; }
        .stApp { background-color: #1e1e1e; color: white; }
        section[data-testid="stSidebar"] { background-color: #111; color: white; }
        div[data-testid="stHeader"] { background-color: #1e1e1e; color: white; }
        </style>
        """
    else:
        css = """
        <style>
        body { background-color: #ffffff; color: #000000; }
        .stApp { background-color: #ffffff; color: black; }
        section[data-testid="stSidebar"] { background-color: #f4f6f8; color: black; }
        div[data-testid="stHeader"] { background-color: #ffffff; color: black; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)
