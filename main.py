from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json

app = FastAPI()

# CORS per Wix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = os.getenv("HF_TOKEN")

class InputData(BaseModel):
    content: str
    mode: str = "text"


@app.post("/analyze")
def analyze(data: InputData):

    prompt = f"""
You are an AI Safety & Ethics Analyzer.

Return ONLY valid JSON.

Schema:
{{
  "risk_level": "LOW | MEDIUM | HIGH",
  "score": 0,
  "summary": "",
  "issues": [],
  "improvements": []
}}

Analyze:

TYPE: {data.mode}
CONTENT: {data.content}

Focus on:
privacy, bias, security, misuse, ethics.
"""

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 400,
                    "temperature": 0.2
                }
            }
        )

        result = response.json()

        text = result[0]["generated_text"]

        start = text.find("{")
        end = text.rfind("}") + 1
        cleaned = text[start:end]

        return json.loads(cleaned)

    except Exception as e:
        return {
            "risk_level": "ERROR",
            "score": 0,
            "summary": str(e),
            "issues": [],
            "improvements": []
        }
