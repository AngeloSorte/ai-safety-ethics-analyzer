from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from groq import Groq

app = FastAPI()

# ✅ CORS FIX (OBBLIGATORIO per Wix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in produzione si può restringere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ GROQ CLIENT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================
# INPUT MODEL
# =========================
class InputData(BaseModel):
    content: str
    mode: str = "text"


# =========================
# API ENDPOINT
# =========================
@app.post("/analyze")
def analyze(data: InputData):

    prompt = f"""
You are an AI Safety & Ethics Analyzer.

Return ONLY valid JSON. No markdown. No extra text.

Schema:
{{
  "risk_level": "LOW | MEDIUM | HIGH",
  "score": 0,
  "summary": "",
  "issues": [],
  "improvements": []
}}

Analyze the input below.

TYPE: {data.mode}

CONTENT:
{data.content}

Evaluate:
- privacy risks
- bias
- security risks
- misuse potential
- ethical concerns

Be strict, consistent, and deterministic.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a strict AI safety evaluator that outputs only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content

        # 🔥 JSON CLEANING (important per evitare crash)
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
