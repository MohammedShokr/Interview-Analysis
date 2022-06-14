import streamlit as st
import pandas as pd
import seaborn as sns
from Queries import *
import matplotlib.pyplot as plt
import numpy as np 

# Get the top candidates in a certain job
## Define colors
dark_blue = '#112B3C'
second_blue_bg = '#205375'
orange = '#F66B0E'
orange_bar = '#fc8121'
white = '#FFFFFF'
dull_white = '#C8C6C6'
# ### css ###
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def load_view(comp_id):
    ### CSS
    local_css("styles_reports.css")
    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
    metrics = ["overall_score", "FER_score", "tone_score", "fluency_score", "coherence_score"]
    jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]
    analysis_cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]

    rc = {'figure.figsize':(8, 4.5),
          'axes.facecolor': second_blue_bg,
          'axes.edgecolor': dark_blue,
          'axes.labelcolor': white,
          'figure.facecolor': second_blue_bg,
          'patch.edgecolor': orange,
          'text.color': white,
          'xtick.color': white,
          'ytick.color': white,
          'grid.color': white,
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    col1_spacer1, col1, col1_spacer2 = st.columns((.2, 7.1, .2))
    with col1:
        st.subheader('Top 10 candidates in a Job')
    with st.container():
        col2_spacer1, col2_1, col2_spacer2, col2_2, col2_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with col2_1:
            st.markdown('More details can be witten here')
            job_title_top = st.selectbox("Choose a job", available_jobs)
            metric_top = st.selectbox("Choose metric used for comparison", metrics)

        with col2_2:
            st.text("")
            st.text("")
            top_cands_df = get_top_cands_job(comp_id, job_title_top, metric_top)
            # st.dataframe(top_cands_df)
            ##########
            fig1 = plt.figure()
            ax = fig1.add_axes([0, 0, 1, 1])

            names = top_cands_df['cand_ID'].tolist()
            scores = top_cands_df[metric_top].tolist()
            ax.bar(names, scores, color=orange_bar)
            plt.xlabel(f'candidate ID')
            plt.ylabel(f'metric: {metric_top}')
            plt.title(f'Candidates sorted by {metric_top}')
            st.pyplot(fig1)
            st.text("")
            st.text("")
            ##########
            # st.bar_chart(top_cands_df[metric])

    col3_spacer1, col3, col3_spacer2 = st.columns((.2, 7.1, .2))
    with col3:
        st.subheader('Compare between two candidates')
    with st.container():
        col4_spacer1, col4_1, col4_spacer2, col4_2, col4_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with col4_1:
            st.text("")
            st.text("")
            job_title_compare = st.selectbox("Choose job", available_jobs)
            metric_compare = st.selectbox("Comparison metric", metrics)
            cand1 = st.text_input("First candidate's National ID", max_chars = 14)
            cand1_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, cand1), columns=analysis_cols)
            if cand1:
                if cand1_analysis_df.empty:
                    col4_2.info("The first candidate does not have any analysis results")
            cand1_interviews = cand1_analysis_df[cand1_analysis_df["job_title"]==job_title_compare]["interview_no"]
            intv1 = st.selectbox("Select an Interview for the first candidate", cand1_interviews.unique())
            cand2 = st.text_input("Second candidate's National ID", max_chars = 14)
            cand2_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, cand2), columns=analysis_cols)
            if cand2:
                if cand2_analysis_df.empty:
                    col4_2.info("The second candidate does not have any analysis results")
            cand2_interviews = cand2_analysis_df[cand2_analysis_df["job_title"]==job_title_compare]["interview_no"]
            intv2 = st.selectbox("Select an Interview for the second candidate", cand2_interviews.unique())
        with col4_2:
            if intv1: intv1 = int(intv1)
            if intv2: intv2 = int(intv2)
            cand1_df, cand2_df = compare_two_cands(comp_id, job_title_compare, cand1, cand2, intv1, intv2, metric_compare)
            # st.dataframe(cand1_df)
            # st.dataframe(cand2_df)
            fig2 = plt.figure()
            c1_qn = cand1_df[cand1_df.columns[0]].tolist()
            c1_scores = cand1_df[cand1_df.columns[1]].tolist()

            c2_qn = cand2_df[cand2_df.columns[0]].tolist()
            c2_scores = cand2_df[cand2_df.columns[1]].tolist()

            # plot lines
            plt.plot(c1_qn, c1_scores,  marker='o',label=cand1, color=dull_white)
            plt.plot(c2_qn, c2_scores, marker='o', label=cand2, color=orange_bar)
            plt.xlabel(f'Question Number')
            plt.ylabel(f'scores')
            plt.title(f'Candidates Scores over questions')
            plt.legend()
            st.text("")
            st.text("")
            st.pyplot(fig2)
            st.text("")
            st.text("")
            ##########

    # # ### TO DOWNLOAD
    # with st.expander("View all analysis details of candidates"):
    #     analysis_df = pd.DataFrame(get_analysis_comp(comp_id), columns=analysis_cols)
    #     st.dataframe(analysis_df)
    #
    # ####### EDIT HERE ####
    # # ### TO DOWNLOAD
    # col5_spacer1, col5, col5_spacer2 = st.columns((.2, 7.1, .2))
    # with col5:
    #     st.subheader('Show all analysis details of a Job')
    # col6_spacer1, col6_1, col6_spacer2, col6_2, col6_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    # with col6_1:
    #     job_title_analysis = st.selectbox("Choose job for analysis", available_jobs)
    # with col6_2:
    #     analysis_in_job_df = pd.DataFrame(get_analysis_with_job(comp_id, job_title_analysis), columns=analysis_cols)
    #     st.dataframe(analysis_in_job_df)
        
    # col7_spacer1, col7, col7_spacer2 = st.columns((.2, 7.1, .2))
    # with col7:
    #     st.subheader('Show all analysis details of a Candidate')
    # col8_spacer1, col8_1, col8_spacer2, col8_2, col8_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    # with col8_1:
    #     candindate_id = st.text_input("Write Candidate National ID")
    # with col8_2:
    #     analysis_candidate_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_id), columns=analysis_cols)
    #     st.dataframe(analysis_candidate_df[analysis_cols[2:]])

    ####### END EDIT HERE ####
    with st.expander("Individual Report"):
        col1, col2 = st.columns((2, 7))
        with col1:
            candindate_ID = st.text_input("Write the Candidate's National ID", max_chars = 14)
        if candindate_ID:
            cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID), columns=analysis_cols)
            if cand_analysis_df.empty:
                st.info("The entered candidate ID doesn't have any analysis recored")
            else:
                st.subheader("General Insights")
                # col1, col2, col3 = st.columns((2, 6, 2))
                with st.container():
                    # with col2:
                    _, col_ind1, col_ind2, col_ind3, _ = st.columns(5)
                    # No. of jobs applied for
                    jobs_num = cand_analysis_df["job_title"].nunique()
                    col_ind1.metric("Applied for", f'{jobs_num} Jobs')

                    # No. of interviews he has done
                    interviews_num = cand_analysis_df.groupby(["job_title", "interview_no"]).size().count()
                    col_ind2.metric("Interviewd", f'{interviews_num}')

                    # Average overall score in all interviews
                    avg_overall_score_df = cand_analysis_df[["job_title", "interview_no", "overall_score"]]\
                                    .groupby(["job_title", "interview_no"]).mean()

                    if not cand_analysis_df.empty:
                        avg_overall = round(avg_overall_score_df['overall_score'].mean(),2)
                        col_ind3.metric("Acheived Average Overall Score", f'{avg_overall} %')

                    st.subheader("Highest Achieved Scores")
                    _, col_ind4, col_ind5, col_ind6, col_ind7, _ = st.columns((1,4,4,4,4,1))
                    if not cand_analysis_df.empty:
                        # Best FER score
                        best_fer_score = cand_analysis_df[["job_title", "interview_no", "FER_score"]]\
                                        .groupby(["job_title", "interview_no"]).max()["FER_score"][0]
                        col_ind4.metric("Facial Expression Analysis", f'{best_fer_score} %')
                        # Best tone score
                        best_tone_score = cand_analysis_df[["job_title", "interview_no", "tone_score"]]\
                                        .groupby(["job_title", "interview_no"]).max()["tone_score"][0]
                        col_ind5.metric("Tone Analysis", f'{best_tone_score} %')
                        # Best fluency score
                        best_fluency_score = cand_analysis_df[["job_title", "interview_no", "fluency_score"]]\
                                        .groupby(["job_title", "interview_no"]).max()["fluency_score"][0]
                        col_ind6.metric("English Fluency Analysis", f'{best_fluency_score} %')
                        # Best coherence score
                        best_coherence_score = cand_analysis_df[["job_title", "interview_no", "coherence_score"]]\
                                        .groupby(["job_title", "interview_no"]).max()["coherence_score"][0]
                        col_ind7.metric("Topic Coherence Analysis", f'{round(100*best_coherence_score,2)} %')
                
                col5_spacer1, col5, col5_spacer2 = st.columns((2, 6, 2))
                with col5:
                    st.subheader('Interview Details')
                with st.container():
                    with col5:
                        cand_jobs = cand_analysis_df["job_title"].unique()
                        cand_job_title = st.selectbox("Choose a Job title", cand_jobs)
                        cand_interviews = cand_analysis_df[cand_analysis_df["job_title"]==cand_job_title]["interview_no"]
                        cand_interview_no = st.selectbox("Select an Interview", cand_interviews.unique())
                        cand_questions = cand_analysis_df[(cand_analysis_df["job_title"]==cand_job_title) &\
                                        (cand_analysis_df["interview_no"]==cand_interview_no)]["question_no"]
                    
                    if cand_interview_no: cand_interview_no = int(cand_interview_no)
                    cand_interview_df = pd.DataFrame(get_analysis_with_job_cand(comp_id, cand_job_title, candindate_ID, cand_interview_no), columns=analysis_cols)
                with st.container():
                
                    _, col_ind12, col_ind13, _ = st.columns(4)
                    if not cand_interview_df.empty:
                        questions_num = len(list(cand_questions))
                        col_ind12.metric("Number of Questions", questions_num)
                        overall_score = cand_interview_df['overall_score'].mean()
                        col_ind13.metric("Overall Score", f'{round(overall_score, 2)} %')
                        
                    col11_spacer1, col11, col11_spacer2 = st.columns((2, 6, 2))
                    col11.markdown(candidate_evaluation(overall_score))
                    
                    _, col_ind8, col_ind9, col_ind10, col_ind11, _ = st.columns((1,4,4,4,4,1))
                    if not cand_interview_df.empty:
                        # Best FER score
                        fer_score = cand_interview_df['FER_score'].mean()
                        col_ind8.metric("Facial Expression Analysis", f'{round(fer_score,2)} %')
                        # Best tone score
                        tone_score = cand_interview_df['tone_score'].mean()
                        col_ind9.metric("Tone Analysis", f'{round(tone_score,2)} %')
                        # Best fluency score
                        fluency_score = cand_interview_df['fluency_score'].mean()
                        col_ind10.metric("English Fluency Analysis", f'{round(fluency_score,2)} %')
                        # Best coherence score
                        coherence_score = cand_interview_df['coherence_score'].mean()
                        col_ind11.metric("Topic Coherence Analysis", f'{round(100*coherence_score,2)} %')
                #For a single analysis video
                col9_spacer1, col9, col9_spacer2 = st.columns((2, 6, 2))
                with col9:
                    st.subheader('More analysis details')
                with st.container():
                    with col9:
                        with st.container():
                            ques_no = st.selectbox("Select Question no.", list(cand_questions))
                    ########
                    with st.container():
                        cand_analysis = pd.DataFrame(get_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no), columns=analysis_cols)

                        st.subheader("Achieved Scores")
                        _, col_ind4, col_ind5, col_ind6, col_ind7, _ = st.columns((1,4,4,4,4,1))
                        if not cand_analysis_df.empty:
                            # Best FER score
                            fer_score = cand_analysis['FER_score'][0]
                            col_ind4.metric("Facial Expression Analysis", f'{fer_score} %')
                            # Best tone score
                            tone_score = cand_analysis['tone_score'][0]
                            col_ind5.metric("Tone Analysis", f'{tone_score} %')
                            # Best fluency score
                            fluency_score = cand_analysis['fluency_score'][0]
                            col_ind6.metric("English Fluency Analysis", f'{fluency_score} %')
                            # Best coherence score
                            coherence_score = cand_analysis['coherence_score'][0]
                            col_ind7.metric("Topic Coherence Analysis", f'{round(100*coherence_score,2)} %')
                    #######
                    if cand_interview_no: cand_interview_no = int(cand_interview_no)
                    cand_analysis = pd.DataFrame(get_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no), columns=analysis_cols)

                    if not cand_analysis.empty:
                        FER_matrix = list(eval(cand_analysis["FER"][0]).values())
                        tone_matrix = list(eval(cand_analysis["tone"][0]).values())
                        fluency_matrix = list(eval(cand_analysis["fluency"][0]).values())

                        FER_weights = np.mean(np.array(FER_matrix), axis=0)
                        tone_weights = np.mean(np.array(tone_matrix), axis=0)
                        fluency_weights = np.mean(np.array(fluency_matrix), axis=0)
                        # st.write(FER_matrix[0:5])
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
                                st.info("No FER data")

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
                                st.info("No tone data")

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
                                st.info("No fluency data")

