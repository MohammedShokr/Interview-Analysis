import streamlit as st

def load_view():
    st.title('Applicant data')
    cand_name = st.text_input('Full name')
    cand_id = st.text_input('National ID')
    cand_job = st.text_input('Applying for')

