import re
import spacy

nlp = spacy.load("en_core_web_sm")

DATE_PATTERN = re.compile(
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
    r'|January|February|March|April|June|July|August|September|October|November|December)'
    r'[\s,]*\d{4}|\d{2}/\s*\d{4}|\d{4}\s*[-–]\s*(\d{4}|present|current)',
    re.IGNORECASE
)
HEADER_LINE_MAX_LEN = 120


def extract_email(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text, re.IGNORECASE)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'\+?[\d][\d\s\-\(\)]{8,15}', text)
    return match.group(0).strip() if match else None


KNOWN_SKILLS = {
    "python", "java", "sql", "flutter", "aws", "docker",
    "kotlin", "c++", "html", "css", "mysql", "tensorflow",
    "pytorch", "keras", "numpy", "pandas", "scikit", "git",
    "javascript", "typescript", "react", "node", "fastapi",
    "django", "flask", "mongodb", "postgresql", "redis"
}


def extract_name(sections: dict):
    general = sections.get("general", [])
    for line in general:
        line_s = line.strip()
        if not line_s:
            continue
        # Name is typically the first short line with no digits, emails, or special chars
        if len(line_s.split()) <= 5 and not re.search(r'[\d@|/]', line_s):
            return line_s
    return None


def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in KNOWN_SKILLS if skill in text_lower]


def extract_summary(sections: dict):
    for key in sections:
        if any(k in key for k in ["summary", "profile", "about", "objective"]):
            return " ".join(line.strip() for line in sections[key] if line.strip())
    return None


def _has_date(line: str) -> bool:
    return bool(DATE_PATTERN.search(line))


def _parse_dates(line: str):
    matches = re.findall(r'\d{2}/\s*\d{4}|\d{4}\s*[-–]\s*(\d{4}|present|current)|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{4}', line, re.IGNORECASE)
    matches = [m.strip() for m in matches if m.strip()]
    # also grab full MM/YYYY tokens directly
    tokens = re.findall(r'\d{2}/\s*\d{4}', line)
    all_dates = tokens if tokens else matches
    start = all_dates[0] if len(all_dates) > 0 else None
    end = all_dates[1] if len(all_dates) > 1 else None
    return start, end


def _is_entry_header(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("-") or line.startswith("•"):
        return False
    return _has_date(line) and len(line) < HEADER_LINE_MAX_LEN


def _extract_role_company(line: str):
    """Use pipe-split if available, otherwise NER fallback."""
    if "|" in line:
        parts = [p.strip() for p in line.split("|")]
        role = parts[0]
        company = parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
        return role, company
    doc = nlp(line)
    company = next((ent.text for ent in doc.ents if ent.label_ == "ORG"), None)
    role = line.split(",")[0].strip()
    return role, company or line


def _extract_degree_institution(line: str):
    """Use pipe-split if available, otherwise NER fallback."""
    if "|" in line:
        parts = [p.strip() for p in line.split("|")]
        degree = parts[0]
        institution = parts[1] if len(parts) > 1 else ""
        return degree, institution
    doc = nlp(line)
    institution = next((ent.text for ent in doc.ents if ent.label_ in ("ORG", "GPE")), None)
    degree = re.split(r'[,@]', line)[0].strip()
    return degree, institution or line


def extract_projects(sections: dict):
    projects = []
    for key in sections:
        if "project" not in key:
            continue
        current = None
        desc_lines = []
        for line in sections[key]:
            line_s = line.strip()
            if not line_s:
                continue
            is_name = (
                len(line_s) < 60
                and not line_s[0].islower()
                and not line_s.startswith(("In ", "I ", "The ", "We ", "This "))
            )
            if is_name:
                if current is not None:
                    current["description"] = " ".join(desc_lines)
                    projects.append(current)
                current = {"name": line_s, "description": ""}
                desc_lines = []
            elif current is not None:
                desc_lines.append(line_s)
        if current is not None:
            current["description"] = " ".join(desc_lines)
            projects.append(current)
    return projects


def extract_experience(sections: dict):
    experiences = []
    for key in sections:
        if "experience" not in key and "work" not in key:
            continue
        current = None
        desc_lines = []
        for line in sections[key]:
            line_s = line.strip()
            if not line_s:
                continue
            if _is_entry_header(line_s):
                if current:
                    current["description"] = " ".join(desc_lines)
                    experiences.append(current)
                start, end = _parse_dates(line_s)
                role, company = _extract_role_company(line_s)
                current = {
                    "company": company,
                    "role": role,
                    "start_date": start,
                    "end_date": end,
                    "description": ""
                }
                desc_lines = []
            elif current:
                desc_lines.append(line_s)
        if current:
            current["description"] = " ".join(desc_lines)
            experiences.append(current)
    return experiences


def extract_education(sections: dict):
    education_list = []
    for key in sections:
        if "education" not in key:
            continue
        current = None
        for line in sections[key]:
            line_s = line.strip()
            if not line_s:
                continue
            if _is_entry_header(line_s) or ("|" in line_s and _has_date(line_s)):
                if current:
                    education_list.append(current)
                start, end = _parse_dates(line_s)
                degree, institution = _extract_degree_institution(line_s)
                current = {
                    "institution": institution,
                    "degree": degree,
                    "start_date": start,
                    "end_date": end
                }
        if current:
            education_list.append(current)
    return education_list
