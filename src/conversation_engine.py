import os
import json
import time
from datetime import datetime
import streamlit as st
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import load_index_from_storage, StorageContext, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory.types import DEFAULT_CHAT_STORE_KEY
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from src.global_settings import INDEX_STORAGE, CONVERSATION_FILE, SCORES_FILE, PINECONE_INDEX_NAME
from src.global_settings import DEFAULT_GEMINI_MODEL, DEFAULT_OPENAI_MODEL
from src.prompts import (CUSTORM_AGENT_SYSTEM_TEMPLATE,
                         QA_PROMPT_TEMPLATE,
                         TEXT_QA_TEMPLATE,
                         AGENT_WORKER_PROMPT_TEMPLATE_VI,
                         AGENT_WORKER_PROMPT_TEMPLATE_EN,
                         AGENT_WORKER_PROMPT_TEMPLATE_TEST
                         )
from src.gemini import Gemini

# query_llm = Gemini(model=DEFAULT_GEMINI_MODEL)
# gemini_agent_llm = Gemini(model=DEFAULT_GEMINI_MODEL, system_instruction=CUSTORM_AGENT_SYSTEM_TEMPLATE)
# openai_agent_llm = OpenAI(model=DEFAULT_OPENAI_MODEL)

# Utility functions
def load_chat_store():
    """Loads or initializes the chat store."""
    if os.path.exists(CONVERSATION_FILE) and os.path.getsize(CONVERSATION_FILE) > 0:
        try:
            return SimpleChatStore.from_persist_path(CONVERSATION_FILE)
        except json.JSONDecodeError:
            return SimpleChatStore()
    return SimpleChatStore()

def save_score(full_advice: str, score: int, content: str):
    """
    Saves a mental health score and details to a file.

    Args:
        - full_advice (str): The full advice for the user.
        - score (int): The mental health score.
            1: Very poor, 2: Poor, 3: Average, 4: Good, 5: Excellent
        - content (str): The detailed mental health information. 
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "time": current_time,
        "advice": full_advice,
        "score": score,
        "content": content,
    }

    # Read existing data
    data = []
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass

    # Append new data
    data.append(new_entry)
    with open(SCORES_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return full_advice

# Chat functions
def display_messages(chat_store, container):
    """Displays chat messages from the chat store."""
    with container:
        for message in chat_store.get_messages(key=DEFAULT_CHAT_STORE_KEY):
            avatar = "🧑🏻" if message.role == "user" else "🧑🏻‍⚕️"
            if message.content:
                with st.chat_message(message.role, avatar=avatar):
                    st.markdown(message.content)

def initialize_chatbot(chat_store=None, container=None, system_prompt=CUSTORM_AGENT_SYSTEM_TEMPLATE, evaluate=False):
    """Initializes the chatbot agent."""
    # Memory
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000,
        chat_store=chat_store
    )
    
    pc = Pinecone()
    pinecone_index = pc.Index(PINECONE_INDEX_NAME)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # Initialize the query engine tools
    mental_health_query_engine = index.as_query_engine(similarity_top_k=3,
                                                    #    llm=query_llm
                                                       )
    mental_health_query_engine.update_prompts({"response_synthesizer:text_qa_template": PromptTemplate(TEXT_QA_TEMPLATE)})

    mental_health_tool = QueryEngineTool(
        query_engine=mental_health_query_engine,
        metadata=ToolMetadata(
            name="MentalHealth",
            description=("Công cụ này sẽ trả lời các câu hỏi về sức khỏe tâm thần dựa trên chuẩn DSM5 và ICD-10."
                         "Đầu vào của công cụ này là một câu hỏi về sức khỏe tâm thần, và đầu ra là câu trả lời chi tiết về câu hỏi đó.")
        )
    )

    # Initialize the save score tool
    save_score_tool = FunctionTool.from_defaults(
        fn=save_score,
        name="SaveScore",
    )

    # Initialize the agent
    # agent = ReActAgent.from_tools(
    #     tools=[mental_health_tool, save_score_tool],
    #     # llm=gemini_agent_llm,
    #     memory=memory,
    #     verbose=True,
    #     # context=system_prompt
    # )

    agent = OpenAIAgent.from_tools(
        tools=[mental_health_tool, save_score_tool] if not evaluate else [mental_health_tool],
        # llm=openai_agent_llm,
        memory=memory,
        system_prompt=system_prompt,
        verbose=True
    )
 
    # agent.update_prompts({"agent_worker:system_prompt": PromptTemplate(AGENT_WORKER_PROMPT_TEMPLATE_EN)})

    # Display chat messages
    if not evaluate:
        display_messages(chat_store, container)
    return agent

def stream_data(response):
    for word in response.response.split(" "):
        yield word + " "
        time.sleep(0.05)

def chat_inference(agent, chat_store, container):
    """Performs chat inference with the agent."""
    # Display welcome message
    if not os.path.exists(CONVERSATION_FILE) or os.path.getsize(CONVERSATION_FILE) == 0:
        with container:
            with st.chat_message(name="assistant", avatar="🧑🏻‍⚕️"):
                st.markdown("Chào bạn! Mình là chuyên gia tâm lý AI, mình sẽ giúp bạn theo dõi và tư vấn về sức khỏe tâm thần theo từng ngày. Hãy nói chuyện với mình như một người bạn để tạo cảm giác thoải mái nhất nhé!")

    # Get user input
    prompt = st.chat_input("Nhập tin nhắn của bạn...")
    if prompt:
        with container:
            with st.chat_message(name="user", avatar="🧑🏻"):
                st.markdown(prompt)
            response = agent.chat(prompt)
            with st.chat_message(name="assistant", avatar="🧑🏻‍⚕️"):
                st.write_stream(stream_data(response))
        chat_store.persist(CONVERSATION_FILE)