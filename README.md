# AI Safety & Ethics Analyzer

AI-powered tool that analyzes text, code, and AI project descriptions for potential risks.

## Features
- Risk level classification (LOW / MEDIUM / HIGH)
- Score-based evaluation (0–100)
- Detection of:
  - Privacy risks
  - Bias risks
  - Security risks
  - Misuse potential
  - Transparency issues

## Stack
- FastAPI (backend)
- Gemini API (LLM)
- Wix (frontend)
- Render (deployment)

## API Endpoint
POST `/analyze`

### Input
{
  "content": "your text or code here",
  "mode": "text | code | project"
}

### Output
{
  "risk_level": "MEDIUM",
  "score": 65,
  "summary": "...",
  "issues": [],
  "improvements": []
}

### Goal

This project is a decision-support tool, not a legal or ethical authority.
