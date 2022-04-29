import streamlit as st
import utils as utl
from views import data_mng, home,analysis,options,configuration
from database_functions import *

st.set_page_config(layout="wide", page_title='Soft-Skill Interview Analysis')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()
st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #99ff99 , #00ccff);
        }
    </style>""",
    unsafe_allow_html=True,
)
def navigation():
    route = utl.get_current_route()
    if route == "home":
        home.load_view()
    elif route == "data_mng":
        data_mng.load_view()
    elif route == "analysis":
        analysis.load_view()
    elif route == "options":
        options.load_view()
    elif route == "configuration":
        configuration.load_view()
    elif route == None:
        home.load_view()
        
navigation()