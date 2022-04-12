import streamlit as st
from FER import analyze_face
from tone import analyze_tone

def load_view():
    with st.sidebar:
        st.header("Hello form analysis")
    uploaded_file = st.file_uploader("Choose a file")
    st.video(uploaded_file)
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col2:
        analyzeBtn = st.button('Analyze Facial')
        if analyzeBtn:
            if uploaded_file:
                FER_score, FER_weights = analyze_face("./test_interviews/"+uploaded_file.name)
                st.write(f'The score based on face expression analysis is: {FER_score}')
            else:
                st.write("ERROR: No video found, please select a video and try again!")

    with col3:
        reportsBtn = st.button('Analyze tone')
        if reportsBtn:
            if uploaded_file:
                tone_score, tone_weights = analyze_tone("./test_interviews/"+uploaded_file.name)
                st.write(f'The score based on tone analysis is: {tone_score}')
            else: 
                st.write("ERROR: No video found, please select a video and try again!")