import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime
from src.global_settings import SCORES_FILE, SUMMARY_FILE
import plotly.graph_objects as go
from llama_index.core import Settings

llm = Settings.llm

st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="wide")

def main():
    st.header("Mental Health Score Analysis 📈")
    st.markdown("This page displays the mental health scores and detailed information.")

    st.markdown("## Mental Health Scores")
    info = """
    The mental health score is a numerical representation of the user's mental health.
    The score ranges from 1 to 5, where:
    - 1: Very poor
    - 2: Poor
    - 3: Average
    - 4: Good
    - 5: Excellent
    """
    st.info(info, icon="ℹ️")
    if os.path.exists(SCORES_FILE) and os.path.getsize(SCORES_FILE) > 0:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
        df = pd.DataFrame(scores)
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "time": st.column_config.DatetimeColumn("Time"),
                "advice": st.column_config.TextColumn("Advice"),
                "score": st.column_config.NumberColumn("Score"),
                "content": st.column_config.TextColumn("Content"),
            }
        )

        st.markdown("## Mental Health Score Statistics through Time")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["score"], mode="lines+markers"))
        fig.update_layout(title="Mental Health Score through Time", xaxis_title="Time", yaxis_title="Score")
        st.plotly_chart(fig)

        st.markdown("## Overall")

        with open(SUMMARY_FILE, "a+") as f:
            f.seek(0)
            summary = f.read()
        if summary and (int(summary.split("\n")[0]) == len(scores)):
            summary = "\n".join(summary.split("\n")[1:])
            st.write(summary)
        else:
            print("Generating summary...")
            content = "\n".join([f"**{score['time']}**: {score['content']}" for score in scores])
            prompt = f"Summary in a short paragraph of user's mental health through time:\n{content}"
            response = llm.complete(prompt)
            summary = response.text
            st.write(summary)
            with open(SUMMARY_FILE, "w") as f:
                f.write(f"{len(scores)}\n{summary}")
    else:
        st.write("No mental health scores available.")

if __name__ == "__main__":
    main()