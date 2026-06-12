from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
from groq import Groq

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class InputData(BaseModel):
    content: str
    mode: str = "text"


@app.post("/analyze")
def analyze(data: InputData):

    prompt = f"""
You are an AI Safety & Ethics Analyzer.

Return ONLY valid JSON. No markdown. No explanations.

Schema:
{{
  "risk_level": "LOW | MEDIUM | HIGH",
  "score": 0,
  "summary": "",
  "issues": [],
  "improvements": []
}}

Analyze the following content:

TYPE: {data.mode}

CONTENT:
{data.content}

Focus on:
- privacy risks
- bias
- security risks
- misuse potential
- ethical concerns

Be strict and consistent.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a strict AI safety evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    text = response.choices[0].message.content

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        cleaned = text[start:end]

        return json.loads(cleaned)

    except Exception:
        return {
            "risk_level": "ERROR",
            "score": 0,
            "summary": "Failed to parse model output",
            "issues": [],
            "improvements": []
        }
