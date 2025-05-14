import os, uuid, logging
from fastapi import FastAPI, Body
from pydantic import BaseModel
from openai import AsyncOpenAI

# Create OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()
conversation_store: dict[str, list[dict]] = {}

class ChatReq(BaseModel):
    user_id: str
    content: str

@app.post("/chat")
async def chat(req: ChatReq = Body(...)):
    thread = conversation_store.setdefault(req.user_id, [])
    thread.append({"role": "user", "content": req.content})

    messages = (
        [{"role": "system", "content": "You are a helpful customer support assistant for Acme Inc. Keep answers professional, friendly, and concise."}]
        + thread
    )
    resp = await client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    answer = resp.choices[0].message.content
    thread.append({"role": "assistant", "content": answer})
    logging.info("VULN snapshot %s len=%d", req.user_id, len(thread))
    return {"answer": answer} 