from database_functions import *
import streamlit as st
import pandas as pd

# analysis_data_job = get_analysis_with_job("comp1", "HR")
# print(analysis_data_job)
result = get_analysis_with_job("comp1", "accountant")

df = pd.DataFrame(result,columns=["cand_ID", "comp_ID", "job_title",\
    "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
    "fluency", "fluency_score", "coherence_score", "overall_score"])

ranked_candidates = df[["cand_ID", "interview_no", "overall_score"]].groupby(["cand_ID", "interview_no"]).mean()
ranked_candidates = ranked_candidates.sort_values(by='overall_score', ascending=False)
print(df)
#st.dataframe(clean_df)
#my_matrix = str(FER_matrix)
#print(eval(my_matrix)[0])

FER_scores = df[["cand_ID", "job_title", "interview_no", "question_no", "FER", "FER_score"]].sort_values(by='FER_score', ascending=False)
print(FER_scores)

