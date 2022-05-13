from matplotlib.style import available
import streamlit as st
import pandas as pd
import numpy as np
import io
from FER import analyze_face
from tone import analyze_tone
from fluency_analysis import analyze_fluency
from database_functions import *
from audio_processing import convert_video_to_audio
from coherence_assessment import coherence_scoring
from speech_to_text import short_speech_to_text
def load_view(comp_id):
    FER_score = 0
    tone_score = 0
    fluency_score = 0
    coherence_score = 0
    overall_score = 0
    fer_weight = 0
    tone_weight = 0
    fluency_weight =0
    coherence_weight = 0
    FER_matrix = {}
    tone_matrix = {}
    fluency_matrix = {}
    
    
    with st.sidebar:
        st.title("Analysis")
        selections = st.multiselect('Select what you want to analyze', ["Facial Analysis", "Tone Analysis", "English Text Coherence", "English Fluency Analysis"])
        if len(selections)>1:
            if "Facial Analysis" in selections:
                fer_weight = st.slider('FER weight', 0, 100, 50)
            if "Tone Analysis" in selections:
                tone_weight = st.slider('Tone analysis weight', 0, 100, 50)
            if "English Fluency Analysis" in selections:
                fluency_weight = st.slider('Fluency analysis weight', 0, 100, 50)
            if "English Text Coherence" in selections:
                coherence_weight = st.slider('English coherence weight', 0, 100, 50)
        reportBx = st.checkbox("Generate detailed report")
        addAnalysisBx = st.checkbox("Add Analysis results to database")
    
    ######################## Database Management ############################
    curr_cand_id = st.text_input("Ender your candidate National ID", "1")
    curr_cand_data = get_cand(curr_cand_id)
    if not curr_cand_data:
        st.error('A candidate of this ID is not in the database')
        with st.expander("Add a new candidate"):
            add_cand_form = st.form(key='add_candidate')
            cand_name = add_cand_form.text_input("Enter Candidate's name")
            cand_id = add_cand_form.text_input("Ender candidate National ID")
            cand_qualifications = add_cand_form.text_input("Enter candidate's qualification")
            add_cand_btn = add_cand_form.form_submit_button('Add Candidate')
        if add_cand_btn:
            try:
                add_candidate(cand_id, cand_name, cand_qualifications)
                st.success('The candidate added successfuly to the database')
   
            except:
                st.error('This data cannot be inserted. Already an ID')
            with st.expander("View All Candidates "):
                result = view_candidate_data()
                # st.write(result)
                cand_df = pd.DataFrame(result,columns=["ID","Name","Qualification"])
                st.dataframe(cand_df)
    
    col_11, col_12 = st.columns(2)           
    with st.form('add_analysis'):
        available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
        
        job_title = col_11.selectbox("Choose job for analysis", available_jobs)
        ques_number = col_11.number_input('Question No.', 1, 50)   
        interview_number = col_12.number_input('Interview No.', 1, 10)
    #################################################################################################
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.video(uploaded_file)
        g = io.BytesIO(uploaded_file.read())  ## BytesIO Object
        video_path = "./test_interviews/testout_simple.mp4"
        
        with open(video_path, 'wb') as out:  ## Open temporary file as bytes
            out.write(g.read())  ## Read bytes and put it into the file

    ########################################################################################################
    col1, col2, col3 = st.columns([5,4,3])
    with col2:
        analyzeBtn = st.button('Analyze')
    if analyzeBtn:
        if uploaded_file:
            if "Tone Analysis" or "English Text Coherence" or "English Fluency Analysis"in selections:
                audio_path = convert_video_to_audio(video_path)
            if "Facial Analysis" in selections:
                st.header("FER")
                with st.spinner("Facial expressions are being analyzed"):
                    FER_score, FER_matrix, FER_weights = analyze_face(video_path)
                st.write(f'The score based on face expression analysis is: {FER_score}')
                st.progress(FER_score/100)
                overall_score = FER_score
                
            if "Tone Analysis" in selections:
                st.header("Tone")
                with st.spinner("Tone expressions are being analyzed"):
                    tone_score, tone_matrix, tone_weights = analyze_tone(audio_path)
                st.write(f'The score based on tone analysis is: {tone_score}')
                st.progress(tone_score/100)
                overall_score = tone_score
                
            if "English Fluency Analysis" in selections:
                st.header("Fluency")
                with st.spinner("English Fluency is being analyzed"):
                    fluency_score, fluency_matrix, fluency_weights = analyze_fluency(audio_path)
                st.write(f'The score based on fluency analysis is: {fluency_score}')
                st.progress(fluency_score/100)
                overall_score = fluency_score

            if "English Text Coherence" in selections:
                st.header("English")
                with st.spinner("English coherence is being assessed"):
                    text = short_speech_to_text(audio_path)
                    coherence_score = coherence_scoring(text)
                    st.write(f'The Coherence percentage of English text: {round(coherence_score*100,2)}%')
                    st.progress(coherence_score)
                    overall_score = coherence_score*100
            if len(selections)>1:
                overall_score = ((0.01*fer_weight*FER_score)+(0.01*tone_weight*tone_score)+\
                    (0.01*fluency_weight*fluency_score)+(coherence_weight*coherence_score))/\
                    (0.01*fer_weight+0.01*tone_weight+0.01*fluency_weight+0.01*coherence_weight)
                st.header("Overall score")
                st.write(f'{round(overall_score,2)}%')
                st.progress(overall_score/100)
            
            if addAnalysisBx:
                if curr_cand_data:
                    cand_id = curr_cand_id
                if get_one_analysis(comp_id, job_title, cand_id, interview_number, ques_number):
                    update_analysis(cand_id, comp_id, job_title, interview_number, ques_number, str(FER_matrix),\
                        FER_score, str(tone_matrix), tone_score, str(fluency_matrix), fluency_score,\
                        coherence_score, overall_score)
                    st.info("This analysis entry has been updated in the database")
                else:
                    st.info("This analysis entry has been added to the database")
                    add_analysis(cand_id, comp_id, job_title, interview_number, ques_number, str(FER_matrix),\
                        FER_score, str(tone_matrix), tone_score, str(fluency_matrix), fluency_score,\
                        coherence_score, overall_score)
                    
        else:
            st.write("ERROR: No video found, please select a video and try again!")

    if reportBx:
        try:
            with st.expander("Show a report"):
                st.header("Average scores of expressions")
                st.write(f'angry: {round(100*FER_weights[0],2)}%')
                st.progress(float(FER_weights[0]))
                st.write(f'disgust: {round(100*FER_weights[1],2)}%')
                st.progress(float(FER_weights[1]))
                st.write(f'fear: {round(100*FER_weights[2],2)}%')
                st.progress(float(FER_weights[2]))
                st.write(f'happy: {round(100*FER_weights[3],2)}%')
                st.progress(float(FER_weights[3]))
                st.write(f'neutral: {round(100*FER_weights[4],2)}%')
                st.progress(float(FER_weights[4]))
                st.write(f'sad: {round(100*FER_weights[5],2)}%')
                st.progress(float(FER_weights[5]))
                st.write(f'surprise: {round(100*FER_weights[6],2)}%')
                st.progress(float(FER_weights[6]))

                st.header("Detailed report")
                df = pd.DataFrame(
                np.array(list(FER_matrix.values())),
                columns=(['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']))
                st.dataframe(100*df)

        except:
            st.info("Report will be shown after analysis")
    
    
    
