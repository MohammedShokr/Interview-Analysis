import streamlit as st
from FER import analyze_face
from tone import analyze_tone

def load_view():
    with st.sidebar:
        st.title("Analysis")
        selections = st.multiselect('Select what you want to analyze', ["Facial Analysis", "Tone Analysis", "English Text Coherence"], ["Facial Analysis", "Tone Analysis"])
    uploaded_file = st.file_uploader("Choose a file")
    ques_number = st.number_input('Question No.', 0, 10)
    st.video(uploaded_file)
    
    col1, col2, col3 = st.columns([5,4,3])
    with col2:
        analyzeBtn = st.button('Analyze')
        if analyzeBtn:
            if uploaded_file:
                if "Facial Analysis" in selections:
                    with st.spinner("Facial expressions are being analyzed"):
                        FER_score, FER_weights = analyze_face("./test_interviews/"+uploaded_file.name)
                    st.write(f'The score based on face expression analysis is: {FER_score}')
                    with col3:
                        st.write(f'angry: {round(FER_weights[0],2)}%')
                        st.progress(FER_weights[0])
                        st.write(f'disgust: {round(FER_weights[1],2)}%')
                        st.progress(FER_weights[1])
                        st.write(f'fear: {round(FER_weights[2],2)}%')
                        st.progress(FER_weights[2])
                        st.write(f'happy: {round(FER_weights[3],2)}%')
                        st.progress(FER_weights[3])
                        st.write(f'neutral: {round(FER_weights[4],2)}%')
                        st.progress(FER_weights[4])
                        st.write(f'sad: {round(FER_weights[5],2)}%')
                        st.progress(FER_weights[5])
                        st.write(f'surprise: {round(FER_weights[6],2)}%')
                        st.progress(FER_weights[6])
                if "Tone Analysis" in selections:
                    with st.spinner("Tone expressions are being analyzed"):
                        tone_score, tone_weights = analyze_tone("./test_interviews/"+uploaded_file.name)
                    st.write(f'The score based on tone analysis is: {tone_score}')
                if "English Text Coherence" in selections:
                    st.write("⏳Analysis of English is being implemented")
                
            else:
                st.write("ERROR: No video found, please select a video and try again!")