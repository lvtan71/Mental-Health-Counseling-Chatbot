import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
from src.conversation_engine import initialize_chatbot
from src.prompts import EVALUATE_AGENT_SYSTEM_TEMPLATE
from src.global_settings import DEFAULT_OPENAI_MODEL, DEFAULT_GEMINI_EMBEDDING, EVALUATE_DATA

Settings.llm = OpenAI(model=DEFAULT_OPENAI_MODEL)
Settings.embed_model = GeminiEmbedding(model_name=DEFAULT_GEMINI_EMBEDDING)

def main():
    # Load the evaluation data
    data = pd.read_json(EVALUATE_DATA)

    # Initialize the chatbot
    agent = initialize_chatbot(system_prompt=EVALUATE_AGENT_SYSTEM_TEMPLATE, evaluate=True)

    # Generate answers
    data['answer'] = None
    # data['answer'] = data['query'].apply(lambda x: agent.chat(x).response)
    for idx, row in enumerate(data.iterrows()):
        query = row[1]['query']
        response = agent.chat(query).response
        # Reset the memory after each query
        agent.memory.reset()
        data.at[idx, 'answer'] = response
        # print(f"Query: {query}")
        # print(f"Answer: {response}")
        print("-"*100)
    
    # Save the answers
    data.to_csv(f"results_{Settings.llm.__class__.__name__}.csv", index=False)

if __name__ == "__main__":
    main()