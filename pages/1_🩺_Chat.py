import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from dotenv import load_dotenv
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.memory.types import DEFAULT_CHAT_STORE_KEY
from src.global_settings import DEFAULT_GEMINI_MODEL, DEFAULT_GEMINI_EMBEDDING, DEFAULT_OPENAI_MODEL, CONVERSATION_FILE
from src.prompts import CUSTORM_AGENT_SYSTEM_TEMPLATE
from src.conversation_engine import load_chat_store, initialize_chatbot, chat_inference
from src.gemini import Gemini
load_dotenv()

# Settings.llm = Gemini(model=DEFAULT_GEMINI_MODEL, system_instruction=CUSTORM_AGENT_SYSTEM_TEMPLATE)
Settings.llm = OpenAI(model=DEFAULT_OPENAI_MODEL)
Settings.embed_model = GeminiEmbedding(model_name=DEFAULT_GEMINI_EMBEDDING)

st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠")

def main():
    st.header("Mental Health Counselling Chatbot 🩺")
    chat_store = load_chat_store()
    container = st.container()
    agent = initialize_chatbot(chat_store, container)
    chat_inference(agent, chat_store, container)
    if st.button("Clear chat"):
        chat_store.delete_messages(key=DEFAULT_CHAT_STORE_KEY)
        with open(CONVERSATION_FILE, "w") as f:
            f.truncate()
        st.rerun()

if __name__ == "__main__":
    main()