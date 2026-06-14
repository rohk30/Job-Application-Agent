# app/services/search_service.py

from sqlalchemy import text
from backend.db.session import SessionLocal
from backend.app.ingestion.embeddings import get_embedding


def search_resumes(query: str, top_k: int = 5):
    db = SessionLocal()

    query_embedding = get_embedding(query)
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    sql = text("""
        SELECT
            r.id AS resume_id,
            u.full_name AS name,
            u.email AS email,
            (re.embedding <=> CAST(:embedding AS vector)) AS distance
        FROM resume_embeddings re
        JOIN resumes r ON r.id = re.resume_id
        JOIN candidate_profiles cp ON cp.id = r.candidate_profile_id
        JOIN users u ON u.id = cp.user_id
        ORDER BY re.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k;
    """)

    results = db.execute(sql, {
        "embedding": embedding_str,
        "top_k": top_k
    }).fetchall()

    db.close()

    return sorted(
        [
            {
                "resume_id": str(row.resume_id),
                "name": row.name,
                "email": row.email,
                "score": round(1 - float(row.distance), 4)
            }
            for row in results
        ],
        key=lambda x: x["score"],
        reverse=True
    )
