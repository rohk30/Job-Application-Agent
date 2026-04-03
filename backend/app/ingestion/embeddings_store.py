# ingestion/embeddings_store.py

from backend.db.session import SessionLocal
from backend.db.models.resume_embedding import ResumeEmbedding

def store_embedding(resume_id: int, embedding: list):
    db = SessionLocal()

    obj = ResumeEmbedding(
        resume_id=resume_id,
        embedding=embedding
    )

    db.add(obj)
    db.commit()
    db.close()