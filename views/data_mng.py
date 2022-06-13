from faulthandler import disable
from pickle import TRUE
import streamlit as st
import pandas as pd
from database_functions import *

def load_view(comp_id):
    # getting useful resources to load queries into dataframes consitently
    available_jobs = [job[0] for job in get_jobs_comp(comp_id)]  # all job titles this company have
    jobs_cols = ["job_title", "job_req", "job_description", "comp_ID"]  # columns of jobs table
    cand_cols = ["candidate ID", "candidate name", "candidate qualifications"]  # cloumns of candidate table
    analysis_cols = ["cand_ID", "comp_ID", "job_title",\
        "interview_no", "question_no", "FER" , "FER_score", "tone", "tone_score",\
        "fluency", "fluency_score", "coherence_score", "overall_score"]   # columns of analysis table
    
    # In a sidebar, let the user select the page to manage from a  dropdown menu
    with st.sidebar:
        st.subheader("Database Management")  # informational header
        menu = ["Manage Jobs","Manage Candidates","Manage Analysis Data"]  # selection menu
        choice = st.selectbox("Choose what you want to do: ",menu)  # drop down menu creation 
    
    ##################################### Manage Jobs ##################################################    
    if choice == "Manage Jobs":
        ############ Add a new job ################
        st.subheader("Add a new Job")
        col1,col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Enter a Job Title")   # text input of job title to be added

        job_req = st.text_input("Job requirements")          # text input of job requirements to be added
        job_description = st.text_input("Job description")   # text input of job description to be added
        
        col3, col4, col5 = st.columns((8,3,7))
        if col4.button("Add Job"):    # add job button method
            try:
                add_job(job_title, job_req, job_description, comp_id)   #database fuction call to add the job
                st.success("Added the {} job to Jobs".format(job_title)) # success message
            except :
                # printing an error message if the job was not added to the database
                st.error("This job details is already there! Enter a valid job title that is not already there")
        
        ################ Edit job #####################
        st.subheader("Edit Jobs data")
        
        if len(available_jobs):  # only make it available if the company has any jobs to edit
            selected_job_edit = st.selectbox("Choose a Job Title to edit", available_jobs) # select the job title to edt its info
            selected_job_details = get_job(selected_job_edit, comp_id)[0] # get the job details of the the selected title, from database functions
            job_req = st.text_input("Job requirements", selected_job_details[1]) # editable textbox viewing current job requirements
            job_description = st.text_input("Job description", selected_job_details[2])  # editable textbox viewing current job description
            col6, col7, col8 = st.columns((8,3,7))  # styling button alignment
            if col7.button("Update Job"):
                try:
                    update_job(selected_job_edit, comp_id, job_req, job_description) # update the job with the new details
                    st.success("Updated the {} job successfully".format(selected_job_edit)) # success message
                except :
                    # printing an error message if the job was not updated
                    st.error("This shouldnot happen!!!!!!!")
        else:
            st.info("You don't have any jobs to edit")  # info message to show to the company of no jobs
        
        ############## Delete job ################
        st.subheader("Delete a job")
        col9, col10, col11 = st.columns((6,6,2))   # styling button alignment
        if len(available_jobs):
            selected_job_delete = col9.selectbox("Choose a Job Title to delete", available_jobs) # menu of available job titles to delete 
            if col11.button("Delete Job"):
                try:
                    delete_job(selected_job_delete, comp_id)  #delete a job with the given title
                    st.success("deleted the {} job successfully".format(selected_job_delete)) # success message
                except :
                    # printing an error message if the job was not deleted
                    st.error("This shouldnot happen!!!!!!!")
        else:
            st.info("You don't have any jobs to delete")  # info message to show to the company of no jobs
        
        ########### view all jobs ##############
        with st.expander("View all jobs in details"):
            colex1, colex2, colex3 = st.columns((1,10,1))   # styling dataframe alignment
            jobs_df = pd.DataFrame(get_jobs_comp(comp_id), columns=jobs_cols)[jobs_cols[:-1]] # get all jobs of that company with all details
            colex2.dataframe(jobs_df)   # print the dataframe
            
    ######################################### Manage candidates ####################################
    elif choice == "Manage Candidates":
        ################### Add new candidate ###############
        st.subheader("Add Candidate")
        col12,col13 = st.columns(2)
        candidate_id = col12.text_input("Enter candidate's ID")  # text input of candidate ID to add
        candidate_name = col13.text_input("Enter Candidate's name") # text input of candidate name to add
        candidate_qual = st.text_input("Candidate qualifications") # text input of candidate qalufications to add
        
        col14, col15, col16 = st.columns((8,3,7))    # styling button alignment
        if col15.button("Add Candidate"):
            try:
                add_candidate(candidate_id, candidate_name, candidate_qual)  # add the candidate details to the database
                st.success("The candidate has been successfully added to the database") # success message 
            except :
                st.info("This candidate is already there! Enter a valid candidate ID") # error message informing the reason of the error
        ################### Edit candidate data ###################
        st.subheader("Edit Candidate data")
        col17,col18 = st.columns(2)
        candidate_id_edit = col17.text_input("Enter the candidate's ID") # text input to enter the candidate to be edited
        if candidate_id_edit:
            try:
                selected_cand_details = get_cand(candidate_id_edit)[0]   # get the candidates details to be easily edited
                candidate_name_edit = col18.text_input("Updated candidate name", selected_cand_details[1]) # editable textbox with the current candidate name
                candidate_qual_edit = st.text_input("Updated candidate qualifications", selected_cand_details[2]) # editable textbox with the current candidate qualifications
            except:
                st.error("You entered a non-valid candidate ID") # error message with the corresponding error
            
        col19, col20, col21 = st.columns((8,3,7))   # styling button alignment
        if col20.button("Edit Candidate"):
            try:
                update_cand(candidate_id_edit, candidate_name_edit, candidate_qual_edit) # update the edited detailes in the database
                st.success("The candidate details has been successfully updated") # success message
            except:
                # printing an error message if the candidate was not updated
                st.error("This shouldnot happen!!!!!!!")
        #################### view all candidates #################
        with st.expander("View all candidate"):
            colex4, colex5, colex6 = st.columns((1,10,1))
            cands_df = pd.DataFrame(view_candidate_data(), columns=cand_cols) # get the candidates table and load it into a dataframe
            colex5.dataframe(cands_df) # print the dataframe 
            
    ###################################### Manage Analysis ########################################        
    elif choice == "Manage Analysis Data":
        ######################## Edit Analysis Data #########################
        st.subheader("Edit Analysis data")
        st.markdown("Choose analysis data to tune the needed weights")
        col22, col23 = st.columns(2)
        candindate_ID = col22.text_input("Enter Candidate's National ID") # enter the candidate id to update its analysis results
        if candindate_ID:
            # getting all analysis of that candidate and load it into a dataframe
            cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID), columns=analysis_cols)
            cand_jobs = cand_analysis_df["job_title"].unique() # get the jobs he applied for
            cand_job_title = col23.selectbox("Choose a Job title", cand_jobs)  # selection menu of avalible jobs the candidate applied for
            cand_interviews = cand_analysis_df[cand_analysis_df["job_title"]==cand_job_title]["interview_no"] # get all the interview numbers the candidate did for that job
            cand_interview_no = col22.selectbox("Select an Interview", cand_interviews.unique()) # selelct an interview menu creation
            cand_questions = cand_analysis_df[(cand_analysis_df["job_title"]==cand_job_title) &\
                            (cand_analysis_df["interview_no"]==cand_interview_no)]["question_no"] # get the question no. that has results
            ques_no = col23.selectbox("Select Question no.", list(cand_questions)) # create the selection menu of the available qustions
            cand_interview_no = int(cand_interview_no) #cast the type of the interview no. into int
            # get the analysis result according to user selection, and load it into a dataframe.
            cand_analysis = pd.DataFrame(get_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no), columns=analysis_cols)
            
            st.markdown("Adjust weights to change the effective overall score") # Inform the user to edit the desired scores
            
            # slider tuning of the FER score
            col24, col25 = st.columns((10, 3))
            fer_weight = col24.slider('FER weight', 0, 100, 50)
            FER_score = col25.text_input('FER Score %', cand_analysis['FER_score'][0], disabled=True)
            
            # slider tuning of the tone score
            col26, col27 = st.columns((10, 3))
            tone_weight = col26.slider('Tone analysis weight', 0, 100, 50)
            tone_score = col27.text_input('Tone analysis Score %', cand_analysis['tone_score'][0], disabled=True)
            
            # slider tuning of the fluency score
            col28, col29 = st.columns((10, 3))
            fluency_weight = col28.slider('Fluency analysis weight', 0, 100, 50)
            fluency_score = col29.text_input('Fluency analysis Score %', cand_analysis['fluency_score'][0], disabled=True)
            
            # slider tuning of the coherence score
            col30, col31 = st.columns((10, 3))
            coherence_weight = col30.slider('English Topic coherence weight', 0, 100, 50)
            coherence_score = col31.text_input('Topic coherence Score %', round(100*cand_analysis['coherence_score'][0]), disabled=True)
            
            # Recalculate the ooverall score according to the new used weights, and view it
            _, col32, _, col33, _ = st.columns((1, 5, 0.5, 3, 1))
            overall_score = ((0.01*fer_weight*cand_analysis['FER_score'][0])+\
                (0.01*tone_weight*cand_analysis['tone_score'][0])+\
                (0.01*fluency_weight*cand_analysis['fluency_score'][0])+\
                (coherence_weight*cand_analysis['coherence_score'][0]))/\
                (0.01*fer_weight+0.01*tone_weight+0.01*fluency_weight+0.01*coherence_weight)
            overall_score = col32.text_input('The newly calulated overall score %', round(overall_score,2), disabled=True)
            col33.markdown("\n")
            col33.markdown("\n")
            if col33.button('Update Analysis'):  # update the analysis result according to the new adjusted weights
                update_one_analysis(comp_id, cand_job_title, candindate_ID, cand_interview_no, ques_no, overall_score)
                st.success("The analysis data is successfully updated!") # success message
               
        ########################### Delete Analysis Data ######################## 
        st.subheader("Delete Analysis")
        col34, col35 = st.columns(2)
        candindate_ID_delete = col34.text_input("Candidate's National ID")  # textbox to enter candidate id to delete its results data
        # getting all analysis result of that candidate and load it into a dataframe
        delete_cand_analysis_df = pd.DataFrame(get_analysis_with_cand(comp_id, candindate_ID_delete), columns=analysis_cols)
        if not delete_cand_analysis_df.empty:
            delete_cand_jobs = delete_cand_analysis_df["job_title"].unique()  # get the jobs that candidate applied for
            delete_cand_job_title = col35.selectbox("Job title", delete_cand_jobs) # let the user select whivh jon=b using drop down menu
            delete_cand_interviews = delete_cand_analysis_df[delete_cand_analysis_df["job_title"]==delete_cand_job_title]["interview_no"] # get the interviews that candidate did for that job
            delete_cand_interview_no = col34.selectbox("Interview Number", delete_cand_interviews.unique()) # let the user which interview to delete
            delete_cand_questions = delete_cand_analysis_df[(delete_cand_analysis_df["job_title"]==delete_cand_job_title) &\
                            (delete_cand_analysis_df["interview_no"]==delete_cand_interview_no)]["question_no"] # get the questions of the selected interview
            delete_ques_no = col35.selectbox("Question Number", list(delete_cand_questions)) # let the user select the question to be deleted
            delete_cand_interview_no = int(delete_cand_interview_no)
            # # show the user the data to be deleted
            delete_cand_analysis = pd.DataFrame(get_one_analysis(comp_id, delete_cand_job_title, candindate_ID_delete, delete_cand_interview_no, delete_ques_no), columns=analysis_cols)
            st.dataframe(delete_cand_analysis)
            _, col36, _ = st.columns((8,3,7))     # styling button alignment
            if col36.button('Delete analysis'): # delete the selected analysis result
                delete_one_analysis(comp_id, delete_cand_job_title, candindate_ID_delete, delete_cand_interview_no, delete_ques_no)
        
        ###################### View analysis data #################################
        with st.expander("View all analysis"):
            colex7, colex8, colex9 = st.columns((1,10,1))
            analysis_df = pd.DataFrame(get_analysis_comp(comp_id), columns=analysis_cols) # get the analysis result in that company and load it into a dataframe
            colex8.dataframe(analysis_df) # print the dataframe 
        