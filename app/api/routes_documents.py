from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pypdf import PdfReader


router = APIRouter()

UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

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
        raise HTTPException(status_code=400, detail="Unsupported file type")

    text_path = file_path + ".txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text_content)

    return {
        "filename": file.filename,
        "status": "uploaded and processed",
        "text_preview": text_content[:100] + "...",
    }
