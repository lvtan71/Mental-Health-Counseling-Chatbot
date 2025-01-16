import streamlit as st
from src.sidebar import show_sidebar

st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")

def main():
    st.header("Mental Health Counselling Chatbot 🚑")
    st.markdown("Welcome to the Mental Health Chatbot! This project aims to provide mental health counselling services to users. You can interact with the chatbot to discuss your mental health concerns or analyze your mental health score.")
    col1, col2 = st.columns([3, 3])
    with col1:
        if st.button("🩺 Chatbot"):
            st.switch_page("pages/1_🩺_Chat.py")
        
    with col2:
        if st.button("📈 Mental Health Score Analysis"):
            st.switch_page("pages/2_📈_Statistics.py")

    st.image("pages/images/mentalhealth.png", use_container_width=True)

if __name__ == "__main__":
    show_sidebar()
    main()