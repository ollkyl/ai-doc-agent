from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.core.db import get_db
from app.models.document import Document
from app.services.vectorstore import VectorStore
from pypdf import PdfReader
import os

router = APIRouter()
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_store = VectorStore()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    # Сохранение загруженного файла
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Извлечение текстового содержимого
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

    # Сохранение текста в .txt файл
    text_path = file_path + ".txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text_content)

    # Сохранение в базу данных
    stmt = (
        insert(Document)
        .values(filename=file.filename, filepath=file_path, content=text_content)
        .returning(Document.id)
    )

    result = await db.execute(stmt)
    await db.commit()
    doc_id = result.scalar()

    # Добавление в VectorStore
    vector_store.add_documents([text_content])

    # Ответ
    return {
        "id": doc_id,
        "filename": file.filename,
        "status": "загружено и проиндексировано",
        "text_preview": text_content[:100] + "..." if len(text_content) > 100 else text_content,
    }
