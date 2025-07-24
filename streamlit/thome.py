import streamlit as st
import joblib
from streamlit_lottie import st_lottie
import requests
import random
import os
import pandas as pd
from openpyxl import load_workbook
from fuzzywuzzy import process
import time
from streamlit_autorefresh import st_autorefresh

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

def thome_show():
    def reset_all_states():
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    if "started_input" not in st.session_state:
        st.session_state.started_input = False

    def normalize_symptom(s):
        return s.strip().lower().replace("_", " ")

    def get_closest_symptom(symptom, known_symptoms, threshold=80):
        match = process.extractOne(symptom, known_symptoms)
        if match and match[1] >= threshold:
            return match[0]
        return None

    # Upper section (just ui)
    if not st.session_state.started_input:
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
        if not st.session_state.started_input:
            st_autorefresh(interval=15 * 1000, limit=None, key="quote_autorefresh")

            if "quote_index" not in st.session_state:
                st.session_state.quote_index = 0

            st.session_state.quote_index = (st.session_state.quote_index + 1) % len(quotes)
            current_quote = quotes[st.session_state.quote_index]

            st.markdown(
                f"""
                <div style='
                    text-align: center;
                    font-size: 18px;
                    color: #2E8B57;
                    background-color: #E0F8E0;
                    padding: 10px;
                    border-radius: 10px;
                    margin-top: -90px;  /* Move upward by 20px */
                '>
                    <strong>{current_quote}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap');

            .header-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: -50px;   /* reduced top margin here */
                padding: 20px;
                font-family: 'Montserrat', sans-serif;
                text-align: center;
                animation: fadeIn 5s ease-in-out;
            }

            .welcome-text {
                font-size: 2rem;
                color: #555;
                margin: 0;
                font-weight: 500;
            }

            .app-name {
                font-size: 4rem;
                background: linear-gradient(90deg, #3CB371, #2E8B57);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
                margin: 0;
                line-height: 1.1;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-15px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @media screen and (max-width: 768px) {
                .welcome-text {
                    font-size: 1.5rem;
                }
                .app-name {
                    font-size: 2.5rem;
                }
            }
            </style>

            <div class="header-container">
                <div class="welcome-text">Welcome to</div>
                <div class="app-name">Mind Mantra</div>
            </div>
        """, unsafe_allow_html=True)


    base_dir = os.path.dirname(os.path.abspath(__file__))
    illness_data_path = os.path.join(base_dir, "..", "datasets", "illness_dataset.csv")
    df_ill = pd.read_csv(illness_data_path)
    similar_name_path = os.path.join(base_dir, "..", "datasets", "similar_name.csv")
    df_sim = pd.read_csv(similar_name_path, encoding='ISO-8859-1')
    precaution_path = os.path.join(base_dir, "..", "datasets", "precaution_dataset.csv")
    df_precaution = pd.read_csv(precaution_path, encoding='ISO-8859-1')
    df_precaution['Disease'] = df_precaution['Disease'].str.lower().str.strip()


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
            "Are your daily responsibilities harder to manage because of these feelings?"
        ],
        "Anxiety": [
            "Do you often feel nervous or on edge, even without a clear reason?",
            "Is it hard to control your worrying?",
        ],
        "Bipolar Disorder": [
            "Have you experienced extreme mood swings recently?",
            "Have these shifts affected your work, finances, or relationships?"
        ],
        "Panic Disorder": [
            "Have you had multiple panic attacks over the past month?",
            "Do you avoid situations or places out of fear of having an attack?"
        ],
        "Schizophrenia": [
            "Have unusual thoughts or perceptions persisted for over a month?",
            "Have these experiences disrupted your work or personal life?"
        ],
        "Eating Disorder": [
            "Have you been concerned about food or body image for several months?",
            "Is your eating behavior affecting your health or daily functioning?"
        ],
        "ADHD (Attention Deficit Hyperactivity Disorder)": [
            "Have you struggled with attention or hyperactivity since childhood?",
            "Do these difficulties impact your school, job, or daily activities?"
        ],
        "Dissociative Identity Disorder": [
            "Have you felt like multiple identities or memory gaps have persisted over weeks or months?",
            "Have these experiences disrupted your daily life or relationships?"
        ],
        "Substance Use Disorder": [
            "Have you been using substances regularly for over a month?",
            "Has substance use interfered with your responsibilities or relationships?"
        ],
        "Obsessive-Compulsive Disorder (OCD)": [
            "Have your unwanted thoughts or rituals lasted more than an hour a day for over two weeks?",
            "Do they interfere with your ability to focus or get things done?"
        ],
        "Post-Traumatic Stress Disorder (PTSD)": [
            "Have you had distressing memories or reactions for more than a month after a traumatic event?",
            "Has this trauma affected your relationships or ability to concentrate?"
        ],
        "Borderline Personality Disorder": [
            "Have your emotional struggles lasted for several months or longer?",
            "Have your intense emotions or relationships caused problems at work or home?"
        ],
        "Social Anxiety Disorder": [
            "Have you been avoiding social situations for six months or more?",
            "Has this anxiety made it difficult to go to work or school?"
        ],
        "Generalized Anxiety Disorder (GAD)": [
            "Have you experienced excessive worry about various things for 6 months or more?",
            "Has this worry made it difficult to focus or enjoy life?"
        ],
        "Adjustment Disorder": [
            "Did your emotional symptoms begin soon after a specific stressor or change?",
            "Is the stress still affecting your ability to function or move forward?"
        ],
        "Insomnia": [
            "Have you had trouble sleeping at least three nights a week for the past month?",
            "Does your poor sleep affect your energy or concentration during the day?"
        ],
        "Autism Spectrum Disorder": [
            "Have you experienced social or communication challenges since early childhood?",
            "Do these challenges affect your ability to connect with others or work independently?"
        ],
        "Persistent Depressive Disorder": [
            "Have you felt low or hopeless for more days than not for over two years?",
            "Are these long-term feelings making everyday life harder to manage?"
        ],
        "Major Depressive Disorder": [
            "Have you felt down or unmotivated for more than two weeks?",
            "Have these feelings made it hard to complete everyday tasks?"
        ],
        "Separation Anxiety Disorder": [
            "Have you felt extreme distress when away from someone for over four weeks?",
            "Has this fear kept you from going places or being independent?"
        ],
        "Dissociative Amnesia": [
            "Has the memory loss lasted more than a few hours or days?",
            "Is it interfering with your ability to function or feel safe?"
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
            # st.markdown("### Follow the instructions")
            st.markdown(
                """
                <div style='
                    background-color: #f0f9f4;
                    color: #2E8B57;
                    padding: 20px;
                    border-radius: 12px;
                    font-size: 16px;
                    text-align: left;
                    margin-top: 20px;
                '>
                    <p>📋 <strong>Follow the Instructions Below:</strong></p>
                    <ul style="padding-left: 20px; margin: 0;">
                        <li>📝 <strong>Enter at least 7 symptoms</strong> (e.g., sleep disturbance, anxiety, dizziness...)</li>
                        <li>💡 Click the <strong>'Predict Mental Health Condition'</strong> button to continue</li>
                        <li>🔍 Answer follow-up questions to receive helpful tips and condition insights</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )

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

            if len(matched) < 7:
                st.warning("⚠️ Please enter or select at least 7 valid symptoms.")
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

            # Load precautions from Excel
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

            # UI Section
            st.markdown("---")
            st.subheader("📋 Precaution or Self-care Tips:")

            if precautions:
                # Initialize toggle state
                if "show_all_precautions" not in st.session_state:
                    st.session_state.show_all_precautions = False

                # Decide how many to show
                if st.session_state.show_all_precautions:
                    to_show = precautions
                else:
                    to_show = precautions[:6]

                # Display tips
                for i, tip in enumerate(to_show, 1):
                    st.markdown(f"**{i}.** {tip}")

                # Show toggle button only if more than 6 tips exist
                if len(precautions) > 6:
                    if st.session_state.show_all_precautions:
                        if st.button("🔼 Show Less"):
                            st.session_state.show_all_precautions = False
                            st.rerun()
                    else:
                        if st.button("🔽Show More"):
                            st.session_state.show_all_precautions = True
                            st.rerun()
            else:
                st.info("No specific precautions found for this condition.")

            # Clear session
            if st.button("🔄 Clear"):
                reset_all_states()


