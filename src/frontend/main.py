import streamlit as st
import requests
from typing import Dict, Any
from utils import enable_chat_history, display_msg, StreamHandler


FASTAPI_URL = "http://127.0.0.1:8000"


def configure_model() -> str:
    """Function to configure the model parameters"""
    st.sidebar.header("Model Configuration")
    models = ["ollama", "xai"]
    model = st.sidebar.selectbox(label="LLM Provider:", options=models, index=0)
    return model


def submit_task(task_description: str, llm: str) -> Dict[str, Any]:
    """Function to submit the task description to the FastAPI backend using GET request."""
    url = f"{FASTAPI_URL}/run/essay"
    params = {"task_description": task_description, "llm": llm}
    response = requests.get(url, params=params)
    return response.json()


def draw_title() -> None:
    """Function to draw the frontend title"""
    st.title("Archetype2")

    st.session_state["llm"] = configure_model()

    display_msg(
        "Hello! I'm here to help you compose essays. Please enter a task description.",
        "assistant",
    )


def draw_input() -> None:
    """Draws input forms and triggers process_input() on click"""
    with st.form(key="task_form"):
        task_description = st.text_input("Enter task description:")
        submit_button = st.form_submit_button(label="Submit Task")

    if submit_button:
        if task_description:
            process_input(task_description)
        else:
            st.error("Task description cannot be empty!")


def process_input(task_description: str) -> None:
    """Processes the input task description and displays the result"""
    with st.spinner("Processing..."):
        display_msg(f"Task Description: {task_description}", "user")
        result = submit_task(task_description, st.session_state["llm"])
        display_msg(f"{result}", "assistant")


@enable_chat_history
def main():

    draw_title()
    draw_input()


if __name__ == "__main__":
    main()
