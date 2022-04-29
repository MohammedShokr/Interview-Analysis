import streamlit as st
from database_functions import *

def load_view():
    with st.sidebar:
        menu = ["Add new job","Add new candidate","Update","Delete"]
        choice = st.selectbox("Choose what you want to do",menu)
    if choice == "Add new job":
        st.subheader("Add a new Job")
        col1,col2 = st.columns(2)
        with col1:
            job_id = st.number_input("Job ID")
            
        with col2:
            job_title = st.text_input("Job Title")
            #job_status = st.selectbox("Job Status",["Open","Inprogress","Closed"])
            #job_date = st.date_input("")
            
        job_req = st.text_input("Job requirements")
        job_description = st.text_input("Job desciption")
        if st.button("Add Job"):
            add_job(job_id,job_title,job_req=job_req, job_description=job_description)
            st.success("Added the {} job to Jobs".format(job_title))
    
    elif choice == "Add new candidate":
        st.subheader("Add Candidate")
        
    elif choice == "Update":
        st.subheader("View Items")
        
    elif choice == "Delete":
        st.subheader("View Items")
        

        
