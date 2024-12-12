import streamlit as st
import requests
from utils import enable_chat_history, display_msg, StreamHandler

# Replace 'http://localhost:8000' with your actual FastAPI URL
FASTAPI_URL = "http://127.0.0.1:8000"


def submit_task(task_description):
    """Function to submit the task description to the FastAPI backend using GET request."""
    url = f"{FASTAPI_URL}/run/essay"

    # Send GET request to the FastAPI backend with query parameters
    params = {"task_description": task_description}

    response = requests.get(url, params=params)

    # Return the response data in JSON format
    return response.json()


@enable_chat_history
def main():
    """Main function to create Streamlit interface."""
    st.title("Essay Composer Frontend")

    # Display initial assistant message
    display_msg(
        "Hello! I'm here to help you compose essays. Please enter a task description.",
        "assistant",
    )

    # Input section for the task description
    with st.form(key="task_form"):
        task_description = st.text_input("Enter task description:")

        submit_button = st.form_submit_button(label="Submit Task")

    if submit_button:
        if task_description:
            # Display user message
            display_msg(f"Task Description: {task_description}", "user")

            # Call the FastAPI backend to run the essay composition task
            result = submit_task(task_description)

            # Check if the result is a dictionary (expected format)
            if isinstance(result, dict):
                # Handle case where the backend returns a JSON response
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Display the essay result from FastAPI
                    essay = result.get("essay", "No essay generated.")
                    st.success(f"Essay Generated: {essay}")
                    display_msg(f"Essay Generated: {essay}", "assistant")
            else:
                # Handle case where the result is a string (unexpected but valid response)
                st.success(f"Essay Generated: {result}")
                display_msg(f"Essay Generated: {result}", "assistant")
        else:
            st.error("Task description cannot be empty!")


if __name__ == "__main__":
    main()
