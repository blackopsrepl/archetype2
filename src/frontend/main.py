import streamlit as st
import requests
from typing import Dict, Any
from utils import enable_chat_history, display_msg, StreamHandler

# Replace 'http://localhost:8000' with your actual FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000"


def submit_task(task_description) -> Dict[str, Any]:
    """Function to submit the task description to the FastAPI backend using GET request."""
    url = f"{FASTAPI_URL}/run/essay"
    params = {"task_description": task_description}
    response = requests.get(url, params=params)
    return response.json()


def draw_title() -> None:
    st.title("Essay Composer Frontend")

    display_msg(
        "Hello! I'm here to help you compose essays. Please enter a task description.",
        "assistant",
    )


def draw_input() -> None:
    with st.form(key="task_form"):
        task_description = st.text_input("Enter task description:")
        submit_button = st.form_submit_button(label="Submit Task")

    if submit_button:
        if task_description:
            process_input(task_description)
        else:
            st.error("Task description cannot be empty!")


def process_input(task_description) -> None:
    display_msg(f"Task Description: {task_description}", "user")
    result = submit_task(task_description)
    display_msg(f"{result}", "assistant")


@enable_chat_history
def main():

    draw_title()

    draw_input()


if __name__ == "__main__":
    main()
