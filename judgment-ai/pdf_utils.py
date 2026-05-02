import fitz  # PyMuPDF

def extract_text(pdf_path):
    """
    Extract text page by page and attach page markers.
    This helps in traceability (PAGE X).
    """

    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        full_text += f"\n--- PAGE {page_num + 1} ---\n"
        full_text += text

    return full_text

