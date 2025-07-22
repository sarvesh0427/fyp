import streamlit as st
import joblib
from jinja2.sandbox import unsafe
from streamlit_lottie import st_lottie
import requests
import random
import os
import pandas as pd
from openpyxl import load_workbook
import ast
from fuzzywuzzy import process  # for fuzzy matching

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

def normalize_symptom(s):
    return s.strip().lower().replace("_", " ")

def get_closest_symptom(symptom, known_symptoms, threshold=80):
    match = process.extractOne(symptom, known_symptoms)
    if match and match[1] >= threshold:
        return match[0]
    return None

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
        "You are enough, just as you are.",
        "You alone are enough. You have nothing to prove to anybody",
        "Healing grows in honesty, openness, and the courage to speak",
        "Sometimes the people around you won't understand your journey",
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    illness_data_path = os.path.join(base_dir, "..", "datasets", "illness_dataset.csv")
    df_ill = pd.read_csv(illness_data_path)
    similar_name_path = os.path.join(base_dir, "..", "datasets", "similar_name.csv")
    df_sim = pd.read_csv(similar_name_path, encoding='ISO-8859-1')
    precaution_path = os.path.join(base_dir, "..", "datasets", "precaution_dataset.csv")
    df_precaution = pd.read_csv(precaution_path, encoding='ISO-8859-1')
    df_precaution['Disease'] = df_precaution['Disease'].str.lower().str.strip()

    st.markdown("""
        <h2 style='text-align: center;'> Welcome to <span style='color: #3CB371;'>Mind Mantra</span></h2>
    """, unsafe_allow_html=True)
    st_lottie(lottie_mental, height=150, key="mental")
    st.markdown(
        f"""
        <div style='text-align: center; font-size: 18px; color: #2E8B57; background-color: #E0F8E0; padding: 10px; border-radius: 10px;'>
            <strong>{random.choice(quotes)}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    symptoms = df_ill.columns[1:]
    normalized_column_map = {col.replace("_", " ").lower(): col for col in symptoms}
    all_normalized = list(normalized_column_map.keys())

    similar_name_map = {}
    for _, row in df_sim.iterrows():
        actual_symptom = row[0]
        for alt_name in row[1:]:
            if pd.notna(alt_name):
                key = str(alt_name).strip().lower().replace("_", " ")
                similar_name_map[key] = actual_symptom

    followup_path = os.path.join(base_dir, "..", "datasets", "followup_dataset.csv")
    df_followup = pd.read_csv(followup_path)
    df_followup['followup_questions'] = df_followup['followup_questions'].apply(ast.literal_eval)
    follow_up_questions = {
        row['predicted_condition'].strip().lower(): row['followup_questions']
        for _, row in df_followup.iterrows()
    }

    st.header(" Mental Health Condition Predictor")

    for key, default in {
        "follow_up_index": 0,
        "follow_up_answers": [],
        "follow_up_complete": False,
        "follow_up_triggered": False,
        "user_input": "",
        "selected_symptoms": [],
        "cleared": False
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("### 📝 Enter Your Symptoms")
            st.text_area("", key="user_input", placeholder="e.g., sleep disturbance, irritability, dizziness...")

        with right_column:
            display_symptoms = [s.replace("_", " ") for s in symptoms]
            st.markdown("### 🩺 Or Select from the List")
            st.multiselect("", display_symptoms, key="selected_symptoms")

    if st.button("💡 Predict Mental Health Condition"):
        st.session_state.follow_up_index = 0
        st.session_state.follow_up_answers = []
        st.session_state.follow_up_complete = False
        st.session_state.cleared = False

        user_input = st.session_state.user_input
        selected_symptoms = st.session_state.selected_symptoms

        if user_input.strip() or selected_symptoms:
            typed_symptoms_raw = [normalize_symptom(s) for s in user_input.split(",") if s.strip()]
            selected_symptoms_raw = [normalize_symptom(s) for s in selected_symptoms]
            all_entered = list(set(typed_symptoms_raw + selected_symptoms_raw))

            matched, unmatched, corrected = [], [], []
            for sym in all_entered:
                if sym in normalized_column_map:
                    matched.append(normalized_column_map[sym])
                elif sym in similar_name_map:
                    matched.append(similar_name_map[sym])
                else:
                    closest = get_closest_symptom(sym, all_normalized)
                    if closest:
                        corrected.append((sym, closest))
                        matched.append(normalized_column_map[closest])
                    else:
                        unmatched.append(sym)

            if len(matched) < 6:
                st.warning("⚠️ Please enter or select at least 6 valid symptoms.")
            else:
                input_vector = [1 if symptom in matched else 0 for symptom in symptoms]
                prediction = mdl.predict([input_vector])[0]
                predicted_disease = le.inverse_transform([prediction])[0]
                st.session_state.predicted_disease = predicted_disease

                if predicted_disease.lower() in follow_up_questions:
                    st.session_state.follow_up_triggered = True
                else:
                    st.success(f"Predicted mental health condition: **{predicted_disease}**")
                    st.session_state.follow_up_triggered = False

            if unmatched:
                st.warning("⚠️ Unrecognized symptoms: " + ", ".join(unmatched))
            if corrected:
                for wrong, fixed in corrected:
                    st.info(f"✅ Interpreted '{wrong}' as '{fixed}'")
        else:
            st.warning("⚠️ Please enter or select symptoms.")

    # Follow-up logic
    if st.session_state.get("follow_up_triggered") and not st.session_state.get("cleared"):
        disease = st.session_state.get("predicted_disease")
        questions = follow_up_questions.get(disease, [])

        st.markdown(f"### Follow-up Questions for **{disease}**")

        for i in range(len(st.session_state.follow_up_answers)):
            if i < len(questions):
                st.markdown(f"**Q{i + 1}:** {questions[i]}")
                st.markdown(f"**Answer:** {st.session_state.follow_up_answers[i]}")
            else:
                # If answers exist but questions don't (unexpected), just show answer
                st.markdown(f"**Answer {i + 1}:** {st.session_state.follow_up_answers[i]}")

        current_index = st.session_state.follow_up_index
        if current_index < len(questions):
            st.markdown(f"**Q{current_index + 1}:** {questions[current_index]}")
            col1, col2 = st.columns(2)
            if col1.button("✅ Yes", key=f"yes_{current_index}"):
                st.session_state.follow_up_answers.append("Yes")
                st.session_state.follow_up_index += 1
                st.rerun()
            if col2.button("❌ No", key=f"no_{current_index}"):
                st.session_state.follow_up_answers.append("No")
                st.session_state.follow_up_index += 1
                st.rerun()

        if len(st.session_state.follow_up_answers) == len(questions) and not st.session_state.follow_up_complete:
            st.session_state.follow_up_complete = True
            yes_count = st.session_state.follow_up_answers.count("Yes")

            st.markdown("---")
            st.subheader("🧾 Predicted Result")

            if yes_count >= len(questions) / 2:
                st.success(f"Based on your responses, it's more likely you are suffering from **{disease}**.")
            else:
                st.info(f"You may have some symptoms of **{disease}**, but further evaluation is recommended.")

            st.markdown("💡 _Note: This tool is informational. For real diagnosis, consult a professional._")

            # Precaution retrieval
            precautions = []
            excel_path = os.path.join(base_dir, "..", "datasets", "precaution_dataset.xlsx")
            try:
                wb = load_workbook(excel_path)
                ws = wb.active
                for row in ws.iter_rows(min_row=2, values_only=True):
                    disease_name, precaution_text = row[0], row[1]
                    if disease_name and precaution_text and disease.strip().lower() == disease_name.strip().lower():
                        precautions.append(precaution_text)
            except Exception as e:
                st.warning(f"⚠️ Could not load precautions: {e}")

            st.markdown("---")
            st.subheader("📋 Precaution or Self-care Tips:")
            if precautions:
                for i, tip in enumerate(precautions, 1):
                    st.markdown(f"**{i}.** {tip}")
            else:
                st.info("No specific precautions found for this condition.")

            # Clear button
            if st.button("🧹 Clear"):
                st.session_state.follow_up_triggered = False
                st.session_state.predicted_disease = None
                st.session_state.follow_up_index = 0
                st.session_state.follow_up_answers = []
                st.session_state.follow_up_complete = False
                st.session_state.user_input = ""
                st.session_state.selected_symptoms = []
                st.session_state.cleared = True
                st.rerun()

            st.markdown(f"Do you want to know more about **{disease}**?")
            col1, col2 = st.columns(2)
            if col1.button("✅ Yes"):
                st.session_state.follow_up_answers.append("Yes")
                st.session_state.follow_up_index += 1
                st.rerun()  # Rerun to refresh view with updated state
            if col2.button("❌ No"):
                st.session_state.follow_up_answers.append("No")
                st.session_state.follow_up_index += 1
                st.rerun()  # Rerun to refresh view with updated state

