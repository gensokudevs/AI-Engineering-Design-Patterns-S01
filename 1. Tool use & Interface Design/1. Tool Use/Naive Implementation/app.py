from typing import Annotated

from agent import SYSTEM_PROMPT, parse_action, run_lookup, run_refund
from anthropic import AsyncAnthropic
from auth import User, current_user
from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()
client = AsyncAnthropic()
MODEL = "claude-haiku-4.5"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user: Annotated[User, Depends(current_user)]) -> ChatResponse:
    # The user is authenticated upstream, but it never reaches the agent or the store.
    messages = [{"role": "user", "content": req.message}]
    resp = await client.messages.create(
        model=MODEL, max_tokens=1024, system=SYSTEM_PROMPT, messages=messages
    )
    text = resp.content[0].text
    action = parse_action(text)

    match action.kind:
        case "refund":
            return ChatResponse(reply=await run_refund(action))
        case "lookup":
            order = await run_lookup(action)
            followup = await client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    *messages,
                    {"role": "assistant", "content": text},
                    {"role": "user", "content": f"Order data: {order}"},
                ],
            )
            return ChatResponse(reply=followup.content[0].text)
        case _:
            return ChatResponse(reply=text)