from typing import Container
import streamlit as st
from PIL import Image


# ### css ###
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def load_view():
   local_css("styles_home.css")
   col1, col2 = st.columns(2)
   with st.container():
      col1.title("Choose skills; Not Identity.")
      #col1.title("Evaluate Humans based on their skills. Break the Bias and prejudice")
      col1.subheader("Skivia helps you measure your candidates skills")
      col1.button('Get Started')
   with st.container():
      with col2:
         image = Image.open('bg.png')
         st.image(image, caption='Video Interview Analyzer')
   ################################################################
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   ##############################################
   col1, col2, col3 = st.columns(3)
   with st.container():
      col1.header("Facial Expression Recognition Analysis")
      col1.header("Tone Analysis")
   with st.container(): 
      col2.header("Data Analytics")
   with st.container():
      col3.header("Fluency Analysis")
      col3.header("Coherence Analysis")
   ###############################################
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")

   ##################################################
   col1, col2, col3 = st.columns(3)
   with st.container():
      col2.title("Why Skivia?")
   st.write("")
   col1, col2, col3,col4 = st.columns(4)
   with st.container():
      col1.header("Reduce Hiring Bias     ")
   with st.container(): 
      col2.header("  Save Time")
   with st.container():
      col3.header("Enviormental Impacts")
   with st.container():
      col4.header("Save Money")
   ##################################################
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   ##################################
   col1, col2, col3 = st.columns(3)
   with st.container():
      col2.title("How Skivia works?")
   col1, col2, col3,col4 = st.columns(4)
   with st.container():
      col1.header("Step 1")
   with st.container(): 
      col2.header("Step 2")
   with st.container():
      col3.header("Step 3")
   with st.container():
      col4.header("Step 4")
   col1, col2, col3 = st.columns(3)
   with st.container():
      col2.title("Guide Video")
   ########################################
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   ######################################
   with st.container():
      st.title("Another an Ending Sentence..")
   ######################################
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   #########################################
   with st.container():
      st.header("About us")
      st.write("platform")
      st.write("Mission")