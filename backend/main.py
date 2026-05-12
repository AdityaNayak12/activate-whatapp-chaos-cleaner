from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
import json

from parser import clean_chat
from prompt import SUMMARY_PROMPT, QUERY_PROMPT

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in .env")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    chat_text: str

class QueryRequest(BaseModel):
    chat_text: str
    question: str
    history: list = []

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/summary")
async def summary_endpoint(req: SummaryRequest):
    cleaned = clean_chat(req.chat_text)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SUMMARY_PROMPT},
                {"role": "user", "content": cleaned}
            ],
            max_tokens=1000,
        )
        content = response.choices[0].message.content
        # Strip markdown code fences if model wraps JSON in them
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        parsed = json.loads(content)
        return {"summary": parsed, "cleaned_chat": cleaned}
    except json.JSONDecodeError:
        return HTTPException(status_code=422, detail={"error": "Invalid JSON from Groq", "raw_response": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_endpoint(req: QueryRequest):
    messages = req.history.copy() if req.history else []
    user_message = f"Here is the chat:\n{req.chat_text}\n\nQuestion: {req.question}"
    messages.append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": QUERY_PROMPT},
                *messages
            ],
            max_tokens=500,
        )
        content = response.choices[0].message.content
        return {"answer": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
