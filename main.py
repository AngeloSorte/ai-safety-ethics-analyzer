from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import json

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class InputData(BaseModel):
    content: str
    mode: str = "text"


@app.post("/analyze")
def analyze(data: InputData):

    prompt = f"""
You are an AI Safety and Ethics Analyzer.

Analyze the input and return ONLY valid JSON.

Input type: {data.mode}

Content:
{data.content}

Evaluate:
- privacy risks
- bias risks
- security risks
- misuse potential
- transparency issues

Return ONLY this JSON format:

{{
  "risk_level": "LOW | MEDIUM | HIGH",
  "score": 0,
  "summary": "",
  "issues": [],
  "improvements": []
}}
"""

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
    )

    try:
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)

    except Exception:
        return {
            "risk_level": "ERROR",
            "score": 0,
            "summary": "Failed to parse AI response",
            "issues": [],
            "improvements": []
        }