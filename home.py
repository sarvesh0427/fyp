
import streamlit as st
import joblib
import random
from streamlit_lottie import st_lottie
import requests
import time
import random
# Load model and artifacts
mdl = joblib.load("mental_health_model.joblib")
le = joblib.load("label_encoder.joblib")
symptoms = joblib.load("symptoms_list.joblib")

# Load Lottie animations
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

lottie_mental = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

# Custom CSS for soft green styling (Predict button + Sidebar only)
st.markdown("""
    <style>
    /* Soft green Predict button */
    div.stButton > button:first-child {
        background-color: #a8d5ba;
        color: black;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 1em;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #94c9aa;
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

def home_show():
#     quotes = [
#     "Believe you can and you're halfway there.",
#     "Every day may not be good... but there is something good in every day.",
#     "Your present circumstances don’t determine where you can go; they merely determine where you start.",
#     "Healing takes time, and that's okay.",
#     "You are enough, just as you are."
# ]

# # This will refresh the app every 45,000 milliseconds (45 seconds)
# st_autorefresh = st.experimental_singleton(lambda: st.experimental_rerun)
# st.experimental_set_query_params(refresh=int(time.time()))

# # Get current time and use it to pick quote
# index = int(time.time() // 45) % len(quotes)

# st.info(f"*{quotes[index]}*")

# # Use Streamlit's built-in function to auto refresh every 45 seconds
# st.experimental_memo.clear()  # Clear cache to avoid showing same quote
# st.experimental_rerun()


    # 1. Motivational Quote
    quotes = [
        "Believe you can and you're halfway there.",
        "Every day may not be good... but there is something good in every day.",
        "Your present circumstances don’t determine where you can go; they merely determine where you start.",
        "Healing takes time, and that's okay.",
        "You are enough, just as you are."
    ]
    st.info(f"*{random.choice(quotes)}*")
   
    # 2. Welcome Title + Animation
    
    st.markdown("""
        <h2 style='text-align: center;'>
            🧠 Welcome to <span style='color: #3CB371;'>Mind Mantra</span>
        </h2>
    """, unsafe_allow_html=True)
    st_lottie(lottie_mental, height=150, key="mental")


    # 3. Symptom Text Input
    st.markdown("### 📝 Enter Your Symptoms")
    user_input = st.text_area("", placeholder="e.g., sleep disturbance, irritability, dizziness...")

    # 4. Symptom Multiselect
    st.markdown("### 🩺 Or Select from the List")
    selected_symptoms = st.multiselect("", symptoms)

    # Predict Button
    if st.button("💡 Predict Mental Health Condition"):
        if user_input.strip() or selected_symptoms:
            typed_symptoms = [s.strip() for s in user_input.split(",") if s.strip()]
            input_symptoms = list(set(typed_symptoms + selected_symptoms))

            if len(input_symptoms) < 6:
                st.warning("⚠️ Please enter or select at least 6 symptoms.")
                return

            input_vector = [1 if symptom in input_symptoms else 0 for symptom in symptoms]
            prediction = mdl.predict([input_vector])[0]
            predicted_disease = le.inverse_transform([prediction])[0]

            if hasattr(mdl, "predict_proba"):
                confidence = max(mdl.predict_proba([input_vector])[0]) * 100
                st.success(f"🧾 Predicted Condition: **{predicted_disease}**")
                st.info(f"Confidence: {confidence:.2f}%")
            else:
                st.success(f"🧾 Predicted Condition: **{predicted_disease}**")

            st.markdown("💡 _Note: This tool is informational. For real diagnosis, consult a professional._")
        else:
            st.warning("⚠️ Please enter or select symptoms.")

