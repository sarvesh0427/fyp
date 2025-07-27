import streamlit as st
import joblib
import os
import pandas as pd
import random
from openpyxl import load_workbook
from fuzzywuzzy import process
from streamlit_autorefresh import st_autorefresh
from follow_ups import follow_up_questions, quotes

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

        if not st.session_state.started_input:
            st_autorefresh(interval=20 * 1000, limit=None, key="quote_autorefresh")

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
                        <li>📝 <strong>Enter at least 7 symptoms</strong> (e.g., sleep disturbance, low mood, dizziness...)</li>
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
                st.warning("⚠️ Please enter at least 7 valid symptoms or if you are having only this symptoms then you may not have mental illness.")
            else:
                input_vector = [1 if symptom in matched else 0 for symptom in symptoms]
                prediction = mdl.predict([input_vector])[0]
                predicted_disease = le.inverse_transform([prediction])[0]

                st.session_state.predicted_disease = predicted_disease

                if predicted_disease in follow_up_questions:
                    questions_copy = follow_up_questions[predicted_disease][:]
                    random.shuffle(questions_copy)
                    st.session_state.follow_up_questions = questions_copy
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
            st.warning("⚠️ Please enter a symptoms.")

    # Follow-up question logic
    if st.session_state.get("follow_up_triggered") and not st.session_state.get("cleared"):

        disease = st.session_state.get("predicted_disease", "")
        questions = st.session_state.get("follow_up_questions", [])
        answers = st.session_state.get("follow_up_answers", [])
        index = st.session_state.get("follow_up_index", 0)

        st.markdown("---")
        st.markdown("### 🔍 Follow-up Questions")

        # Display all previously answered questions
        if answers:
            for i, ans in enumerate(answers):
                st.markdown(f"**Q{i + 1}: {questions[i]}**")
                st.markdown(f"🟩 Answer: **{ans}**")

        # Ask the next unanswered question
        if index < len(questions):
            st.markdown(f"**Q{index + 1}: {questions[index]}**")
            yes_col, no_col = st.columns(2)
            with yes_col:
                if st.button("✅ Yes", key=f"yes_{index}"):
                    answers.append("Yes")
                    st.session_state.follow_up_answers = answers
                    st.session_state.follow_up_index = index + 1
                    st.rerun()
            with no_col:
                if st.button("❌ No", key=f"no_{index}"):
                    answers.append("No")
                    st.session_state.follow_up_answers = answers
                    st.session_state.follow_up_index = index + 1
                    st.rerun()
        st.markdown('---')
        # Show only after all questions answered
        if index == len(questions):  # All questions answered
            yes_count = answers.count("Yes")
            no_count = answers.count("No")
            total_questions = len(questions)

            st.markdown("### 🧠 Interpretation")

            if yes_count >= 8:
                st.success(f"✅ Based on your responses, you are **very likely experiencing {disease}**.")
                st.markdown(
                    "🧘 **We strongly recommend speaking to a licensed mental health professional as soon as possible.**")

            elif 5 <= yes_count < 8:
                st.info(
                    f"ℹ️ Your answers suggest symptoms **related to {disease}**, though not necessarily severe.")
                st.markdown("💬 _It may be helpful to monitor your symptoms and consider professional guidance._")

            elif 2 <= yes_count < 5:
                st.info(f"❕ Some features of **{disease}** may be present, but not dominant.")
                st.markdown(
                    "📌 _Consider lifestyle support, self-care, and possibly a preliminary discussion with a mental health counselor._")

            else:  # yes_count < 2
                st.warning(
                    f"⚠️ Your symptoms do **not strongly align with {disease}**, but could indicate a different or more severe condition.")
                st.markdown(
                    "🔍 _Please consider seeking a comprehensive evaluation to rule out other possible concerns._")

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
            st.subheader("📋 Suggestion or Self-care Tips:")

            if precautions:
                # Toggle state
                if "show_all_precautions" not in st.session_state:
                    st.session_state.show_all_precautions = False

                # Show all or first 6
                to_show = precautions if st.session_state.show_all_precautions else precautions[:6]

                # Display tips
                for i, tip in enumerate(to_show, 1):
                    st.markdown(f"**{i}.** {tip}")

                if len(precautions) > 6:
                    toggle_label = "🔼 Show Less" if st.session_state.show_all_precautions else "🔽 Show More"
                    if st.button(toggle_label):
                        st.session_state.show_all_precautions = not st.session_state.show_all_precautions
                        st.rerun()
            else:
                st.info("No specific precautions found for this condition.")

        # Clear session button centered
        center_col = st.columns(2)
        with center_col[1]:  # Middle column
            if st.button("🔄 Clear"):
                reset_all_states()


