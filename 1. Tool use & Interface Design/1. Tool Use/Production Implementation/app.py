import uuid
from typing import Annotated

from agent import AgentTurnLimitExceeded, run_agent
from auth import User, current_user  # your existing auth dependency
from context import RequestContext
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    request_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user: Annotated[User, Depends(current_user)]):
    ctx = RequestContext(user_id=user.id, request_id=str(uuid.uuid4()))
    try:
        reply = await run_agent(req.message, ctx)
    except AgentTurnLimitExceeded:
        raise HTTPException(503, "The assistant couldn't complete this request.")
    return ChatResponse(reply=reply, request_id=ctx.request_id)