import streamlit as st
import joblib
import numpy as np
import pandas as pd

model = joblib.load('mental_health_model.joblib')
symptom_list = joblib.load('symptoms_list.joblib')
user_input = st.text_area("Symptoms", placeholder="e.g., feeling sad, anxious, trouble sleeping...")
def home_show():
    st.header("Home Page")
    user_input = st.text_area("Symptoms", placeholder="e.g., feeling sad, anxious, trouble sleeping...")
    if user_input.strip():
        # Preprocess input: convert to lowercase, split on comma
        input_symptoms = [sym.strip().lower().replace(" ", "_") for sym in user_input.split(",")]

        # Create input vector
        input_vector = [1 if symptom in input_symptoms else 0 for symptom in symptom_list]
        input_df = pd.DataFrame([input_vector], columns=symptom_list)

        # Predict
        prediction = model.predict(input_df)[0]
        st.success(f"Based on your symptoms, you might be experiencing **{prediction}**.")
    else:
        st.warning("Please enter some symptoms to get a prediction.")