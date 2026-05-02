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

# In-memory DB (for hackathon demo)
verified_cases = []

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # STEP 1: Extract text
        text = extract_text(file_path)

        # STEP 2: Extraction
        extraction_prompt = get_extraction_prompt(text)
        extraction_response = call_llm(extraction_prompt)

        try:
            extracted_content = extraction_response["choices"][0]["message"]["content"]
            extracted_json = json.loads(extracted_content)
        except:
            extracted_json = {"error": extraction_response}

        # STEP 3: Action Plan
        action_prompt = get_action_prompt(extracted_json)
        action_response = call_llm(action_prompt)

        try:
            action_content = action_response["choices"][0]["message"]["content"]
            action_json = json.loads(action_content)
        except:
            action_json = {"error": action_response}

        return {
            "extracted_data": extracted_json,
            "action_plan": action_json
        }

    finally:
        os.remove(file_path)


# ✅ APPROVE API
@app.post("/approve")
async def approve_case(data: dict = Body(...)):
    verified_cases.append(data)
    return {"status": "approved"}


# ✅ DASHBOARD API
@app.get("/dashboard")
async def dashboard():
    return verified_cases




