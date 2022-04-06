import streamlit as st
from FER import analyze_face
from tone import analyze_tone

st.set_page_config(page_title="Video Interview Analysis")
uploaded_file = st.file_uploader("Choose a file")
st.video(uploaded_file)
analyzeBtn = st.button('Analyze')
if analyzeBtn:
    Score = analyze_face(uploaded_file.name)
    st.write('The score based on face expression analysis is: ')
    st.write(Score)
reportsBtn = st.button('Generate Button')
if reportsBtn:
    tone_predicted = analyze_tone(uploaded_file.name)
    st.write(tone_predicted)
