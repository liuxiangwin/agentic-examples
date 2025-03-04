import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8080"  # Update this if deployed elsewhere

def check_api_status():
    """Check if the backend API is up and running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            return "🟢 API Status: Ready"
        return "🔴 API Status: Down"
    except Exception:
        return "🔴 API Status: Unreachable"

def get_enabled_tools():
    """Fetch the list of enabled tools from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/tools")
        if response.status_code == 200:
            return response.json().get("tools", [])
        return ["Failed to fetch tools"]
    except Exception as e:
        return [f"Error: {e}"]

def get_model_name():
    """Fetch the model name from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/config")
        if response.status_code == 200:
            return response.json().get("model_name", "Unknown Model")
        return "Failed to fetch model"
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Agentic AI App", page_icon="🤖", layout="wide")
st.title("🤖 Agentic AI App")

# Sidebar
with st.sidebar:
    # API Status
    api_status = check_api_status()
    st.subheader(api_status)

    # Model in Use
    st.subheader("📌 Model in Use")
    model_name = get_model_name()
    st.write(f"**{model_name}**")

    # Enabled Tools
    st.subheader("🔧 Enabled Tools")
    tools = get_enabled_tools()
    
    for tool in tools:
        st.write(f"✅ {tool}")

# Chat input and response display
st.subheader("💬 Ask a Question")
user_query = st.text_input("Enter your query:")
if st.button("Ask"):
    if user_query.strip():
        with st.spinner("Processing..."):
            response = requests.post(f"{BACKEND_URL}/ask", json={"query": user_query}).json()
            st.write("### 📝 Agent Response:")
            st.write(response.get("response", "No response"))
    else:
        st.warning("⚠️ Please enter a valid query.")
# Footer
st.markdown("---")
st.caption("Built with ❤️ by the Red Hat AI Business Unit")
