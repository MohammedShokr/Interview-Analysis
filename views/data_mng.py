import streamlit as st
import pandas as pd
from database_functions import *

def load_view(comp_id):
    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]
    jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]
    cand_cols = ["candidate ID", "candidate name", "candidate qualifications"]
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
            selected_job_details = get_job(selected_job_edit, comp_id)[0]
            job_req = st.text_input("Job requirements", selected_job_details[1])
            job_description = st.text_input("Job description", selected_job_details[2])
            col6, col7, col8 = st.columns((8,3,7))
            if col7.button("Update Job"):
                update_job(selected_job_edit, comp_id, job_req, job_description)
        else:
            st.info("You don't have any jobs to edit")
        
            
        st.subheader("Delete a job")
        col9, col10, col11 = st.columns((6,6,2))
        if len(available_jobs):
            selected_job_delete = col9.selectbox("Choose a Job Title to delete", available_jobs)
            if col11.button("Delete Job"):
                delete_job(selected_job_delete, comp_id)
        else:
            st.info("You don't have any jobs to delete")
            
        with st.expander("View all jobs in details"):
            colex1, colex2, colex3 = st.columns((1,10,1))
            jobs_df = pd.DataFrame(get_jobs_comp(comp_id), columns=jobs_cols)[jobs_cols[:-1]]
            colex2.dataframe(jobs_df)
    
    elif choice == "Manage Candidates":
        st.subheader("Add Candidate")
        col12,col13 = st.columns(2)
        candidate_id = col12.text_input("Enter candidate's ID")
        candidate_name = col13.text_input("Enter Candidate's name")
        candidate_qual = st.text_input("Candidate qualifications")
        
        col14, col15, col16 = st.columns((8,3,7))
        if col15.button("Add Candidate"):
            try:
                add_candidate(candidate_id, candidate_name, candidate_qual)
                st.success("The candidate has been successfully added to the database")
            except :
                st.info("This candidate is already there! Enter a valid candidate ID")
        
        st.subheader("Edit Candidate data")
        col17,col18 = st.columns(2)
        candidate_id_edit = col17.text_input("Enter the candidate's ID", 1)
        try:
            selected_cand_details = get_cand(candidate_id_edit)[0]
            candidate_name_edit = col18.text_input("Updated candidate name", selected_cand_details[1])
            candidate_qual_edit = st.text_input("Updated candidate qualifications", selected_cand_details[2])
        except:
            st.error("You entered a non-valid candidate ID")
        
        col19, col20, col21 = st.columns((8,3,7))
        if col20.button("Edit Candidate"):
            update_cand(candidate_id_edit, candidate_name_edit, candidate_qual_edit)
            st.success("The candidate details has been successfully updated")
        with st.expander("View all candidate"):
            colex4, colex5, colex6 = st.columns((1,10,1))
            cands_df = pd.DataFrame(view_candidate_data(), columns=cand_cols)
            colex5.dataframe(cands_df)        
    elif choice == "Manage Analysis Data":
        st.subheader("Edit Analysis data")
        st.subheader("Delete Analysis")
        
        

        
