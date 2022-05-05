import pandas as pd
from database_functions import *

def get_top_cands_job_overall_score(comp_id, job_title):
    result = get_analysis_with_job(comp_id, job_title)

    df = pd.DataFrame(result,columns=["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"])

    ranked_candidates = df[["cand_ID", "interview_no", "overall_score"]]\
                        .groupby(["cand_ID", "interview_no"]).mean()
    ranked_candidates = ranked_candidates.sort_values(by='overall_score', ascending=False)
    return ranked_candidates

def get_top_job_FER_score(comp_id, job_title):
    result = get_analysis_with_job(comp_id, job_title)

    df = pd.DataFrame(result,columns=["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"])
    FER_scores = df[["cand_ID", "job_title", "interview_no", "question_no", "FER", "FER_score"]]\
                .sort_values(by='FER_score', ascending=False)
    return FER_scores