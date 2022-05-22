import streamlit as st

def load_view():
    st.title('Logout page')
    with open(r"C:\Users\messi\Desktop\GP\Interview-Analysis\vars.txt", "w") as f2:
        f2.writelines(f'{0}\n{"blabla"}')
        print("file opened")
        return