import requests
import os
from pydantic import BaseModel

API_KEY = os.getenv("OPENROUTER_API_KEY")

class InterviewInput(BaseModel):
    role: str
    skills: str
    answer: str | None = None

def run_agent(data: InterviewInput):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Interview Agent"
    }

    # Decide mode: generate questions OR evaluate answer
    if not data.answer or data.answer.strip() == "":
        # Generate questions
        user_prompt = f"""
Generate 3 technical interview questions for a fresher applying for the role of {data.role}
with skills {data.skills}.
"""
    else:
        # Evaluate answer
        user_prompt = f"""
You are an interview evaluator.

Role: {data.role}
Skills: {data.skills}
Candidate Answer: {data.answer}

Please evaluate the answer based on:
- Technical correctness
- Clarity
- Depth of explanation

Give:
1. Score out of 10
2. Feedback
3. Suggestions for improvement
"""

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    result = response.json()

    return result["choices"][0]["message"]["content"]
