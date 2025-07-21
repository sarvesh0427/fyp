import streamlit as st
import joblib
from streamlit_lottie import st_lottie
import requests
import random
import os
import pandas as pd
from openpyxl import load_workbook

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

def home_show():

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
            "Have you been feeling down or sad most of the day for over 2 weeks?",
            "Have you lost interest in activities you used to enjoy?",
            "Do you feel tired or low in energy most days?"
        ],
        "Anxiety": [
            "Do you often feel nervous or on edge, even without a clear reason?",
            "Is it hard to control your worrying?",
            "Does your anxiety interfere with your sleep or daily activities?"
        ],
        "Bipolar Disorder": [
            "Have you experienced extreme mood swings recently?",
            "Do you go through periods of high energy and impulsiveness, followed by deep sadness?",
            "Have your sleep or thinking patterns changed drastically?"
        ],
        "Panic Disorder": [
            "Do you experience sudden, intense fear that peaks in minutes?",
            "Do you worry about having another panic attack?"
        ],
        "Schizophrenia": [
            "Do you experience hallucinations (e.g., hearing voices) or delusions?",
            "Have others noticed you acting in strange or disconnected ways?"
        ],
        "Eating Disorder": [
            "Do you restrict food, binge eat, or purge to control your weight?",
            "Are you overly concerned about body shape or weight?"
        ],
        "ADHD (Attention Deficit Hyperactivity Disorder)": [
            "Do you have trouble focusing or staying organized?",
            "Do you act impulsively or get distracted easily, even in quiet settings?"
        ],
        "Dissociative Identity Disorder": [
            "Do you experience two or more identities or personality states?",
            "Do you sometimes lose time or forget actions you've done?"
        ],
        "Substance Use Disorder": [
            "Do you find it hard to stop using a substance, even if it causes problems?",
            "Have you experienced tolerance or withdrawal?"
        ],
        "Obsessive-Compulsive Disorder (OCD)": [
            "Do you have unwanted, intrusive thoughts that cause anxiety?",
            "Do you perform rituals or repetitive actions to reduce the anxiety?"
        ],
        "Post-Traumatic Stress Disorder (PTSD)": [
            "Have you experienced a traumatic event (e.g., accident, assault, disaster)?",
            "Do you have nightmares, flashbacks, or avoid reminders of the trauma?"
        ],
        "Borderline Personality Disorder": [
            "Do your emotions change rapidly, making it hard to maintain stable relationships?",
            "Do you often feel empty or fear being abandoned?"
        ],
        "Social Anxiety Disorder": [
            "Do you feel very anxious in social situations, like public speaking or being watched?",
            "Do you often avoid social events because of fear of embarrassment?"
        ],
        "Generalized Anxiety Disorder (GAD)": [
            "Have you experienced excessive worry about various things for 6 months or more?",
            "Do you often feel restless, tired, or irritable?"
        ],
        "Adjustment Disorder": [
            "Have your symptoms started after a major life change or stressful event?",
            "Are these feelings beyond what you expected for the situation?"
        ],
        "Insomnia": [
            "Do you have trouble falling or staying asleep, even when you're tired?",
            "Does lack of sleep affect your energy, focus, or mood?"
        ],
        "Autism Spectrum Disorder": [
            "Do you find it difficult to understand or respond to social cues?",
            "Do you have strong interests in specific topics or routines?"
        ],
        "Persistent Depressive Disorder": [
            "Have you felt consistently low or sad for more than 2 years?",
            "Is your mood low but not severe enough to stop you from doing daily tasks?"
        ],
        "Major Depressive Disorder": [
            "Are your depressive symptoms present almost every day?",
            "Do you have difficulty concentrating or making decisions?",
            "Have you had thoughts of self-harm or hopelessness?"
        ],
        "Separation Anxiety Disorder": [
            "Do you feel intense fear when separated from someone you’re emotionally attached to?",
            "Do you avoid being alone due to fear of separation?"
        ],
        "Dissociative Amnesia": [
            "Do you have gaps in your memory, especially around stressful events?",
            "Are you missing large parts of your personal history?"
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

    if st.session_state.get("follow_up_triggered") and not st.session_state.get("cleared", False):
        disease = st.session_state.get("predicted_disease")
        questions = follow_up_questions.get(disease, [])

        st.markdown(f"### 🧠 Follow-up Questions for **{disease}**")

        # Display previously answered questions
        for i in range(len(st.session_state.follow_up_answers)):
            st.markdown(f"**Q{i + 1}:** {questions[i]}")
            st.markdown(f"**Answer:** {st.session_state.follow_up_answers[i]}")

        # Ask the next unanswered question
        current_index = st.session_state.follow_up_index
        if current_index < len(questions):
            st.markdown(f"**Q{current_index + 1}:** {questions[current_index]}")
            col1, col2 = st.columns(2)
            if col1.button("✅ Yes", key=f"yes_{current_index}"):
                st.session_state.follow_up_answers.append("Yes")
                st.session_state.follow_up_index += 1
                st.rerun()  # Rerun to refresh view with updated state
            if col2.button("❌ No", key=f"no_{current_index}"):
                st.session_state.follow_up_answers.append("No")
                st.session_state.follow_up_index += 1
                st.rerun()  # Rerun to refresh view with updated state

        # Final result once all questions are answered
        if len(st.session_state.follow_up_answers) == len(questions) and not st.session_state.follow_up_complete:
            yes_count = st.session_state.follow_up_answers.count("Yes")
            st.session_state.follow_up_complete = True

            st.markdown("---")
            st.subheader("🧾 Predicted Result")

            if yes_count >= len(questions) / 2:
                st.success(f"Based on your responses, it's more likely you are suffering from **{disease}**.")
            else:
                st.info(f"You may have some symptoms of **{disease}**, but further evaluation is recommended.")

            # ========== Precaution Lookup ==========

            excel_path = os.path.join(base_dir,"..","datasets", "precaution_dataset.xlsx")
            precautions = []
            try:
                # Load workbook and worksheet
                wb = load_workbook(excel_path)
                ws = wb.active

                # Collect all precautions that match the predicted condition
                for row in ws.iter_rows(min_row=2, values_only=True):
                    disease_name, precaution_text = row[0], row[1]
                    if disease_name and st.session_state.predicted_disease.strip().lower() == disease_name.strip().lower():

                        if precaution_text and isinstance(precaution_text, str):
                            precautions.append(precaution_text)

            except FileNotFoundError:
                st.warning("⚠️ The precaution Excel file was not found. Please check the path.")
            except Exception as e:
                st.error(f"❌ An error occurred while reading the Excel file: {e}")

            st.markdown("---")
            # Display the precautions
            st.subheader("📋 Precaution or Self-care Tips:")
            if precautions:
                for i, tip in enumerate(precautions, 1):
                    st.markdown(f"**{i}.** {tip}")
            else:
                st.info("No specific precautions found for this condition.")

            # ========= Clear Button =========
            if st.button("🔄 Clear"):
                st.session_state.follow_up_index = 0
                st.session_state.follow_up_answers = []
                st.session_state.follow_up_complete = False
                st.session_state.follow_up_triggered = False
                st.session_state.predicted_disease = ""

                # Force rerun and skip all below
                st.experimental_set_query_params(clear="1")  # optional: clear URL parameters
                st.stop()  # ✅ stop Streamlit from continuing below this point

