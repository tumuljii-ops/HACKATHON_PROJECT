import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Correct stable model
MODEL = "gemini-1.5-pro"   # more stable than flash
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def call_llm(prompt: str):
    if not API_KEY:
        return {"error": "GEMINI_API_KEY not set"}

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 4096
        }
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

        # 🔵 SAFE EXTRACTION
        candidates = result.get("candidates", [])
        if not candidates:
            return {"error": "No candidates returned", "raw": result}

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])

        if not parts:
            return {"error": "No response parts", "raw": result}

        text = parts[0].get("text", "").strip()

        if not text:
            return {"error": "Empty response text", "raw": result}

        # 🔵 TRY JSON PARSE (your use case)
        try:
            return json.loads(text)
        except:
            return {"raw_text": text}

    except Exception as e:
        return {"error": str(e)}
