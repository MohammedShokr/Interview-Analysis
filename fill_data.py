from database_functions import *
import streamlit as st
import pandas as pd

cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]

result = view_analysis_data()
df = pd.DataFrame(result,columns=cols)

# my_matrix = df["FER"]
# print(eval(my_matrix[0]))

# FER_scores = df[["cand_ID", "job_title", "interview_no", "question_no", "FER", "FER_score"]].sort_values(by='FER_score', ascending=False)
# print(FER_scores)

