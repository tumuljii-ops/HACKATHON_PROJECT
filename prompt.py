def get_extraction_prompt(text):

    return f"""
You are an expert legal AI system specialized in Indian court judgments.

Your task is to extract structured information from the judgment.

Return ONLY VALID JSON. No explanation, no extra text.

FORMAT:

{{
  "case_number": "",
  "case_title": "",
  "court_name": "",
  "date_of_order": "",

  "parties": {{
    "petitioner": "",
    "respondent": ""
  }},

  "key_directions": [
    {{
      "text": "",
      "page_ref": "PAGE X",
      "confidence": 0.0
    }}
  ],

  "timelines": [
    {{
      "event": "",
      "date": "",
      "is_inferred": false
    }}
  ],

  "compliance_required": false,
  "appeal_possible": false,

  "summary": ""
}}

IMPORTANT RULES:
- DO NOT hallucinate
- If not found → leave field empty
- Extract DIRECTIVES carefully (orders, instructions by court)
- page_ref MUST match the page markers (--- PAGE X ---)
- Confidence:
    1.0 → explicitly written
    0.7 → strongly implied
    0.4 → weak inference

TEXT:
{text[:15000]}
"""

def get_action_prompt(extracted_json):

    return f"""
You are a senior government legal officer.

Based on the extracted court judgment data, generate a clear and practical action plan.

Return ONLY VALID JSON:

{{
  "action_required": "",
  "urgency_level": "HIGH / MEDIUM / LOW",
  "recommended_steps": [
    ""
  ],
  "appeal_decision": "",
  "deadline": "",
  "responsible_department": ""
}}

RULES:
- Be specific and actionable
- Avoid vague language
- If compliance_required = true → urgency HIGH
- If appeal_possible = true → evaluate whether appeal is needed
- Mention deadlines clearly (use inferred if needed)

DATA:
{extracted_json}
"""


