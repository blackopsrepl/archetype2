import streamlit as st
import requests

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


def main():
    """Main function to create Streamlit interface."""
    st.title("Essay Composer Frontend")

    # Input section for the task description
    with st.form(key="task_form"):
        task_description = st.text_input("Enter task description:")

        submit_button = st.form_submit_button(label="Submit Task")

    if submit_button:
        if task_description:
            # Call the FastAPI backend to run the essay composition task
            result = submit_task(task_description)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Essay Generated: {result}")
        else:
            st.error("Task description cannot be empty!")


if __name__ == "__main__":
    main()
