import streamlit as st


def configure_model() -> str:
    """Function to configure the model parameters"""
    st.sidebar.header("Model Configuration")
    models = ["ollama", "xai"]
    model = st.sidebar.selectbox(label="LLM Provider:", options=models, index=0)
    return model


def configure_archetype() -> str:
    """Function to configure the model parameters"""
    st.sidebar.header("Archetype Configuration")
    archetypes = ["essay", "task"]
    archetype = st.sidebar.selectbox(label="Archetype:", options=archetypes, index=0)
    return archetype
