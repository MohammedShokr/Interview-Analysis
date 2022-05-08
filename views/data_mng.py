import streamlit as st
import pandas as pd
from database_functions import *

def load_view(comp_id):
    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
    jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]
    analysis_cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]
    
    with st.sidebar:
        st.subheader("Database Management")
        menu = ["Manage Jobs","Manage Candidates","Manage Analysis Data"]
        choice = st.selectbox("Choose what you want to do: ",menu)
        
    if choice == "Manage Jobs":
        
        st.subheader("Add a new Job")
        col1,col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Enter a Job Title")

        job_req = st.text_input("Job requirements")
        job_description = st.text_input("Job description")
        
        col3, col4, col5 = st.columns((8,3,7))
        if col4.button("Add Job"):
            try:
                add_job(job_title, job_req, job_description, comp_id)
                st.success("Added the {} job to Jobs".format(job_title))
            except :
                st.error("This job details is already there! Enter a valid job title that is not already there")
        
        
        st.subheader("Edit Jobs data")
        
        if len(available_jobs):
            selected_job_edit = st.selectbox("Choose a Job Title to edit", available_jobs)
            selected_job_details = get_job(selected_job_edit, comp_id)
            job_req = st.text_input("Job requirements", selected_job_details[0][1])
            job_description = st.text_input("Job description", selected_job_details[0][2])
            col6, col7, col8 = st.columns((8,3,7))
            if col7.button("Update Job"):
                update_job(selected_job_edit, comp_id, job_req, job_description)
        else:
            st.info("You don't have any jobs to edit")
        
            
        st.subheader("Delete a job")
        col9, col10, col11 = st.columns((2,6,2))
        if len(available_jobs):
            selected_job_delete = col9.selectbox("Choose a Job Title to delete", available_jobs)
            if col11.button("Delete Job"):
                delete_job(selected_job_delete, comp_id)
        else:
            st.info("You don't have any jobs to delete")
            
        with st.expander("View all job details"):
            colex1, colex2, colex3 = st.columns((1,3,1))
            jobs_df = pd.DataFrame(get_jobs_comp(comp_id), columns=jobs_cols)[jobs_cols[:-1]]
            colex2.dataframe(jobs_df)
    
    elif choice == "Manage Candidates":
        st.subheader("Add Candidate")
        st.subheader("Edit Candidate data")
        
    elif choice == "Manage Analysis Data":
        st.subheader("Edit Analysis data")
        st.subheader("Delete Analysis")
        
        

        
