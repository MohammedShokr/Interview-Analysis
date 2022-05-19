import streamlit as st
import utils as utl
from views import home, data_mng, analysis, reports, options, configuration
from database_functions import *

#create_tables()
#print(view_schema())


# ### css ###
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


############

logged_in = [0, ""]
with open("vars.txt", "r") as f:
    cache = f.readlines()
    if cache:
        logged_in[0] = int(cache[0])
        logged_in[1] = cache[1]


users_raw = []
with open("users.txt", "r") as f1:
    users_raw = f1.readlines()
users = [usr.split('-')[0].strip() for usr in users_raw]
passwords = [usr.split('-')[1].strip() for usr in users_raw]


def navigation():
    if logged_in[0] == 0:
        username = st.text_input("Username: ")
        entered_pass = st.text_input("Password: ")
        but1 = st.button("Login")
        but2 = st.button("Sign Up")
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
    elif logged_in[0] == 3:
        username = st.text_input("New username: ")
        entered_pass = st.text_input("New Password: ")
        but2 = st.button("Sign Up")
        if but2:
            with open("vars.txt", "w") as f2:
                f2.writelines(f'{1}\n{username}')
            with open("users.txt", "a") as f3:
                f3.writelines(f'{username}-{entered_pass}\n')
            st.experimental_rerun()
    elif logged_in[0] == 1:
        st.set_page_config(layout="wide", page_title='Interview-Analysis')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        utl.inject_custom_css()
        utl.navbar_component(logged_in[1])
        utl.hide_row_index_css()

        ### CSS
        local_css("styles.css")

        ####

        col1, col2, col3 = st.columns((10,2,1))
        but3 = col3.button("Logout")
        if but3:
            with open("vars.txt", "w") as f2:
                f2.writelines(f'{0}\n{"blabla"}')
            st.experimental_rerun()

        route = utl.get_current_route()
        if route == "home":
            home.load_view()
        elif route == "data_mng":
            data_mng.load_view(logged_in[1])
        elif route == "analysis":
            analysis.load_view(logged_in[1])
        elif route == "reports":
            reports.load_view(logged_in[1])
        elif route == "options":
            options.load_view()
        elif route == "configuration":
            configuration.load_view()
        elif route == None:
            home.load_view()


navigation()

