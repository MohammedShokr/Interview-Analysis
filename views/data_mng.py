import streamlit as st
import pandas as pd
from database_functions import *

jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]
def load_view(comp_id):
    with st.sidebar:
        menu = ["Add new job","Add new candidate","Update","Delete"]
        choice = st.selectbox("Choose what you want to do",menu)
    if choice == "Add new job":
        st.subheader("Add a new Job")
        col1,col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title")

        job_req = st.text_input("Job requirements")
        job_description = st.text_input("Job desciption")
        
        col3, col4, col5 = st.columns((8,3,7))
        if col4.button("Add Job"):
            try:
                add_job(job_title, job_req, job_description, comp_id)
                st.success("Added the {} job to Jobs".format(job_title))
            except :
                st.error("This job details is already there! Enter a valid job title that is not already there")
        with st.expander("View all job details"):
            colex1, colex2, colex3 = st.columns((1,3,1))
            jobs_df = pd.DataFrame(get_jobs_comp(comp_id), columns=jobs_cols)[jobs_cols[:-1]]
            colex2.dataframe(jobs_df)
    
    elif choice == "Add new candidate":
        st.subheader("Add Candidate")
        
    elif choice == "Update":
        st.subheader("View Items")
        
    elif choice == "Delete":
        st.subheader("View Items")
        

        
