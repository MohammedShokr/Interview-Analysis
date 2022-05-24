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

def candidate_evaluation(score):
    if score>=85:
        return "Excellent Candidate, Having very cood communication skills and is meeting your requirements"
    elif score>=75:
        return "Very Good candidate, You can consider hiring him"
    elif score>=65:
        return "Good candidate, with average performance"
    elif score>=50:
        return "The candidate has passed the minimal specified requirements"
    else:
        return "Not accepted Candidate, The candidate could not pass the non technical Interview"
    
def progressbar_FER_weights(FER_weights):
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Angry")
        col2.progress(float(FER_weights[0]))
        col3.write(f'{round(100*FER_weights[0],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Disgust")
        col2.progress(float(FER_weights[1]))
        col3.write(f'{round(100*FER_weights[1],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Fear")
        col2.progress(float(FER_weights[2]))
        col3.write(f'{round(100*FER_weights[2],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write(f'Happy')
        col2.progress(float(FER_weights[3]))
        col3.write(f'{round(100*FER_weights[3],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Neutral")
        col2.progress(float(FER_weights[4]))
        col3.write(f'{round(100*FER_weights[4],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Sad")
        col2.progress(float(FER_weights[5]))
        col3.write(f'{round(100*FER_weights[5],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Surprise")
        col2.progress(float(FER_weights[6]))
        col3.write(f'{round(100*FER_weights[6],2)}%')


def progressbar_tone_weights(tone_weights):
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Angry")
        col2.progress(float(tone_weights[0]))
        col3.write(f'{round(100*tone_weights[0],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Fear")
        col2.progress(float(tone_weights[1]))
        col3.write(f'{round(100*tone_weights[1],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Happy")
        col2.progress(float(tone_weights[2]))
        col3.write(f'{round(100*tone_weights[2],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Sad")
        col2.progress(float(tone_weights[3]))
        col3.write(f'{round(100*tone_weights[3],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Surprise")
        col2.progress(float(tone_weights[4]))
        col3.write(f'{round(100*tone_weights[4],2)}%')


def progressbar_fluency_weights(fluency_weights):
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Not Fluent")
        col2.progress(float(fluency_weights[0]))
        col3.write(f'{round(100*fluency_weights[0],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Average Fluency")
        col2.progress(float(fluency_weights[1]))
        col3.write(f'{round(100*fluency_weights[1],2)}%')
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.write("Fluent")
        col2.progress(float(fluency_weights[2]))
        col3.write(f'{round(100*fluency_weights[2],2)}%')


