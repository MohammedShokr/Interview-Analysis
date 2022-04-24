import streamlit as st
from FER import analyze_face
from tone import analyze_tone
from audio_processing import convert_video_to_audio
from coherence_assessment import coherence_scoring
from speech_to_text import short_speech_to_text
def load_view():
    FER_score = 0
    tone_score = 0
    coherence_score = 0
    fer_weight = 0
    tone_weight = 0
    coherence_weight = 0
    with st.sidebar:
        st.title("Analysis")
        selections = st.multiselect('Select what you want to analyze', ["Facial Analysis", "Tone Analysis", "English Text Coherence"])
        if len(selections)>1:
            if "Facial Analysis" in selections:
                fer_weight = st.slider('FER weight', 0, 100)
            if "Tone Analysis" in selections:
                tone_weight = st.slider('Tone analysis weight', 0, 100)
            if "English Text Coherence" in selections:
                coherence_weight = st.slider('English coherence weight', 0, 100)
        reportBx = st.checkbox("Generate detailed report")
    uploaded_file = st.file_uploader("Choose a file")
    #ques_number = st.number_input('Question No.', 0, 10)
    st.video(uploaded_file)
    
    col1, col2, col3 = st.columns([5,4,3])
    with col2:
        analyzeBtn = st.button('Analyze')
        if analyzeBtn:
            if uploaded_file:
                if "Facial Analysis" in selections:
                    st.header("FER")
                    with st.spinner("Facial expressions are being analyzed"):
                        FER_score, FER_weights = analyze_face("./test_interviews/"+uploaded_file.name)
                    st.write(f'The score based on face expression analysis is: {FER_score}')
                    st.progress(FER_score/10)
                    if reportBx:
                        with col3:
                            st.write(f'angry: {round(FER_weights[0],2)*100}%')
                            st.progress(FER_weights[0])
                            st.write(f'disgust: {round(100*FER_weights[1],2)}%')
                            st.progress(FER_weights[1])
                            st.write(f'fear: {round(100*FER_weights[2],2)}%')
                            st.progress(FER_weights[2])
                            st.write(f'happy: {round(100*FER_weights[3],2)}%')
                            st.progress(FER_weights[3])
                            st.write(f'neutral: {round(100*FER_weights[4],2)}%')
                            st.progress(FER_weights[4])
                            st.write(f'sad: {round(100*FER_weights[5],2)}%')
                            st.progress(FER_weights[5])
                            st.write(f'surprise: {round(100*FER_weights[6],2)}%')
                            st.progress(FER_weights[6])
                    
                if "Tone Analysis" in selections:
                    st.header("Tone")
                    with st.spinner("Tone expressions are being analyzed"):
                        tone_score, tone_weights = analyze_tone("./test_interviews/"+uploaded_file.name)
                    st.write(f'The score based on tone analysis is: {tone_score}')
                    st.progress(tone_score/10)

                if "English Text Coherence" in selections:
                    st.header("English")
                    with st.spinner("English coherence is being assessed"):
                        audio_path = convert_video_to_audio("./test_interviews/"+uploaded_file.name)
                        text = short_speech_to_text(audio_path)
                        coherence_score = coherence_scoring(text)
                        st.write(f'The Coherence percentage of English text: {round(coherence_score*100,2)}%')
                        st.progress(coherence_score)
                if len(selections)>1:
                    overall_score = ((0.1*fer_weight*FER_score)+(0.1*tone_weight*tone_score)+(coherence_weight*coherence_score))/(0.1*fer_weight+0.1*tone_weight+0.1*coherence_weight)
                    st.header("Overall score")
                    st.write(f'{round(overall_score,2)}%')
                    st.progress(overall_score/10)
            else:
                st.write("ERROR: No video found, please select a video and try again!")
