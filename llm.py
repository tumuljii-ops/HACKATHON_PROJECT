import os
import requests
import json

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
URL = "https://api.groq.com/openai/v1/chat/completions"

def call_llm(prompt: str):
    if not API_KEY:
        return {"error": "GROQ_API_KEY not set"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        result = response.json()

        # 🔴 HANDLE API ERRORS FIRST
        if "error" in result:
            return {
                "error": "API Error",
                "raw": result["error"]
            }

        choices = result.get("choices", [])
        if not choices:
            return {"error": "No choices returned", "raw": result}

        message = choices[0].get("message", {})
        text = message.get("content", "").strip()

        if not text:
            return {"error": "Empty response text", "raw": result}

        try:
            return json.loads(text)
        except:
            return {"raw_text": text}

    except Exception as e:
        return {"error": str(e)}
