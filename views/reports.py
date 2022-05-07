import streamlit as st
import pandas as pd
import seaborn as sns
from Queries import *
import matplotlib.pyplot as plt
import numpy as np 

# Get the top candidates in a certain job

def load_view(comp_id):

    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
    metrics = ["overall_score", "FER_score", "tone_score", "fluency_score", "coherence_score"]
    jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]
    analysis_cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]
    
    
    col1_spacer1, col1, col1_spacer2 = st.columns((.2, 7.1, .2))
    with col1:
        st.subheader('Top 10 candidates in a Job')
    
    col2_spacer1, col2_1, col2_spacer2, col2_2, col2_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col2_1:
        st.markdown('More details can be witten here')
        job_title_top = st.selectbox("Choose a job", available_jobs) 
        metric_top = st.selectbox("Choose metric used for comparison", metrics)   

    with col2_2:
        top_cands_df = get_top_cands_job(comp_id, job_title_top, metric_top)
        st.dataframe(top_cands_df)
        ##########
        fig1 = plt.figure()
        ax = fig1.add_axes([0, 0, 1, 1])
        names = top_cands_df['cand_ID'].tolist()
        scores = top_cands_df[metric_top].tolist()
        ax.bar(names, scores)
        plt.xlabel(f'candidate ID')
        plt.ylabel(f'metric: {metric_top}')
        plt.title(f'Candidates sorted by {metric_top}')
        rc = {'figure.figsize':(8, 4.5),
              'axes.facecolor':'#0e1117',
              'axes.edgecolor': '#0e1117',
              'axes.labelcolor': 'white',
              'figure.facecolor': '#0e1117',
              'patch.edgecolor': '#0e1117',
              'text.color': 'white',
              'xtick.color': 'white',
              'ytick.color': 'white',
              'grid.color': 'grey',
              'font.size' : 12,
              'axes.labelsize': 12,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12}
        plt.rcParams.update(rc)
        st.pyplot(fig1)
        ##########
        # st.bar_chart(top_cands_df[metric])
        
    col3_spacer1, col3, col3_spacer2 = st.columns((.2, 7.1, .2))
    with col3:
        st.subheader('Compare between two candidates')
    col4_spacer1, col4_1, col4_spacer2, col4_2, col4_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col4_1:
        job_title_compare = st.selectbox("Choose job", available_jobs)
        metric_compare = st.selectbox("Comparison metric", metrics)
        cand1 = st.text_input("First candidate's National ID")
        intv1 = st.number_input("First candidate Interview No.", 1, 10)
        cand2 = st.text_input("Second candidate's National ID")
        intv2 = st.number_input("Second candidate Interview No.", 1, 10)
    with col4_2:  
        cand1_df, cand2_df = compare_two_cands(comp_id, job_title_compare, cand1, cand2, intv1, intv2, metric_compare)
        st.dataframe(cand1_df)
        st.dataframe(cand2_df)
        fig2 = plt.figure()
        c1_qn = cand1_df[cand1_df.columns[0]].tolist()
        c1_scores = cand1_df[cand1_df.columns[1]].tolist()

        c2_qn = cand2_df[cand2_df.columns[0]].tolist()
        c2_scores = cand2_df[cand2_df.columns[1]].tolist()

        # plot lines
        plt.plot(c1_qn, c1_scores, label="candidate 1")
        plt.plot(c2_qn, c2_scores, label="candidate 2")
        plt.xlabel(f'Question Number')
        plt.ylabel(f'scores')
        plt.title(f'Candidates Scores over questions')
        plt.legend()
        rc = {'figure.figsize':(8, 4.5),
              'axes.facecolor':'#0e1117',
              'axes.edgecolor': '#0e1117',
              'axes.labelcolor': 'white',
              'figure.facecolor': '#0e1117',
              'patch.edgecolor': '#0e1117',
              'text.color': 'white',
              'xtick.color': 'white',
              'ytick.color': 'white',
              'grid.color': 'grey',
              'font.size' : 12,
              'axes.labelsize': 12,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12}
        plt.rcParams.update(rc)
        st.pyplot(fig2)
        ##########
        
    with st.expander("View all jobs details"):
        colex1, colex2, colex3 = st.columns((1,3,1))
        jobs_df = pd.DataFrame(get_jobs_comp(comp_id), columns=jobs_cols)[jobs_cols[:-1]]
        with colex2:
            st.dataframe(jobs_df)
            
    with st.expander("View all analysis details of candidates"):
        analysis_df = pd.DataFrame(get_analysis_comp(comp_id), columns=analysis_cols)
        st.dataframe(analysis_df)


    col5_spacer1, col5, col5_spacer2 = st.columns((.2, 7.1, .2))
    with col5:
        st.subheader('Show all analysis details of a Job')
    col6_spacer1, col6_1, col6_spacer2, col6_2, col6_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col6_1:
        job_title_analysis = st.selectbox("Choose job for analysis", available_jobs)
    with col6_2:
        analysis_in_job_df = pd.DataFrame(get_analysis_with_job(comp_id, job_title_analysis), columns=analysis_cols)
        st.dataframe(analysis_in_job_df)
        
    col7_spacer1, col7, col7_spacer2 = st.columns((.2, 7.1, .2))
    with col7:
        st.subheader('Show all analysis details of a Candidate')
    col8_spacer1, col8_1, col8_spacer2, col8_2, col8_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col8_1:
        candindate_id = st.text_input("Write Candidate National ID")
    with col8_2:
        analysis_candidate_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_id), columns=analysis_cols)
        st.dataframe(analysis_candidate_df[analysis_cols[2:]])
        
    with st.expander("Individual Report"):
        candindate_ID = st.text_input("Write the Candidate's National ID")
        col_ind1, col_ind2, col_ind3 = st.columns(3)
        # No. of jobs applied for
        cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID), columns=analysis_cols)
        jobs_num = cand_analysis_df["job_title"].nunique()
        col_ind1.metric("Applied for", f'{jobs_num} Jobs')
        
        # No. of interviews he has done
        interviews_num = cand_analysis_df.groupby(["job_title", "interview_no"]).size().count()
        col_ind2.metric("Interviewd", f'{interviews_num}')
        
        # Average overall score in all interviews
        avg_overall_score_df = cand_analysis_df[["job_title", "interview_no", "overall_score"]]\
                        .groupby(["job_title", "interview_no"]).mean()
        avg_overall = round(avg_overall_score_df['overall_score'].mean(),2)
        col_ind3.metric("Acheived Average Overall Score", f'{avg_overall} %')
        
        st.subheader("Highest Achieved Scores")
        col_ind4, col_ind5, col_ind6, col_ind7 = st.columns(4)
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
        
        #For a single analysis video
        col9_spacer1, col9, col9_spacer2 = st.columns((.2, 7.1, .2))
        with col9:
            st.subheader('More analysis details')
        col10_spacer1, col10_1, col10_spacer2, col10_2, col10_spacer3  = st.columns((.2, 2, .4, 5, .2))
        with col10_1:
            cand_jobs = cand_analysis_df["job_title"].unique()
            cand_job_title = st.selectbox("Choose a Job title", cand_jobs)
            cand_interviews = cand_analysis_df[cand_analysis_df["job_title"]==cand_job_title]["interview_no"]
            cand_interview_no = st.selectbox("Select an Interview", cand_interviews.unique())
            cand_questions = cand_analysis_df[(cand_analysis_df["job_title"]==cand_job_title) &\
                            (cand_analysis_df["interview_no"]==cand_interview_no)]["question_no"]
            ques_no = st.selectbox("Select Question no.", list(cand_questions))
        with col10_2:

            cand_analysis = pd.DataFrame(get_one_analysis(comp_id, cand_job_title, candindate_ID, int(cand_interview_no), ques_no), columns=analysis_cols)
            st.dataframe(cand_analysis)
            FER_matrix = list(eval(cand_analysis["FER"][0]).values())
            tone_matrix = list(eval(cand_analysis["tone"][0]).values())
            fluency_matrix = list(eval(cand_analysis["fluency"][0]).values())
            
            FER_weights = np.mean(np.array(FER_matrix), axis=0)
            st.write(FER_matrix[0:5])
            st.dataframe(tone_matrix)
        progressbar_FER_weights(FER_weights)
            
        
        # st.header("Average scores of expressions")
        # st.write(f'angry: {round(100*FER_weights[0],2)}%')
        # st.progress(float(FER_weights[0]))
        # st.write(f'disgust: {round(100*FER_weights[1],2)}%')
        # st.progress(float(FER_weights[1]))
        # st.write(f'fear: {round(100*FER_weights[2],2)}%')
        # st.progress(float(FER_weights[2]))
        # st.write(f'happy: {round(100*FER_weights[3],2)}%')
        # st.progress(float(FER_weights[3]))
        # st.write(f'neutral: {round(100*FER_weights[4],2)}%')
        # st.progress(float(FER_weights[4]))
        # st.write(f'sad: {round(100*FER_weights[5],2)}%')
        # st.progress(float(FER_weights[5]))
        # st.write(f'surprise: {round(100*FER_weights[6],2)}%')
        # st.progress(float(FER_weights[6]))
                
    
