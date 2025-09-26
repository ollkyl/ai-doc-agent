import logging

from app.services.vectorstore import VectorStore
from app.models.document import Document, Chunk
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.document import Chunk

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    async def query(self, db: AsyncSession, question: str, top_k: int = 5):
        logger.debug("Запрос к RAG: '%s'", question)
        chunk_ids = self.vectorstore.search(question, top_k)
        logger.debug("Найденные chunk_ids: %s", chunk_ids)

        if not chunk_ids:
            logger.warning("Контекст не найден для вопроса: %s", question)
            return ["No relevant contexxxt found."]

        stmt = select(Chunk.text).where(Chunk.id.in_(chunk_ids))
        result = await db.execute(stmt)
        chunks = result.scalars().all()
        logger.debug("Извлечено %d чанков из БД", len(chunks))
        return "\n".join(chunks)
