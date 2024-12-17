import streamlit as st
import requests
from typing import Dict, Callable, Any

from src.frontend.utils.messages import display_msg
from src.frontend.utils.markdown_analyzer import MarkdownAnalyzer
from src.frontend.sidebar import configure_model, configure_archetype
from src.frontend.config import FASTAPI_URL


def draw_title() -> None:
    """Function to draw the frontend title"""
    st.title("Archetype2")

    st.session_state["llm"] = configure_model()

    st.session_state["archetype"] = configure_archetype()

    display_msg(
        "Hello! Please select the desired archetype from the left sidebar.",
        "assistant",
    )


def generate_input_form(archetype: str) -> Callable[[None], None]:
    def draw_input_form() -> None:
        """Draws input forms and triggers process_input() on click"""

        match st.session_state["archetype"]:

            case "essay" | "task":
                with st.form(key="task_form"):
                    task_description = st.text_input("Enter task description:")
                    submit_button = st.form_submit_button(label="Submit Task")

                if submit_button:
                    if task_description:
                        process_input(task_description)
                    else:
                        st.error("Task description cannot be empty!")

            case _:
                raise ValueError("Invalid archetype")

    return draw_input_form


def unwrap_tasks_from_generated(result: list) -> list:
    tasks = []
    if isinstance(result, list):
        # We expect result to be a list of lists, with only one entry
        if isinstance(result[0], list):
            # Unwrap the inner list of dictionaries
            for task in result[0]:
                if isinstance(task, dict) and "text" in task:
                    tasks.append(task["text"])
                else:
                    print(f"Unexpected task format: {task}")
        else:
            print("Error: The first element of the result is not a list!")
    else:
        print("Error: 'Unordered list' is not a list!")

    return tasks


def generate_task(archetype: str) -> Callable[[None], None]:
    def submit_task(task_description: str, llm: str) -> Dict[str, Any]:
        """Function to submit the task description to the FastAPI backend using GET request."""

        match st.session_state["archetype"]:

            case "essay":
                url = f"{FASTAPI_URL}/run/essay"
                params = {"task_description": task_description, "llm": llm}
                response = requests.get(url, params=params)
                return response.json()

            case "task":
                url = f"{FASTAPI_URL}/run/task"
                params = {"task_description": task_description, "llm": llm}
                response = requests.get(url, params=params)
                analyzer = MarkdownAnalyzer(response.json())
                result = analyzer.identify_lists()["Unordered list"]
                # return unwrap_tasks_from_generated(result)
                result = unwrap_tasks_from_generated(result)
                display_msg(f"{result}", "assistant")
                url = f"{FASTAPI_URL}/run/evaluate"
                merged_tasks = []
                for task in result:
                    params = {"task_description": task, "llm": llm}
                    response = requests.get(url, params=params)
                    merged_tasks.append((task, response.json()))
                return merged_tasks

    return submit_task


def process_input(task_description: str) -> None:
    """Processes the input task description and displays the result"""
    with st.spinner("Processing..."):
        display_msg(f"Task Description: {task_description}", "user")
        submit_task = generate_task(st.session_state["archetype"])
        result = submit_task(task_description, st.session_state["llm"])
        display_msg(f"{result}", "assistant")


def main():

    draw_title()
    draw_input_form = generate_input_form(st.session_state["archetype"])
    draw_input_form()


if __name__ == "__main__":
    main()
