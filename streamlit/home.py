import streamlit as st
import joblib
from streamlit_lottie import st_lottie
import requests
import random
import os
import pandas as pd

# Get current file directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to model files inside ../model_train/
model_path = os.path.join(base_dir, "..", "model_training", "mental_health_model.joblib")
encoder_path = os.path.join(base_dir, "..", "model_training", "label_encoder.joblib")
symptoms_path = os.path.join(base_dir, "..", "model_training", "symptoms_list.joblib")

# Load model and artifacts
mdl = joblib.load(model_path)
le = joblib.load(encoder_path)
symptoms = joblib.load(symptoms_path)

def fhome_show():

    def load_lottie_url(url: str):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
        except:
            pass
        return None

    lottie_mental = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")

    st.markdown("""
        <style>
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

    quotes = [
        "Believe you can and you're halfway there.",
        "Every day may not be good... but there is something good in every day.",
        "Your present circumstances don’t determine where you can go; they merely determine where you start.",
        "Healing takes time, and that's okay.",
        "You are enough, just as you are."
    ]
    st.info(f"*{random.choice(quotes)}*")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    illness_data_path = os.path.join(base_dir, "..", "datasets", "illness_dataset.csv")
    df_ill = pd.read_csv(illness_data_path)
    similar_name_path = os.path.join(base_dir, "..", "datasets", "similar_name.csv")
    df_sim = pd.read_csv(similar_name_path, encoding='ISO-8859-1')
    precaution_path = os.path.join(base_dir, "..", "datasets", "precaution_dataset.csv")
    df_precaution = pd.read_csv(precaution_path, encoding='ISO-8859-1')
    df_precaution['Disease'] = df_precaution['Disease'].str.lower().str.strip()

    st.markdown("""
        <h2 style='text-align: center;'>🧠 Welcome to <span style='color: #3CB371;'>Mind Mantra</span></h2>
    """, unsafe_allow_html=True)
    st_lottie(lottie_mental, height=150, key="mental")

    symptoms = df_ill.columns[1:]
    normalized_column_map = {col.replace("_", " ").lower(): col for col in symptoms}

    similar_name_map = {}
    for _, row in df_sim.iterrows():
        actual_symptom = row[0]
        for alt_name in row[1:]:
            if pd.notna(alt_name):
                key = str(alt_name).strip().lower().replace("_", " ")
                similar_name_map[key] = actual_symptom

    follow_up_questions = {
        "Depression": [
            "Have you been feeling hopeless or helpless recently?",
            "Have you been experiencing these symptoms for more than 2 weeks?"
        ],
        "Anxiety": [
            "Do these symptoms interfere with your daily functioning?",
            "Do you often feel restless or on edge?"
        ],
        "Bipolar Disorder": [
            "Have you experienced extreme mood swings recently?",
            "Do you sometimes feel overly energetic and then extremely low?"
        ],
        "PTSD": [
            "Did your symptoms start after a traumatic event?",
            "Do you experience flashbacks or nightmares about the event?"
        ],
        "OCD": [
            "Do you feel compelled to repeat behaviors or thoughts frequently?",
            "Do you find it hard to stop obsessive thinking or compulsive actions?"
        ]
    }

    st.title("🧠 Mental Health Condition Predictor")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("### 📝 Enter Your Symptoms")
            user_input = st.text_area("", placeholder="e.g., sleep disturbance, irritability, dizziness...")
        with right_column:
            display_symptoms = [s.replace("_", " ") for s in symptoms]
            symptom_display_to_actual = dict(zip(display_symptoms, symptoms))
            st.markdown("### 🩺 Or Select from the List")
            selected_display_symptoms = st.multiselect("", display_symptoms)
            selected_symptoms = [symptom_display_to_actual[s] for s in selected_display_symptoms]

    if "follow_up_index" not in st.session_state:
        st.session_state.follow_up_index = 0
    if "follow_up_answers" not in st.session_state:
        st.session_state.follow_up_answers = []
    if "follow_up_complete" not in st.session_state:
        st.session_state.follow_up_complete = False
    if "follow_up_triggered" not in st.session_state:
        st.session_state.follow_up_triggered = False

    if st.button("💡 Predict Mental Health Condition"):
        st.session_state.follow_up_index = 0
        st.session_state.follow_up_answers = []
        st.session_state.follow_up_complete = False

        if user_input.strip() or selected_symptoms:
            typed_symptoms_raw = [s.strip().lower().replace("_", " ") for s in user_input.split(",") if s.strip()]
            selected_symptoms_raw = [s.replace("_", " ").lower() for s in selected_symptoms]
            all_entered = list(set(typed_symptoms_raw + selected_symptoms_raw))

            matched = []
            unmatched = []

            for sym in all_entered:
                if sym in normalized_column_map:
                    matched.append(normalized_column_map[sym])
                elif sym in similar_name_map:
                    matched.append(similar_name_map[sym])
                else:
                    unmatched.append(sym)

            if len(matched) < 6:
                st.warning("⚠️ Please enter or select at least 6 valid symptoms.")
            else:
                input_vector = [1 if symptom in matched else 0 for symptom in symptoms]
                prediction = mdl.predict([input_vector])[0]
                predicted_disease = le.inverse_transform([prediction])[0]
                st.session_state.predicted_disease = predicted_disease

                if predicted_disease in follow_up_questions:
                    st.session_state.follow_up_triggered = True
                else:
                    st.success(f"Predicted mental health condition: **{predicted_disease}**")
                    st.session_state.follow_up_triggered = False

            if unmatched:
                st.warning("⚠️ Unrecognized symptoms: " + ", ".join(unmatched))
        else:
            st.warning("⚠️ Please enter or select symptoms.")

    if st.session_state.get("follow_up_triggered"):
        disease = st.session_state.get("predicted_disease")
        questions = follow_up_questions.get(disease, [])

        st.markdown(f"### 🧠 Follow-up Questions for **{disease}**")

        for i, q in enumerate(questions):
            if i < len(st.session_state.follow_up_answers):
                answer = st.session_state.follow_up_answers[i]
                st.markdown(f"**Q{i+1}:** {q}")
                st.markdown(f"**Answer:** {answer}")
            elif i == st.session_state.follow_up_index and not st.session_state.follow_up_complete:
                st.markdown(f"**Q{i+1}:** {q}")
                col1, col2 = st.columns(2)
                if col1.button("✅ Yes", key=f"yes_{i}"):
                    st.session_state.follow_up_answers.append("Yes")
                    st.session_state.follow_up_index += 1
                if col2.button("❌ No", key=f"no_{i}"):
                    st.session_state.follow_up_answers.append("No")
                    st.session_state.follow_up_index += 1

        if len(st.session_state.follow_up_answers) == len(questions) and not st.session_state.follow_up_complete:
            yes_count = st.session_state.follow_up_answers.count("Yes")
            st.session_state.follow_up_complete = True

            if yes_count >= len(questions) / 2:
                st.success(f"Based on your responses, it's more likely you are suffering from **{disease}**.")
            else:
                st.info(f"You may have symptoms of **{disease}**, but further evaluation is recommended.")
