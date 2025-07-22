import streamlit as st
import joblib
from streamlit_lottie import st_lottie
import requests
import random
import os
import pandas as pd
from openpyxl import load_workbook
from fuzzywuzzy import process

def reset_all_states():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


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

def thome_show():

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

    st.header(" Mental Health Condition Predictor")

    # Default session state
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

    # Input container
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("### 📝 Enter Your Symptoms")
            st.text_area("", key="user_input", placeholder="e.g., sleep disturbance, irritability, dizziness...")

        with right_column:
            display_symptoms = [s.replace("_", " ") for s in symptoms]
            st.markdown("### 🩺 Or Select from the List")
            st.multiselect("", display_symptoms, key="selected_symptoms")

    # Predict button
    if st.button("💡 Predict Mental Health Condition"):
        st.session_state.follow_up_index = 0
        st.session_state.follow_up_answers = []
        st.session_state.follow_up_complete = False
        st.session_state.cleared = False
        st.session_state.follow_up_triggered = False  # reset

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

                if predicted_disease in follow_up_questions:
                    st.session_state.follow_up_questions = follow_up_questions[predicted_disease]
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

    # Follow-up question logic
    if st.session_state.get("follow_up_triggered") and not st.session_state.get("cleared"):

        disease = st.session_state.get("predicted_disease", "")
        questions = st.session_state.get("follow_up_questions", [])
        answers = st.session_state.get("follow_up_answers", [])
        index = st.session_state.get("follow_up_index", 0)

        st.markdown("### 🔍 Follow-up Questions")

        # Display all previously answered questions
        if answers:
            for i, ans in enumerate(answers):
                st.markdown(f"**Q{i + 1}: {questions[i]}**")
                st.markdown(f"🟩 Answer: **{ans}**")

        # Ask the next unanswered question
        if index < len(questions):
            st.markdown(f"**Q{index + 1}: {questions[index]}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes", key=f"yes_{index}"):
                    answers.append("Yes")
                    st.session_state.follow_up_answers = answers
                    st.session_state.follow_up_index = index + 1
                    st.rerun()
            with col2:
                if st.button("❌ No", key=f"no_{index}"):
                    answers.append("No")
                    st.session_state.follow_up_answers = answers
                    st.session_state.follow_up_index = index + 1
                    st.rerun()

        # After all questions answered
        elif index == len(questions):
            yes_count = answers.count("Yes")
            no_count = answers.count("No")

            if yes_count > no_count:
                st.success(f"✅ Based on your responses, it is likely that you are experiencing **{disease}**.")
                st.markdown("🧘 **Consider consulting a mental health professional for further support.**")
            else:
                st.info("❕ Based on your responses, it's less likely that you're experiencing a severe condition.")
                st.markdown(
                    "💬 _Still, if you're feeling unwell, please consider speaking to someone you trust or a mental health expert._")

            st.markdown("💡 _Note: This tool is informational. For real diagnosis, consult a professional._")

            # Show precaution tips
            precautions = []
            excel_path = os.path.join(base_dir, "..", "datasets", "precaution_dataset.xlsx")
            try:
                wb = load_workbook(excel_path)
                ws = wb.active
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if row[0] and row[1] and disease.strip().lower() == row[0].strip().lower():
                        precautions.append(row[1])
            except Exception as e:
                st.warning(f"⚠️ Could not load precautions: {e}")

            st.markdown("---")
            st.subheader("📋 Precaution or Self-care Tips:")
            if precautions:
                for i, tip in enumerate(precautions, 1):
                    st.markdown(f"**{i}.** {tip}")
            else:
                st.info("No specific precautions found for this condition.")

            # Clear session
            if st.button("🔄 Clear"):
                reset_all_states()

            # st.markdown(f"Do you want to know more about **{disease}**?")
            # col1, col2 = st.columns(2)
            # if col1.button("✅ Yes"):
            #     st.session_state.follow_up_answers.append("Yes")
            #     st.session_state.follow_up_index += 1
            #     st.rerun()  # Rerun to refresh view with updated state
            # if col2.button("❌ No"):
            #     st.session_state.follow_up_answers.append("No")
            #     st.session_state.follow_up_index += 1
            #     st.rerun()  # Rerun to refresh view with updated state

