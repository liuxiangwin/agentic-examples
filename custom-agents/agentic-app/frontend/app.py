import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8080"  # Update if deployed elsewhere

### ✅ Function to Fetch Enabled Tools
def get_enabled_tools():
    """Fetch the list of enabled tools from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/tools")
        if response.status_code == 200:
            return response.json().get("tools", [])
        return ["Failed to fetch tools"]
    except Exception as e:
        return [f"Error: {e}"]

### ✅ Streamlit UI Setup
st.set_page_config(page_title="Agentic App", layout="wide")

st.title("🤖 Agentic App Frontend")

# Sidebar for Tools Display
with st.sidebar:
    st.subheader("🔧 Enabled Tools")
    tools = get_enabled_tools()
    
    if tools:
        for tool in tools:
            st.write(f"✅ {tool}")
    else:
        st.write("⚠️ No tools available")

# User Query Input
st.subheader("💬 Chat with Agent")
user_query = st.text_input("Enter your query:", key="user_input")

if st.button("Ask"):
    if user_query.strip():
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ask", json={"query": user_query}
                ).json()
                
                agent_response = response.get("response", "No response")
                
                # Display the response
                st.subheader("🤖 Agent Response")
                st.markdown(agent_response)

            except Exception as e:
                st.error(f"Error contacting the backend: {e}")
    else:
        st.warning("Please enter a query before asking.")

