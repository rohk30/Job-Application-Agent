# MOST IMPORTANT
# Needs to be updated to handle more sections and be more robust in identifying section headers.
# Trade-off between determinism and expensive model-LLM calls


SECTION_HEADERS = [
    "experience", "work experience",
    "education",
    "skills",
    "projects",
    "summary",
    "volunteering"
]

def segment_sections(text: str):
    sections = {}
    current_section = "general"
    sections[current_section] = []

    for line in text.split("\n"):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Only treat as a section header if the line IS the header (short, no punctuation)
        if (
            line_lower in SECTION_HEADERS
            or any(line_lower == h for h in SECTION_HEADERS)
        ) and len(line_stripped) < 40 and not line_stripped.endswith("."):
            current_section = line_lower
            sections[current_section] = []
        else:
            sections[current_section].append(line_stripped)

    return sections