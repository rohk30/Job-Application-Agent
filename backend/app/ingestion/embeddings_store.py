# ingestion/embeddings_store.py

from backend.db.session import SessionLocal
from backend.db.models.resume_embedding import ResumeEmbedding

def store_embedding(resume_id: int, embedding: list):
    db = SessionLocal()

    existing = db.query(ResumeEmbedding).filter_by(resume_id=resume_id).first()
    if existing:
        existing.embedding = embedding
    else:
        db.add(ResumeEmbedding(
            resume_id=resume_id,
            embedding=embedding
        ))

    db.commit()
    db.close()