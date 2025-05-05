"""
LangChain agent implementation for BigQuery interaction.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine # Import create_engine

# Load .env here as well, in case of import timing issues
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Fallback if agent.py is run standalone or .env isn't found
    load_dotenv() 

from langchain_google_vertexai import VertexAI
# Use the community toolkit for SQL agents
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentExecutor # AgentExecutor is still used
from langchain_community.utilities import SQLDatabase # Needed for BigQuery connection via SQLAlchemy

# Initialize LLM
# Ensure GOOGLE_CLOUD_PROJECT is set in your environment or .env file
llm = VertexAI(
    model_name="gemini-2.0-flash-lite-001", # Try the suggested flash-lite model
    location="us-east1" # Explicitly set location
)

# Create BigQuery Agent
# Requires GOOGLE_CLOUD_PROJECT environment variable to be set
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# Specify dataset if needed
dataset = os.getenv("BIGQUERY_DATASET") # Optional: Load dataset from env or hardcode
# table_names = ["your_table1", "your_table2"] # Optional: Specify tables

# Construct the BigQuery SQLAlchemy URI
# Ensure you have sqlalchemy-bigquery installed (`pip install sqlalchemy-bigquery`)

# Option 1: Using default credentials (gcloud auth application-default login)
bigquery_uri = f"bigquery://{project_id}/{dataset if dataset else ''}"

# Option 2: Using a service account key file (if GOOGLE_APPLICATION_CREDENTIALS is set)
# service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# if service_account_path:
#     bigquery_uri = f"bigquery://{project_id}/{dataset if dataset else ''}?credentials_path={service_account_path}"
# else:
#     bigquery_uri = f"bigquery://{project_id}/{dataset if dataset else ''}"

# Create SQLAlchemy engine explicitly
# This ensures sqlalchemy-bigquery dialect is picked up if installed
engine = create_engine(bigquery_uri)

# Create SQLDatabase instance using the explicit engine
db = SQLDatabase(engine)

# Create the SQL agent using the community toolkit
agent_executor: AgentExecutor = create_sql_agent(
    llm=llm,
    db=db, # Pass the SQLDatabase instance
    agent_type="zero-shot-react-description", # Use the Zero Shot ReAct agent type
    verbose=True,
    handle_parsing_errors=True # Add error handling for LLM output parsing
    # Note: create_sql_agent doesn't directly take project_id/dataset/table_names
    # Scope is controlled by the SQLDatabase instance
)

async def get_agent_response(user_message: str) -> str:
    """Gets a response from the LangChain agent for the given user message asynchronously."""
    if agent_executor is None:
        return "Agent not initialized." # Should not happen with current structure

    try:
        # Use ainvoke for asynchronous execution compatible with FastAPI
        # The input format might need adjustment depending on the agent_type
        response = await agent_executor.ainvoke({"input": user_message})
        return response.get("output", "Agent did not provide an output.")
    except Exception as e:
        print(f"Error invoking agent: {e}")
        # Consider logging the error details
        return "Sorry, I encountered an error trying to process your request." 