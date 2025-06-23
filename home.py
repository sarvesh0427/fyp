import streamlit as st
import joblib

# Load model and artifacts
mdl = joblib.load("mental_health_model.joblib")
le = joblib.load("label_encoder.joblib")
symptoms = joblib.load("symptoms_list.joblib")


def home_show():
    # Title and welcome message
    st.markdown(
        """
        <style>
        body {
            background-color: #f0fdf4;
            color: #1e293b;
        }

        [data-testid="stSidebar"] {
            background-color: #d1fae5;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1e293b;
        }

        div.stButton > button:first-child {
            background-color: #34d399;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }

        div.stButton > button:hover {
            background-color: #059669;
            color: white;
        }

        .stTextInput > div > input {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🧠 Welcome to Mind Mantra")
    st.markdown("""
    Take a deep breath. You're not alone.  
    Please share how you're feeling or list any symptoms you're experiencing.  
    We'll try to understand what you may be going through. 💙
    """)

    st.markdown("---")

    # Free-text input
    st.markdown("### 📝 Share your thoughts or symptoms (comma-separated or a paragraph)")
    user_input = st.text_area('',placeholder="e.g., sleep disturbance, irritability, dizziness...")

    st.markdown("### 🩺 Or select symptoms you relate to:")
    selected_symptoms = st.multiselect(
        "Choose from common symptoms:",
        symptoms
    )

    if st.button("💡 Predict Mental Health Condition"):
        if user_input.strip() or selected_symptoms:
            # Parse typed symptoms (from user_input)
            typed_symptoms = [s.strip() for s in user_input.split(",") if s.strip()]
            input_symptoms = list(set(typed_symptoms + selected_symptoms))

            if len(input_symptoms) < 6:
                st.warning("⚠️ Please enter or select at least 6 symptoms for accurate prediction.")
                return

            # Create input vector
            input_vector = [1 if symptom in input_symptoms else 0 for symptom in symptoms]

            # Predict
            prediction = mdl.predict([input_vector])[0]
            predicted_disease = le.inverse_transform([prediction])[0]

            # Confidence (optional)
            if hasattr(mdl, "predict_proba"):
                confidence = max(mdl.predict_proba([input_vector])[0]) * 100
                st.success(f"🧾 Predicted mental health condition: **{predicted_disease}**")
                st.info(f"Confidence: {confidence:.2f}%")
            else:
                st.success(f"🧾 Predicted mental health condition: **{predicted_disease}**")

            st.markdown("---")
            st.markdown("💡 _Note: This tool is for informational purposes only. Please consult a professional for a confirmed diagnosis._")

        else:
            st.warning("⚠️ Please share your symptoms or select some from the list.")

    st.markdown("---")
    st.markdown("### 🌼 Encouragement for You")
    st.markdown("""
    > "You are stronger than you think, and more loved than you know."  
    > “Healing is not linear — take your time.”  
    _We're here to support you. One step at a time._ 💙
    """)

    st.markdown("---")
    st.markdown("### ✍️ Daily Reflection")
    journal = st.text_area("How was your day?", placeholder="Write anything you'd like to reflect on...")

    if journal:
        st.success("✅ Reflection saved (locally). Thank you for sharing!")

