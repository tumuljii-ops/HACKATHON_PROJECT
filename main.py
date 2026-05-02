from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import json

from pdf_utils import extract_text
from prompt import get_extraction_prompt, get_action_prompt
from llm import call_llm

app = FastAPI()

# Enable frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory DB (hackathon demo)
verified_cases = []


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # STEP 1: Extract text from PDF
        text = extract_text(file_path)

        # STEP 2: Extraction prompt
        extraction_prompt = get_extraction_prompt(text)
        extraction_response = call_llm(extraction_prompt)

        extracted_json = safe_parse_llm_response(extraction_response)

        # STEP 3: Action plan prompt
        action_prompt = get_action_prompt(extracted_json)
        action_response = call_llm(action_prompt)

        action_json = safe_parse_llm_response(action_response)

        return {
            "extracted_data": extracted_json,
            "action_plan": action_json
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# 🔥 SAFE PARSER (IMPORTANT FIX)
def safe_parse_llm_response(response):

    # If mock LLM already returns dict → return directly
    if isinstance(response, dict):
        return response

    # If string → try JSON parse
    if isinstance(response, str):
        try:
            return json.loads(response)
        except:
            return {"raw_text": response}

    return {"error": "Invalid LLM response format"}


# ✅ APPROVE API
@app.post("/approve")
async def approve_case(data: dict = Body(...)):
    verified_cases.append(data)
    return {"status": "approved"}


# ✅ DASHBOARD API
@app.get("/dashboard")
async def dashboard():
    return verified_cases
