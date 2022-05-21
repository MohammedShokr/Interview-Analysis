import streamlit as st
# import utils as utl
# from views import home, about, analysis, options, configuration
from main import navigation
# from database_functions import *

# st.set_page_config(layout="wide", page_title='Navbar sample')
st.set_option('deprecation.showPyplotGlobalUse', False)
# utl.inject_custom_css()
# utl.navbar_component()
# create_tables()
# print(view_schema())


def load_view():
    username = st.text_input("Username: ")
    but1 = st.button("Login")
    if but1:
        if username == "lol":
            st.write("GOOD")
            navigation()
        else:
            st.write("BAD")


load_view()



