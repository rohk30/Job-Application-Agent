# ingestion/storage.py

import os
from uuid import uuid4

BASE_PATH = "storage/resumes"

def save_file_locally(file, user_id: int) -> str:
    os.makedirs(f"{BASE_PATH}/{user_id}", exist_ok=True)

    file_id = str(uuid4())
    file_path = f"{BASE_PATH}/{user_id}/{file_id}.pdf"

    with open(file_path, "wb") as f:
        content = file.file.read() if hasattr(file, "file") else file.read()
        f.write(content)

    return file_path