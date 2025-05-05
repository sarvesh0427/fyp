import streamlit as st

def about_show():
    st.title('About the Project')
    st.subheader("AI Powered Mental Health Assistant")
    st.write("""
        This project is a final year capstone project developed by a Computer Engineering student from the School of Engineering, Pokhara University. It is an AI-powered Mental Health Assistant System designed to assist individuals who are experiencing mental health challenges.
        """)
    st.subheader("The system offers:")
    st.markdown("""
        - Symptom-based prediction of mental health conditions.
        - Recommendations including therapy options, medicines, and professionals if necessary.
        - An AI-powered chatbot for users to open up and talk freely in a safe, supportive space.
        The goal of this platform is to provide accessible mental health support and encourage people to talk about their mental well-being without fear of judgment.
        """)


    st.subheader("⚠️ Disclaimer")
    st.write("""
        This platform is intended for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the guidance of a qualified mental health professional with any questions or concerns you may have regarding a medical condition.
        
        The recommendations provided by this system are based on available data and AI models and may not be fully accurate. The developer and affiliated institutions are not liable for any decisions made based on the information provided by this system.
        
        By using this platform, you agree to this disclaimer and understand that the system does not provide licensed medical or psychiatric care.
        """)