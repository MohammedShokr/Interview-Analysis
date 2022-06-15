'''
This Code was made by the following 4 UST-ZC students, for their graduation project, CIE'22:
                    Shaimaa Said Hassanen 		    | 201700249
                    Mohammed Younis El-Sawi 	    | 201700915
                    Abdelrahman Alaa Elaraby 		| 201700556
                    Habiba Ramadan Mahmoud 	        | 201700832
                    
                Communications and Information Engineering Department
                            Supervised by:
                            Dr. Elsayed Eisa Hemayed
                            Dr. Mohamed Samir Eid
                  Zewail City of Science, Technology and Innovation,
                                Giza, 12578, Egypt
'''

# imports and used libraries
import streamlit as st
import utils as utl
from views import home, data_mng, analysis, reports
from database_functions import *
import webbrowser
from bokeh.models.widgets import Div
import streamlit as st
import atexit

# code snippet we run in the first time for creating tables
#create_tables()
#print(view_schema())


# Function to attach CSS file to a specific page
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



# Keep tracking of the logged in user and ther status
logged_in = [0, ""]
with open("vars.txt", "r") as f:
    cache = f.readlines()
    if cache:
        logged_in[0] = int(cache[0])
        logged_in[1] = cache[1]

# getting all the users and their passwords from the database
users_raw = get_company_IDs()
users = [u[0] for u in users_raw]
passwords = [get_company(u)[0][2] for u in users]

# the overarching function that directs the user to each specific page
def navigation():
    # check for the user status (logged in, sign up, no user logged in)
    if logged_in[0] == 0: # if no user logged in
        username = st.text_input("Username: ")
        entered_pass = st.text_input("New Password: ", type="password")
        but1 = st.button("Login")
        but2 = st.button("Sign Up")
        # check for password
        if but1:
            if username in users:
                user_i = users.index(username)
                password = passwords[user_i]
                if password == entered_pass:
                    st.write("Login Successful..")
                    with open("vars.txt", "w") as f2:
                        f2.writelines(f'{1}\n{username}')
                    st.experimental_rerun()
                else:
                    st.write("..Wrong Password..")
            else:
                st.write("User not found!")
        if but2:
            with open("vars.txt", "w") as f2:
                f2.writelines(f'{3}\n{"blabla"}')
            st.experimental_rerun()
    elif logged_in[0] == 3: # if the user doesn't exist
        comp_ID = st.text_input("New username(comp_ID): ")
        comp_name = st.text_input("Company Name: ")
        comp_pass = st.text_input("New Password: ", type="password")
        website = st.text_input("Company Website: ")
        but2 = st.button("Sign Up")
        if but2:
            with open("vars.txt", "w") as f2:
                f2.writelines(f'{1}\n{comp_ID}')
            add_company(comp_ID, comp_name, comp_pass, website)
            st.experimental_rerun()
    elif logged_in[0] == 1: # if the user is already signed in
        st.set_page_config(layout="wide", page_title='Interview-Analysis')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        utl.inject_custom_css()
        utl.navbar_component(logged_in[1])
        utl.hide_row_index_css()

        # direct the user to the desired page
        route = utl.get_current_route()
        if route == "home":
            home.load_view()
        elif route == "data_mng":
            data_mng.load_view(logged_in[1])
        elif route == "analysis":
            analysis.load_view(logged_in[1])
        elif route == "reports":
            reports.load_view(logged_in[1])
        elif route == "logout":
            with open("vars.txt", "w") as f2:
                f2.writelines(f'{0}\n{"blabla"}')
            js = "window.location.href = 'http://localhost:8501/'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
            
        elif route == None:
            home.load_view()


def my_exit_function():
    with open("vars.txt", "w") as f2:
        f2.writelines(f'{0}\n{"NONE"}')


if __name__ == '__main__':
    atexit.register(my_exit_function, )
    navigation()

