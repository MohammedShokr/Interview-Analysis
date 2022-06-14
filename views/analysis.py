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
from Queries import *
def load_view(comp_id):
    FER_score = 0
    tone_score = 0
    fluency_score = 0
    coherence_score = 0
    overall_score = 0
    fer_weight = 0
    tone_weight = 0
    fluency_weight = 0
    coherence_weight = 0
    FER_matrix = {}
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
from Queries import *
def load_view(comp_id):
    FER_score = 0
    tone_score = 0
    fluency_score = 0
    coherence_score = 0
    overall_score = 0
    fer_weight = 0
    tone_weight = 0
    fluency_weight = 0
    coherence_weight = 0
    FER_matrix = {}
    tone_matrix = {}
    fluency_matrix = {}

    ############################## Sidebar ###################################
    with st.sidebar:
        st.title("Analysis")
        # Choose the models to be involved in the analysis
        selections = st.multiselect('Select what you want to analyze', ["Facial Analysis", 
                                                                        "Tone Analysis",
                                                                        "English Topic Coherence",
                                                                        "English Fluency Analysis"])
        # If more than one model is selected; add slider to choose weight for each model
        if len(selections)>1:
            if "Facial Analysis" in selections:
                fer_weight = st.slider('FER weight', 0, 100, 50)
            if "Tone Analysis" in selections:
                tone_weight = st.slider('Tone analysis weight', 0, 100, 50)
            if "Tone Analysis" in selections:
                tone_weight = st.slider('Tone analysis weight', 0, 100, 50)
            if "English Fluency Analysis" in selections:
                fluency_weight = st.slider('Fluency analysis weight', 0, 100, 50)
            if "English Topic Coherence" in selections:
                coherence_weight = st.slider('English coherence weight', 0, 100, 50)
        reportBx = st.checkbox("Generate detailed report")  # Option to generate a report with more details
        addAnalysisBx = st.checkbox("Add Analysis results to database") # Option to store the analysis to the database

    ######################## Adding metadata to the database ######################
    _, center,_ = st.columns((1,3,1))
    center.title("Interview Analysis Page")

    if addAnalysisBx:
        st.header("Interview-related Data")
        curr_cand_id = st.text_input("Ender your candidate National ID", "1", max_chars = 14) # Get the ID of the candidate
        curr_cand_data = get_cand(curr_cand_id)
        if not curr_cand_data:
            # If the ID doesn't exist allow the user to sign up this candidate
            st.error('A candidate of this ID is not in the database')
            # Adding a new candidate
            with st.expander("Add a new candidate"):
                add_cand_form = st.form(key='add_candidate')
                cand_name = add_cand_form.text_input("Enter Candidate's name") # Get the candidate's name
                cand_id = add_cand_form.text_input("Ender candidate National ID", max_chars = 14) # Get the candidate's ID
                cand_qualifications = add_cand_form.text_input("Enter candidate's qualification") # Get the candidate's qualifications
                add_cand_btn = add_cand_form.form_submit_button('Add Candidate')
            if add_cand_btn:
                try:
                    # When the "Add candidate" button is pressed; add the candidate to the database 
                    add_candidate(cand_id, cand_name, cand_qualifications)
                    st.success('The candidate added successfuly to the database')

                except:
                    # If the ID exists show an error message
                    st.error('This data cannot be inserted. Already an ID')
                # Show all candidates in a dataframe
                with st.expander("View All Candidates "):
                    result = view_candidate_data()
                    cand_df = pd.DataFrame(result,columns=["ID","Name","Qualification"])
                    st.dataframe(cand_df)

        col_11, col_12 = st.columns(2)
        # Getting the metadata about the question
        with st.form('add_analysis_metadata'):
            available_jobs = [job[0] for job in get_jobs_comp(comp_id)] # Get all jobs of the company
            job_title = col_11.selectbox("Choose job for analysis", available_jobs) # Ask the user to select one job
            ques_number = col_11.number_input('Question No.', 1, 50) # Getting the question number
            interview_number = col_12.number_input('Interview No.', 1, 10)  # Getting the interview number

    ############################# Uploading the playing the video #######################################
    st.header("Upload A Video to Analyze🥳")
    uploaded_file = st.file_uploader("Choose a file", type=['mp4','webm']) # Uploading video from local disk
    if uploaded_file is not None:
        st.video(uploaded_file) # Display the video
        g = io.BytesIO(uploaded_file.read())  # Convert the video to BytesIO Object
        video_path = "./test_interviews/testout_simple.mp4"
        with open(video_path, 'wb') as out:  # Open temporary file as bytes
            out.write(g.read())  # Read bytes and put them into the file

    ############################## Analyze the question's video ############################################
    col1, col2, col3 = st.columns([5,4,3])
    with col2:
        analyzeBtn = st.button('Analyze')
    if analyzeBtn:
        if uploaded_file:
            frames_flag = 0
            # Check the selected models to run them
            # FER
            if "Facial Analysis" in selections:
                st.header("FER")
                with st.spinner("Facial expressions are being analyzed"):
                    # Call the analyze face function on the video
                    FER_score, FER_matrix, FER_weights, total_frames = analyze_face(video_path)

                # Check if less than 75% of the frames are without a face 
                frames_flag = (len(FER_matrix.keys()))/(total_frames//10) < 0.75

                # Display the FER score
                st.write(f'The score based on face expression analysis is: {FER_score} %')
                st.progress(FER_score/100)
                overall_score = FER_score # Set the overall score to the FER score if it is the only selected model

            if ("Tone Analysis" in selections) or ("English Topic Coherence" in selections) or ("English Fluency Analysis" in selections):
                # Convert the video to audio for all models other than the FER model
                audio_path = convert_video_to_audio(video_path)    

            # Tone Analysis
            if "Tone Analysis" in selections:
                st.header("Tone")
                with st.spinner("Tone expressions are being analyzed"):
                    # Call the analyze tone function on the audio
                    tone_score, tone_matrix, tone_weights, silence = analyze_tone(audio_path)
                # Display the tone score
                st.write(f'The score based on tone analysis is: {tone_score} %')
                st.progress(tone_score/100)
                overall_score = tone_score # Set the overall score to the tone score if it is the only selected model
                if silence >= 50:
                    # Show warning if the candidate was silent >50% of the time
                    st.warning(f'The interviewee was silent >= 50% of the time, Actual Percentage:{silence}%')

            # English Fluency    
            if "English Fluency Analysis" in selections:
                st.header("Fluency")
                with st.spinner("English Fluency is being analyzed"):
                    # Call the analyze fluency function on the audio
                    fluency_score, fluency_matrix, fluency_weights = analyze_fluency(audio_path)
                # Display the fluency score
                fluency_score = round(fluency_score,2)
                st.write(f'The score based on fluency analysis is: {fluency_score} %')
                st.progress(fluency_score/100)
                overall_score = fluency_score # Set the overall score to the fluency score if it is the only selected model

            # English Topic Coherence
            if "English Topic Coherence" in selections:
                st.header("English")
                with st.spinner("English coherence is being assessed"):
                    # Convert the audio to text
                    text = short_speech_to_text(audio_path)
                    # Call the coherence scoring function on the text
                    coherence_score = coherence_scoring(text)
                # Display the coherence score
                st.write(f'The Coherence percentage of English text: {round(coherence_score*100,2)}%')
                st.progress(coherence_score)
                overall_score = coherence_score*100 # Set the overall score to the coherence score if it is the only selected model

            # If more than one model is selected; calculate the overall score
            if len(selections)>1:
                # Calculate the overall score as a weighted average of the scores
                overall_score = ((0.01*fer_weight*FER_score)+(0.01*tone_weight*tone_score)+(0.01*fluency_weight*fluency_score)+(coherence_weight*coherence_score))/(0.01*fer_weight+0.01*tone_weight+0.01*coherence_weight)
                # Display the overall score
                st.header("Overall score")
                st.write(f'{round(overall_score,2)}%')
                st.progress(overall_score/100)

        ####################### Adding the analysis to the database #################################
            if addAnalysisBx:
                if curr_cand_data:
                    cand_id = curr_cand_id

                # If an analysis with the same data exists; update it with the new data
                if len(get_one_analysis(comp_id, job_title, cand_id, interview_number, ques_number)):
                    delete_one_analysis(comp_id, job_title, cand_id, interview_number, ques_number)
                    st.info("This analysis entry has been updated in the database")
                else:
                    st.info("This analysis enty has been added to the database")
                # Add analysis with the current data to the database
                add_analysis(cand_id, comp_id, job_title, interview_number, ques_number, str(FER_matrix),\
                    FER_score, str(tone_matrix), tone_score, str(fluency_matrix), fluency_score,\
                    coherence_score, overall_score)
                if frames_flag:
                    # If the face was't detected on >75% of the frames don't store the result and show a warning
                    st.warning('''WARNING: The results were added to the database.
                               The interviewee's  face was not detected most of the time''')
                    col4, col5, col6 = st.columns([5,4,3])
                    if col5.button("Delete Analysis"):
                        st.write(job_title)
                        delete_one_analysis(comp_id, job_title, cand_id, interview_number, ques_number)
            else:
                if frames_flag:
                    st.warning('''WARNING: The interviewee's  face was not detected most of the time''')

        else:
            st.write("ERROR: No video found, please select a video and try again!")

        ############################### Generate a detailed report ###################################
        if reportBx:
            try:
                with st.expander("More analysis details"):
                    
                    # For a single analysis video 
                    with st.container():
                        with st.container():
                            st.subheader("Achieved Scores")
                            _, col_ind4, col_ind5, col_ind6, col_ind7, _ = st.columns((1,4,4,4,4,1))
                            # FER score
                            if 'Facial Analysis' in selections:
                                col_ind4.metric("Facial Expression Analysis", f'{FER_score} %')
                            else:
                                col_ind4.metric("Facial Expression Analysis", '-')
                            # tone score
                            if 'Tone Analysis' in selections:
                                col_ind5.metric("Tone Analysis", f'{tone_score} %')
                            else:
                                col_ind5.metric("Tone Analysis", '-')
                            # fluency score
                            if 'English Fluency Analysis' in selections:
                                col_ind6.metric("English Fluency Analysis", f'{fluency_score} %')
                            else:
                                col_ind6.metric("English Fluency Analysis", '-')
                            # coherence score
                            if 'English Topic Coherence' in selections:
                                col_ind7.metric("Topic Coherence Analysis", f'{round(100*coherence_score,2)} %')
                            else:
                                col_ind7.metric("Topic Coherence Analysis", '-')
                        #######
                        FER_matrix = list(FER_matrix.values())
                        tone_matrix = list(tone_matrix.values())
                        fluency_matrix = list(fluency_matrix.values())
                        with st.container():
                            try:
                                dummy = len(FER_weights)
                                st.subheader("FER: average score details")
                                progressbar_FER_weights(FER_weights)
                                st.subheader("FER: score details for each second")
                                FER_matrix = (np.array(FER_matrix)*100).round(decimals=0).astype(int)
                                FER_np = np.array(list(FER_matrix))
                                indx = []
                                for i in range(1, len(FER_np)+1):
                                    indx.append([i])
                                indx = np.array(indx)
                                FER_np = np.append(indx, FER_np, axis=1)
                                # st.write(np.array(list(FER_matrix)))
                                # st.write(FER_np)
                                _, colmat, _ = st.columns((2, 4, 2))
                                df = pd.DataFrame(
                                    FER_np,
                                    columns=(['time index(sec)','angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']))
                                colmat.dataframe(df)
                                colmat.text("")
                                colmat.text("")
                            except:
                                pass
                    #########################################################
                    with st.container():
                        try:
                            dummy = len(tone_weights)
                            st.subheader("Tone: average score details")
                            progressbar_tone_weights(tone_weights)
                            st.subheader("Tone: score details for each 5-seconds")
                            tone_matrix = (np.array(tone_matrix)*100).round(decimals=0).astype(int)
                            tone_np = np.array(list(tone_matrix))
                            indx = []
                            for i in range(1, len(tone_np)+1):
                                indx.append([i])
                            indx = np.array(indx)
                            tone_np = np.append(indx, tone_np, axis=1)
                            _, colmat, _ = st.columns((2, 4, 2))
                            df = pd.DataFrame(
                                tone_np,
                                columns=(['5-sec number', 'Angry', 'Fear', 'Happy', 'Sad', 'surprise']))
                            colmat.dataframe(df)
                            colmat.text("")
                            colmat.text("")
                        except:
                            pass
                    with st.container():
                        try:
                            dummy = len(fluency_weights)
                            st.subheader("Fluency: average score details")
                            progressbar_fluency_weights(fluency_weights)
                            st.subheader("Fluency: score details for each 5-seconds")
                            fluency_matrix = (np.array(fluency_matrix)*100).round(decimals=0).astype(int)
                            fluency_np = np.array(list(fluency_matrix))
                            indx = []
                            for i in range(1, len(fluency_np)+1):
                                indx.append([i])
                            indx = np.array(indx)
                            fluency_np = np.append(indx, fluency_np, axis=1)
                            _, colmat, _ = st.columns((2, 4, 2))
                            df = pd.DataFrame(
                                fluency_np,
                                columns=(['5-sec number', 'Not Fluent', 'Average', 'Fluent']))
                            colmat.dataframe(df)
                            colmat.text("")
                            colmat.text("")
                        except:
                            pass
            except:
                pass