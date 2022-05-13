from database_functions import *
import streamlit as st
import pandas as pd
import string
import random
letters = string.ascii_letters


cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]

# print(pd.DataFrame(get_analysis_with_cand("comp1", "3"), columns=cols))

# my_matrix = df["FER"]
# print(eval(my_matrix[0]))

# FER_scores = df[["cand_ID", "job_title", "interview_no", "question_no", "FER", "FER_score"]].sort_values(by='FER_score', ascending=False)
# print(FER_scores)
# def add_comp(i):
#         letter1 = random.choice(string.ascii_letters)
#         letter2 = random.choice(string.ascii_letters)
#         letter3 = random.choice(string.ascii_letters)
#         letter4 = random.choice(string.ascii_letters)
#         comp_name = "company_" + letter1 + letter2 + letter3 + letter4
#         comp_web = "www.comp_"+letter1+letter2+letter3 + letter4+".com"
#         comp_pass = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))    
#         add_company(i, comp_name, comp_pass,comp_web)

# for i in range(1000):
#         add_comp(i)
# with open("jobs.txt",'r') as f:
#   jobs = f.read().splitlines()

# def create_job(i):
#         job_reqs = "list of reqs" + str(i)
#         job_desc = "description of job" + str(i)
#         comp_ID = random.randint(0,999)

#         add_job(jobs[random.randint(0,len(jobs)-1)], job_reqs, job_desc, comp_ID)

# for i in range(5000):
#         create_job(i)

# with open("names.txt",'r') as f:
#    names = f.read().splitlines()

# def insert_candidate(i):
#         cand_name = names[random.randint(0, len(names)-1)]
#         cand_quali = "qualifications of candidate" + str(i)
#         add_candidate(i, cand_name, cand_quali)

# for i in range(5000):
#         insert_candidate(i)


#add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score)
print(get_one_analysis("comp1", "CV Engineer", "1", 1, 4))


