import pandas as pd
from pyparsing import col
from database_functions import *
import streamlit as st

cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]

def get_top_cands_job(comp_id, job_title, metric):
    result = get_analysis_with_job(comp_id, job_title)
    df = pd.DataFrame(result,columns=cols)

    ranked_candidates = df[["cand_ID", "interview_no", metric]]\
                        .groupby(["cand_ID", "interview_no"]).mean()
    ranked_candidates.reset_index(inplace=True)
    if not ranked_candidates.empty:
        ranked_candidates = ranked_candidates.sort_values("interview_no").groupby("cand_ID").tail(1)
        ranked_candidates = ranked_candidates.sort_values(by= metric, ascending=False).head(10)
    return ranked_candidates


def compare_two_cands(comp_id, job_title, cand1, cand2, intv1, intv2, metric):
    cand1_df = get_analysis_with_job_cand(comp_id, job_title, cand1, intv1)
    cand2_df = get_analysis_with_job_cand(comp_id, job_title, cand2, intv2)
    cand1_df = pd.DataFrame(cand1_df,columns=cols)
    cand2_df = pd.DataFrame(cand2_df,columns=cols)
    
    ##################### Temp solution for multiple data for each question ####################
    # cand1_df = cand1_df[cand1_df[metric]>0]
    # cand2_df = cand2_df[cand2_df[metric]>0]
    #############################################################################################
    
    return cand1_df[["question_no", metric]], cand2_df[["question_no", metric]]


def progressbar_FER_weights(FER_weights):
    col1, col2, col3 = st.columns((1,10,1))
    with col1:
        st.write("Angry:")
        st.write("Disgust:")
        st.write("Fear")
        st.write("Happy")
        st.write("Neutral")
        st.write("Sad")
        st.write("Surprise")
        
    with col2:
        st.progress(float(FER_weights[0]))
        st.progress(float(FER_weights[1]))
        st.progress(float(FER_weights[2]))
        st.progress(float(FER_weights[3]))
        st.progress(float(FER_weights[4]))
        st.progress(float(FER_weights[5]))
        st.progress(float(FER_weights[6]))
    with col3:
        st.write(f'{round(100*FER_weights[0],2)}%')
        st.write(f'{round(100*FER_weights[1],2)}%')
        st.write(f'{round(100*FER_weights[2],2)}%')
        st.write(f'{round(100*FER_weights[3],2)}%')
        st.write(f'{round(100*FER_weights[4],2)}%')
        st.write(f'{round(100*FER_weights[5],2)}%')
        st.write(f'{round(100*FER_weights[6],2)}%')
