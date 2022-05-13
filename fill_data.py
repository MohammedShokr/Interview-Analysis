from ast import Try
from database_functions import *
import streamlit as st
import pandas as pd
import string
import random
import numpy as np

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
#         try:
#                 create_job(i)
#         except:
#                 pass

# with open("names.txt",'r') as f:
#    names = f.read().splitlines()

# def insert_candidate(i):
#         cand_name = names[random.randint(0, len(names)-1)]
#         cand_quali = "qualifications of candidate" + str(i)
#         add_candidate(i, cand_name, cand_quali)

# for i in range(5000):
#         insert_candidate(i)


#add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score)


def create_matrix(n):
  matrix = {}
  for i in range(random.randint(30,200)):
    scores = list(np.random.dirichlet(np.ones(n),size=1)[0])
    matrix[i] = scores
  weights = np.mean(np.array(list(matrix.values())), axis=0)
  return matrix, weights

#companies = get_company_IDs()
def create_analysis(cand, title, n):
        cand_ID = cand #random.randint(0, 4999)
        comp_ID = 5 #companies[random.randint(0, len(companies)-1)][0]
        #comp_jobs =  get_jobs_comp(comp_ID)
        #while not comp_jobs: # keep tryng to find a company with jobs
        #        comp_ID = companies[random.randint(0, len(companies)-1)][0]
        #        comp_jobs = get_jobs_comp(comp_ID)
        
        job_title = title #comp_jobs[random.randint(0, len(comp_jobs)-1)][0]
        interview_no = 1 #random.randint(1, 5)
        question_no = n #random.randint(1, 10)
        FER, FER_weigts = create_matrix(7)
        FER_score = random.randint(0, 100)
        tone, tone_weights = create_matrix(5)
        tone_score = random.randint(0, 100)
        fluency, fluency_weights = create_matrix(3)
        fluency_score = random.randint(0, 100)
        coherence_score = random.random()
        overall_score = ((0.01*FER_score)+(0.01*tone_score)+(coherence_score)+ (0.01*fluency_score))/(0.01*4)
        add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, str(FER) , FER_score, str(tone), tone_score, str(fluency), fluency_score, coherence_score, overall_score)

comp_jobs = get_jobs_comp('5')
#comp_jobs[random.randint(0, len(comp_jobs)-1)][0]
for job in comp_jobs:
        randi = random.randint(0,4999)
        for i in range(randi, randi + 50):
                for j in range(1,8+random.randint(0,10)):
                        create_analysis(i, job[0], j)
# for i in range(50000):
#         try:
#                 create_analysis()
#         except:
#                 pass


