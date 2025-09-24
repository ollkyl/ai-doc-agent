from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.rag_service import RAGService
from app.services.vectorstore import VectorStore
from app.services.llm_service import query_hf_model
from pydantic import BaseModel

router = APIRouter(prefix="/query")

vectorstore = VectorStore()
rag_service = RAGService(vectorstore=vectorstore)


class QueryRequest(BaseModel):
    question: str


@router.post("/")
async def ask_question(request: QueryRequest, db: AsyncSession = Depends(get_db)):
    # 1. Получаем контекст через RAG
    question = request.question
    context = await rag_service.query(db, question, top_k=5)

    # 2. Отправляем на Hugging Face API
    answer = query_hf_model(question, context)

    return {"question": question, "answer": answer}
