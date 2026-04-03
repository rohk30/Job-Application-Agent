import re

def clean_text(text: str) -> str:
    lines = text.splitlines()
    lines = [re.sub(r' +', ' ', line).strip() for line in lines]
    lines = [line for line in lines if line]  # drop blank lines
    return "\n".join(lines)