from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def query_documents(request: QueryRequest):
    return {"question": request.question, "answer": "This is a placeholder answer."}
