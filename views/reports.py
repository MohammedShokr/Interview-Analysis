import streamlit as st
from Queries import *

# Get the top candidates in a certain job

def load_view(comp_id):

    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
    
    
    col1_spacer1, col1, col1_spacer2 = st.columns((.2, 7.1, .2))
    with col1:
        st.subheader('Top 10 candidates in a Job')
    col2_spacer1, col2_1, col2_spacer2, col2_2, col2_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col2_1:
        job_title = st.selectbox("Choose job for analysis", available_jobs)    

    with col2_2:
        top_cands_df = get_top_cands_job_overall_score(comp_id, job_title)
        st.dataframe(top_cands_df)
        st.bar_chart(top_cands_df["overall_score"])
        
    col3_spacer1, col3, col3_spacer2 = st.columns((.2, 7.1, .2))
    with col3:
        st.subheader('Compare between two candidates')
    col4_spacer1, col4_1, col4_spacer2, col4_2, col4_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with col4_1:
        job_title = st.selectbox("Choose job", available_jobs)
        
        cand1 = st.text_input("First candidate's National ID")
        intv1 = st.number_input("First candidate Interview No.", 1, 10)
        cand2 = st.text_input("Second candidate's National ID")
        intv2 = st.number_input("Second candidate Interview No.", 1, 10)
        cand1_df, cand2_df = compare_two_cands(comp_id, job_title, cand1, cand2, intv1, intv2)
    with col4_2:
        st.dataframe(cand1_df)
        st.dataframe(cand2_df)
        
