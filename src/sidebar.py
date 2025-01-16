import streamlit as st

def show_sidebar():
    st.sidebar.markdown("## About us")
    info = """\
    This project serves for coursework Introduction to Statistic Linguistics and Application at University of Science, VNU-HCM.
    The project aims to provide mental health counselling services to users. You can interact with the chatbot to discuss your mental health concerns or analyze your mental health score.

    The project is developed by:
    - 21120554: Lê Văn Tấn
    - 21120527: Nguyễn Thế Phong
    - 18120445: Hoàng Nguyễn Hải Long
    """
    st.sidebar.write(info)