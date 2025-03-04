import streamlit as st
import requests
import os

# Define FastAPI Backend URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8080")

# Set up Streamlit app
st.set_page_config(page_title="Agentic App Frontend", page_icon="🤖")
st.title("🤖 Agentic App Frontend")
st.write("Ask me anything, and I will retrieve the answer from the Agentic API!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
if "input_disabled" not in st.session_state:
    st.session_state["input_disabled"] = False

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
user_input = st.chat_input(disabled=st.session_state["input_disabled"])
if user_input:
    st.session_state["input_disabled"] = True  # Disable input while processing
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    # Send request to FastAPI backend
    response = {"response": "Error: Unable to connect to FastAPI server"}
    try:
        api_response = requests.post(f"{FASTAPI_URL}/ask", json={"query": user_input}, timeout=10)
        if api_response.status_code == 200:
            response = api_response.json()
        else:
            response = {"response": f"Error: Received status code {api_response.status_code}"}
    except Exception as e:
        response = {"response": f"Error: {str(e)}"}

    # Display API response
    assistant_response = response.get("response", "Error retrieving response")
    st.chat_message("assistant").markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    st.session_state["input_disabled"] = False  # Re-enable input
    st.rerun()
