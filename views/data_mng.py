from faulthandler import disable
from pickle import TRUE
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
        ######################## Edit Analysis Data #########################
        st.subheader("Edit Analysis data")
        st.markdown("Choose analysis data to tune the needed weights")
        col22, col23 = st.columns(2)
        candindate_ID = col22.text_input("Enter Candidate's National ID")
        cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID), columns=analysis_cols)
        cand_jobs = cand_analysis_df["job_title"].unique()
        cand_job_title = col23.selectbox("Choose a Job title", cand_jobs)
        cand_interviews = cand_analysis_df[cand_analysis_df["job_title"]==cand_job_title]["interview_no"]
        cand_interview_no = col22.selectbox("Select an Interview", cand_interviews.unique())
        cand_questions = cand_analysis_df[(cand_analysis_df["job_title"]==cand_job_title) &\
                        (cand_analysis_df["interview_no"]==cand_interview_no)]["question_no"]
        ques_no = col23.selectbox("Select Question no.", list(cand_questions))
        cand_interview_no = int(cand_interview_no)
        cand_analysis = pd.DataFrame(get_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no), columns=analysis_cols)
        
        st.markdown("Adjust weights to change the effective overall score")
        col24, col25 = st.columns((10, 3))
        fer_weight = col24.slider('FER weight', 0, 100, 50)
        FER_score = col25.text_input('FER Score %', cand_analysis['FER_score'][0], disabled=True)
        
        col26, col27 = st.columns((10, 3))
        tone_weight = col26.slider('Tone analysis weight', 0, 100, 50)
        tone_score = col27.text_input('Tone analysis Score %', cand_analysis['tone_score'][0], disabled=True)
        
        col28, col29 = st.columns((10, 3))
        fluency_weight = col28.slider('Fluency analysis weight', 0, 100, 50)
        fluency_score = col29.text_input('Fluency analysis Score %', cand_analysis['fluency_score'][0], disabled=True)
        
        col30, col31 = st.columns((10, 3))
        coherence_weight = col30.slider('English Topic coherence weight', 0, 100, 50)
        coherence_score = col31.text_input('Topic coherence Score %', round(100*cand_analysis['coherence_score'][0]), disabled=True)
        
        _, col32, _, col33, _ = st.columns((1, 5, 0.5, 3, 1))
        overall_score = ((0.01*fer_weight*cand_analysis['FER_score'][0])+\
            (0.01*tone_weight*cand_analysis['tone_score'][0])+\
            (0.01*fluency_weight*cand_analysis['fluency_score'][0])+\
            (coherence_weight*cand_analysis['coherence_score'][0]))/\
            (0.01*fer_weight+0.01*tone_weight+0.01*fluency_weight+0.01*coherence_weight)
        overall_score = col32.text_input('The newly calulated overall score %', round(overall_score,2), disabled=True)
        col33.markdown("\n")
        col33.markdown("\n")
        if col33.button('Update Analysis'):
            update_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no, overall_score)
               
        ########################### Delete Analysis Data ######################## 
        st.subheader("Delete Analysis")
        col34, col35 = st.columns(2)
        candindate_ID_delete = col34.text_input("Candidate's National ID")
        delete_cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID_delete), columns=analysis_cols)
        if not delete_cand_analysis_df.empty:
            delete_cand_jobs = delete_cand_analysis_df["job_title"].unique()
            delete_cand_job_title = col35.selectbox("Job title", delete_cand_jobs)
            delete_cand_interviews = delete_cand_analysis_df[delete_cand_analysis_df["job_title"]==delete_cand_job_title]["interview_no"]
            delete_cand_interview_no = col34.selectbox("Interview Number", delete_cand_interviews.unique())
            delete_cand_questions = delete_cand_analysis_df[(delete_cand_analysis_df["job_title"]==delete_cand_job_title) &\
                            (delete_cand_analysis_df["interview_no"]==delete_cand_interview_no)]["question_no"]
            delete_ques_no = col35.selectbox("Question Number", list(delete_cand_questions))
            delete_cand_interview_no = int(delete_cand_interview_no)
            delete_cand_analysis = pd.DataFrame(get_one_analysis(comp_id, delete_cand_job_title, candindate_ID_delete, delete_cand_interview_no, delete_ques_no), columns=analysis_cols)
            st.dataframe(delete_cand_analysis)
            _, col36, _ = st.columns((8,3,7))
            if col36.button('Delete analysis'):
                delete_one_analysis(comp_id, delete_cand_job_title, candindate_ID_delete, delete_cand_interview_no, delete_ques_no)
        
        ###################### View analysis data #################################
        

        
