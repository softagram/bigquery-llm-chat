import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables (optional, if backend URL needs configuration)
load_dotenv()

# --- Configuration ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080/chat")
APP_TITLE = "BigQuery Chat Agent"

# --- Streamlit App ---
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)
st.caption("Ask questions about data in BigQuery!")

# --- Initialize session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display previous messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle user input ---
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare spinner and send request to backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            response = requests.post(BACKEND_URL, json={"message": prompt})
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            agent_reply = response.json().get("reply", "Sorry, I didn't get a valid reply.")
        except requests.exceptions.RequestException as e:
            agent_reply = f"Error communicating with backend: {e}"
        except Exception as e:
            agent_reply = f"An unexpected error occurred: {e}"

        # Display agent reply and add to history
        message_placeholder.markdown(agent_reply)
        st.session_state.messages.append({"role": "assistant", "content": agent_reply}) 