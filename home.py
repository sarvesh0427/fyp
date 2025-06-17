import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- Load Lottie Animation ---
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# Doctor-patient animation from lottie.com
lottie_mental = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

def home_show():
    # --- Custom CSS Styling ---
    st.markdown("""
    <style>
        .stApp { background-color: #0f0f0f; color: #f5f5f5; padding-top: 5px; }
        .title { font-size: 2.2em; font-weight: bold; text-align: center; margin-bottom: 0; }
        .subtitle { font-size: 1em; color: #bbbbbb; text-align: center; margin-bottom: 0.8em; }
        .label { text-align: center; font-size: 1.1em; margin-bottom: 0.5em; }
        .stTextInput>div>div>input {
            text-align: center; font-size: 0.95em; padding: 6px 10px;
            width: 100%; max-width: 400px; margin: auto; display: block;
        }
        .stButton button {
            width: 100%; max-width: 300px; margin: 5px auto; font-size: 1em;
        }
        .result {
            background-color: #14532d; color: white;
            padding: 0.8em; border-radius: 8px;
            margin-top: 1em; text-align: center;
        }
        .tips {
            font-size: 0.95em; line-height: 1.6;
            margin-top: 0.8em; max-width: 450px;
            margin-left: auto; margin-right: auto; text-align: left;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<div class='title'>🧠 Mind Mitra</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your AI Mental Health Companion</div>", unsafe_allow_html=True)

    # --- Animation ---
    if lottie_mental:
        st_lottie(lottie_mental, height=150)
    else:
        st.warning("⚠️ Could not load the animation.")

    # --- Symptom Input ---
    st.markdown("<div class='label'>🔍 Describe your symptoms:</div>", unsafe_allow_html=True)
    symptoms = st.text_input("", placeholder="e.g., feeling anxious, can’t sleep, low energy")

    # --- Prediction + Tips ---
    if st.button("Predict"):
        if symptoms.strip():
            predicted = "Anxiety"
            st.markdown(f"<div class='result'>🧾 Possible Condition: {predicted}</div>", unsafe_allow_html=True)

            st.markdown("### 💡 Tips & Precautions:", unsafe_allow_html=True)
            tips = [
                "🧘 Try 5–10 minutes of meditation or deep breathing.",
                "📝 Keep a mood journal to track patterns.",
                "🚶 Get sunlight and a short walk each day.",
                "📵 Reduce social media use before bedtime.",
                "🗣 Talk with someone you trust or a counselor.",
            ]
            st.markdown("<div class='tips'>" + "<br>".join(f"- {tip}" for tip in tips) + "</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter your symptoms first.")

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:gray;'>Made with ❤️ by students of Pokhara University | Final Year Project</p>",
        unsafe_allow_html=True
    )
