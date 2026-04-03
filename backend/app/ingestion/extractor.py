import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")

    return "\n".join(text)