import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Mind Mantra",
    page_icon="streamlit/img1.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles for UI/UX with bold sidebar font
st.markdown("""
<style>
/* General font */
html, body, [class*="css"] {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
}

/* Sidebar container */
[data-testid="stSidebar"] {
    background-color: #3CB371;
    padding: 20px 15px;
    border-radius: 0px 10px 10px 0px;
}

/* Sidebar text - titles, labels, spans, radio text */
[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: bold !important;
}

/* Sidebar radio buttons */
.css-1v0mbdj > div > div {
    background-color: white;
    border-radius: 10px;
    padding: 6px 10px;
    margin: 5px 0;
    transition: all 0.3s ease;
    font-weight: bold;
    color: #3CB371;
}
.css-1v0mbdj > div > div:hover {
    background-color: #2E8B57;
    color: white;
}

/* Main App Background */
.stApp {
    background-color: #f9f9f9;
    padding: 1rem;
}

/* Footer */
footer, footer p {
    text-align: center;
    font-size: 14px;
    color: #888;
}

/* Buttons */
button[kind="primary"] {
    background-color: #3CB371 !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: bold;
    transition: all 0.2s ease-in-out;
}
button[kind="primary"]:hover {
    background-color: #2E8B57 !important;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# Import your modules
import home
import fhome
import confession
import about

# Sidebar navigation
st.sidebar.title("🧠 Mind Mantra")
section = st.sidebar.radio("Go to", ["🏠 Home", "📝 Anonymous Confession Wall", "ℹ️ About"])

# Section logic
if section == "🏠 Home":
    fhome.fhome_show()
elif section == "📝 Anonymous Confession Wall":
    confession.confess()
elif section == "ℹ️ About":
    about.about_show()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #666; margin-top: 20px;'>
    © 2025 Final Year Project | School of Engineering, Pokhara University – Nepal
</p>
""", unsafe_allow_html=True)
