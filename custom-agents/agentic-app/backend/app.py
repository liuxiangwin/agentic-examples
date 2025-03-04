### FastAPI LangGraph Agent ###

# Import required libraries
import os
import logging
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# LangChain and LangGraph imports
from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
import yfinance as yf

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging to track tool usage
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Environment Variables
INFERENCE_SERVER_URL = os.getenv("API_URL_GRANITE")  # Granite AI Server URL
MODEL_NAME = "granite-3-8b-instruct"  # Model name for LLM
API_KEY = os.getenv("API_KEY_GRANITE")  # API Key for authentication

# Read debug mode from environment variable (default: False)
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Initialize LLM with Granite AI settings
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

### Define Tools ###
# Define Python REPL tool for executing Python code
repl = PythonREPL()

@tool
def python_repl(code: str):
    """Execute Python code and return the output."""
    logging.info(f"Using tool: Python REPL | Code: {code}")
    try:
        result = repl.run(code)
    except BaseException as e:
        logging.error(f"Python REPL execution failed: {repr(e)}")
        return f"Failed to execute. Error: {repr(e)}"
    
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."

# Define yfinance helper tool for stock prices
@tool
def get_stock_price(ticker: str):
    """Fetch the latest stock price for a given ticker symbol using yfinance."""
    logging.info(f"Using tool: YFinance | Ticker: {ticker}")
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return f"The latest closing price of {ticker} is **${price:.2f}**."
    except Exception as e:
        logging.error(f"YFinance tool failed: {repr(e)}")
        return f"Failed to retrieve stock price for {ticker}. Error: {repr(e)}"

# Define tools list with logging
duckduckgo_search = DuckDuckGoSearchRun()

tools = [duckduckgo_search, python_repl, get_stock_price]

### LangGraph REACT Agent ###
# Create LangGraph REACT agent with integrated tools
graph = create_react_agent(llm, tools=tools, debug=DEBUG_MODE)

# Request Model for API calls
class QueryRequest(BaseModel):
    query: str

# Response Model for API responses
class QueryResponse(BaseModel):
    response: str

### FastAPI Endpoints ###
@app.get("/health")
def read_health():
    """Health check endpoint to verify the API is running."""
    return {"message": "Status:OK"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """Handles user queries using the LangGraph REACT agent."""
    logging.info(f"Received user query: {request.query}")

    inputs = {"messages": [("user", request.query)]}
    tool_responses = []
    final_response = ""

    # Stream responses from LangGraph
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]

        # Collect tool responses separately
        if "<tool_call>" in str(message):
            tool_responses.append(str(message))

        # Collect final response separately
        elif isinstance(message, tuple):
            final_response = str(message[1])
        else:
            final_response = str(message.content)

    # Structure the response properly
    structured_response = "\n\n".join(tool_responses) + "\n\n" + final_response.strip()
    
    logging.info(f"Agent response: {structured_response}")
    return {"response": structured_response}

### Launch the FastAPI server ###
if __name__ == "__main__":
    port = int(os.getenv('PORT', '8080'))  # Default to port 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
