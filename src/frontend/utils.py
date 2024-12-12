import os
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler


def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        ### clears chat history cache ###
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        ### prints chat history ###
        if "messages" not in st.session_state:
            if st.session_state["LANGUAGE"] == "en":
                st.session_state["messages"] = [
                    {
                        "role": "assistant",
                        "content": "Hello, I am Clio, your personal task management assistant. How can I help you?",
                    }
                ]
            if st.session_state["LANGUAGE"] == "it":
                st.session_state["messages"] = [
                    {
                        "role": "assistant",
                        "content": "Ciao, sono Clio, la tua assistente personale per la gestione delle attività. Come posso aiutarti?",
                    }
                ]

        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)

    return execute


def display_msg(msg, author):
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)