# ### TO DOWNLOAD
    with st.expander("Download all analysis details of a Job"):
        col5_spacer1, col5, col5_spacer2 = st.columns((.2, 7.1, .2))
        # with col5:
        #     st.subheader('Download all analysis details of a Job')
        col6_spacer1, col6_1, col6_spacer2, col6_2, col6_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with col6_1:
            job_title_analysis = st.selectbox("Choose job for analysis", available_jobs)
        with col6_2:
            analysis_in_job_df = pd.DataFrame(get_analysis_with_job(comp_id, job_title_analysis), columns=analysis_cols)
            st.dataframe(analysis_in_job_df)
        col7_spacer1, col7, col7_spacer2 = st.columns((4, 2, 4))
        with col7:
            st.download_button("DOWNLOAD", analysis_in_job_df.to_csv(), file_name=f'all_job_{job_title_analysis}_analysis.csv')


    with st.expander("Download all analysis details of a Candidate"):

        col8_spacer1, col8_1, col8_spacer2, col8_2, col8_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with col8_1:
            candindate_id = st.text_input("Write Candidate National ID", max_chars = 14)
        with col8_2:
            analysis_candidate_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_id), columns=analysis_cols)
            st.dataframe(analysis_candidate_df[analysis_cols[2:]])
        col7_spacer1, col7, col7_spacer2 = st.columns((4, 2, 4))
        with col7:
            st.download_button("DOWNLOAD", analysis_candidate_df.to_csv(), file_name=f'all_cand_{candindate_id}_analysis.csv')


