import os, re, logging
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI

# Create OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()
conversation_store: dict[str, list[dict]] = {}

SYSTEM_RE = re.compile(r"^\s*(system:|assistant:)", re.I)

class ChatReq(BaseModel):
    user_id: str
    content: str

def validate(text: str):
    if SYSTEM_RE.match(text):
        raise HTTPException(400, "Restricted role tokens are not allowed.")

@app.post("/chat")
async def chat(req: ChatReq = Body(...)):
    validate(req.content)
    thread = conversation_store.setdefault(req.user_id, [])
    thread.append({"role": "user", "content": req.content})

    messages = (
        [{"role": "system", "content": "You are a helpful customer support assistant for Acme Inc. Keep answers professional, friendly, and concise."}]
        + thread
    )
    resp = await client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    answer = resp.choices[0].message.content
    thread.append({"role": "assistant", "content": answer})
    logging.info("DEFENCE snapshot %s len=%d", req.user_id, len(thread))
    return {"answer": answer} 