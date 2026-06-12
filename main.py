from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class InputData(BaseModel):
    content: str
    mode: str = "text"


@app.get("/")
def home():
    return {"status": "online"}


@app.post("/analyze")
def analyze(data: InputData):

    prompt = f"""
You are an AI Safety and Ethics Analyzer.

Analyze the following content.

Input type:
{data.mode}

Content:
{data.content}

Evaluate:

- privacy risks
- security risks
- bias risks
- misuse potential
- transparency issues

Return ONLY valid JSON.

{{
  "risk_level": "LOW",
  "score": 25,
  "summary": "Short explanation",
  "issues": ["issue1", "issue2"],
  "improvements": ["improvement1", "improvement2"]
}}
"""

    try:

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            },
            timeout=60
        )

        result = response.json()

        text = result["candidates"][0]["content"]["parts"][0]["text"]

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception as e:

        return {
            "risk_level": "ERROR",
            "score": 0,
            "summary": str(e),
            "issues": [],
            "improvements": []
        }
