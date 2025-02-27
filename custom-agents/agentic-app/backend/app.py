import os
import json
import getpass
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import uvicorn

load_dotenv()

# Environment Variables
INFERENCE_SERVER_URL = os.getenv("API_URL_GRANITE")
MODEL_NAME = "granite-3-8b-instruct"
API_KEY = os.getenv("API_KEY_GRANITE")

# Initialize LLM
llm = ChatOpenAI(
    openai_api_key=API_KEY,
    openai_api_base=f"{INFERENCE_SERVER_URL}/v1",
    model_name=MODEL_NAME,
    top_p=0.92,
    temperature=0.01,
    max_tokens=512,
    presence_penalty=1.03,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# FastAPI App Initialization
app = FastAPI(
    title="FastAPI LangGraph Agent",
    version="1.0",
    description="An API that integrates LangGraph with Granite AI"
)

# Define Python REPL tool
repl = PythonREPL()

@tool
def python_repl(code: str):
    """Execute Python code and return the output."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."

# Define tools
duckduckgo_search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [duckduckgo_search, python_repl, wikipedia]

# Create LangGraph REACT agent
graph = create_react_agent(llm, tools=tools, debug=False)

# Request Model
class QueryRequest(BaseModel):
    query: str

# Response Model
class QueryResponse(BaseModel):
    response: str

@app.get("/health")
def read_health():
    return {"status": "healthy"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """Handles user queries using the LangGraph REACT agent."""
    inputs = {"messages": [("user", request.query)]}
    response_messages = []
    
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            response_messages.append(str(message))
        else:
            response_messages.append(str(message.content))
    
    return {"response": "\n".join(response_messages)}

# Launch the FastAPI server
if __name__ == "__main__":
    port = int(os.getenv('PORT', '8080'))
    uvicorn.run(app, host="0.0.0.0", port=port)
