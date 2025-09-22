from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.core.db import get_db
from app.models.document import Document, Chunk
from app.services.vectorstore import VectorStore
from pypdf import PdfReader
import os, uuid
from app.core.utils import split_into_chunks_by_paragraphs


router = APIRouter()
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_store = VectorStore()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # Сохраняем файл с уникальным именем
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Извлекаем текст
    text_content = ""
    if file.filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        text_content = "\n".join(
            page.extract_text() for page in reader.pages if page.extract_text()
        )
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла")

    # Сохраняем в БД
    stmt = (
        insert(Document)
        .values(filename=file.filename, filepath=file_path, content=text_content)
        .returning(Document.id)
    )
    result = await db.execute(stmt)
    await db.commit()
    doc_id = result.scalar()

    # Разбиваем на чанки
    chunks = split_into_chunks_by_paragraphs(text_content, max_words=100)

    # Добавляем чанки в БД и VectorStore
    for i, chunk_text in enumerate(chunks):
        stmt_chunk = insert(Chunk).values(doc_id=doc_id, text=chunk_text).returning(Chunk.id)
        res = await db.execute(stmt_chunk)
        await db.commit()
        chunk_id = res.scalar()
        vector_store.add_chunk(chunk_id, chunk_text)

    return {
        "id": doc_id,
        "filename": file.filename,
        "status": f"загружено и проиндексировано {len(chunks)} чанков",
    }
