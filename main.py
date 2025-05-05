from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Implement agent logic in agent.py
from agent import get_agent_response

# Explicitly load .env file from the current directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI(
    title="BigQuery Chat Agent",
    description="An API for chatting with an LLM agent connected to BigQuery.",
    version="0.1.0",
)

class ChatRequest(BaseModel):
    message: str
    # Optional: Add session_id for conversation history later
    # session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a user message and returns the agent's response.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Call the actual agent function
    agent_reply = await get_agent_response(request.message)
    # agent_reply = f"Agent received: {request.message}" # Dummy response

    return ChatResponse(reply=agent_reply)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 