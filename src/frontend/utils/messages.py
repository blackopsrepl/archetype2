import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler


def display_msg(msg, author):
    # Ensure the messages list exists in session_state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)
