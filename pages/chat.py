import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from dotenv import load_dotenv
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
from src.global_settings import DEFAULT_GEMINI_MODEL, DEFAULT_GEMINI_EMBEDDING
from src.prompts import CUSTORM_AGENT_SYSTEM_TEMPLATE
from src.conversation_engine import load_chat_store, initialize_chatbot, chat_inference
from src.gemini import Gemini
load_dotenv()

Settings.llm = Gemini(model=DEFAULT_GEMINI_MODEL, system_instruction=CUSTORM_AGENT_SYSTEM_TEMPLATE)
Settings.embed_model = GeminiEmbedding(model_name=DEFAULT_GEMINI_EMBEDDING)

def main():
    st.header("Mental Health Chatbot")
    chat_store = load_chat_store()
    container = st.container()
    agent = initialize_chatbot(chat_store, container)
    # print(agent.agent_worker._react_chat_formatter)
    chat_inference(agent, chat_store, container)
    # print(agent.chat_history)

if __name__ == "__main__":
    main()