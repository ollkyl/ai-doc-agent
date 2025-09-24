from app.services.vectorstore import VectorStore
from app.models.document import Document, Chunk
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class RAGService:
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    async def query(self, db: AsyncSession, question: str, top_k: int = 5):
        chunk_ids = self.vectorstore.search(question, top_k)
        if not chunk_ids:
            return ["No relevant contexxxt found."]
        stmp = select(Chunk.text).where(Chunk.id.in_(chunk_ids))
        result = await db.execute(stmp)
        chunks = result.scalars().all()

        return "\n".join(chunks)
