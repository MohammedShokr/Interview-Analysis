import streamlit as st
import pandas as pd
from FER import analyze_face
from tone import analyze_tone
from database_functions import *

curr_cand_id = st.text_input("Ender your candidate National ID")
curr_cand_data = get_cand(curr_cand_id)
if curr_cand_data:
    st.write(curr_cand_data)
else:
    st.error('A candidate of this ID is not in the database')
    with st.expander("Add a new candidate"):
        add_cand_form = st.form(key='add_candidate')
        cand_name = add_cand_form.text_input("Enter Candidate's name")
        cand_id = add_cand_form.text_input("Ender candidate National ID")
        cand_qualifications = add_cand_form.text_input("Enter candidate's qualification")
        add_cand_btn = add_cand_form.form_submit_button('Add Candidate')
    if add_cand_btn:
        try:
            add_candidate(cand_id, cand_name, cand_qualifications)
            st.success('The candidate added successfuly to the database')
        except:
            st.error('This data cannot be inserted. Already an ID')
        with st.expander("View All Candidates "):
            result = view_candidate_data()
            # st.write(result)
            clean_df = pd.DataFrame(result,columns=["ID","Name","Qualification"])
            st.dataframe(clean_df)


