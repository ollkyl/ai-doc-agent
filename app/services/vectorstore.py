import logging
from pathlib import Path
from typing import List
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(exist_ok=True)

INDEX_FILE = INDEX_DIR / "document.index.pkl"


class VectorStore:
    def __init__(self, index_file=INDEX_FILE):
        self.index_file = index_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.doc_ids: List[int] = []
        self.chunk_ids: List[int] = []

        self.faiss_file = self.index_file.with_suffix(".faiss")
        self.meta_file = self.index_file.with_suffix(".pkl")

        if self.faiss_file.exists() and self.meta_file.exists():
            logger.debug("Загружаю существующий индекс: %s", self.faiss_file)
            self._load()
        else:
            logger.debug("Файлы индекса не найдены. Начинаем с пустого состояния.")

    def _load(self):
        logger.debug("Чтение FAISS индекса из %s", self.faiss_file)
        self.index = faiss.read_index(str(self.faiss_file))
        with open(self.meta_file, "rb") as f:
            data = pickle.load(f)
            self.doc_ids = data.get("doc_ids", [])
            self.chunk_ids = data.get("chunk_ids", [])
        logger.debug("Загружено %d chunk_ids: %s", len(self.chunk_ids), self.chunk_ids)

    def _save(self):
        if self.index is not None:
            logger.debug("Сохраняю FAISS индекс в %s", self.faiss_file)
            faiss.write_index(self.index, str(self.faiss_file))
        data = {"doc_ids": self.doc_ids, "chunk_ids": self.chunk_ids}
        with open(self.meta_file, "wb") as f:
            pickle.dump(data, f)
        logger.debug("Сохранены метаданные: %d chunk_ids", len(self.chunk_ids))

    def add_chunk(self, chunk_id: int, text: str):
        logger.debug("Добавление чанка %s: '%s...'", chunk_id, text[:50])
        embedding = self.model.encode([text], convert_to_numpy=True)
        if self.index is None:
            dim = embedding.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            logger.debug("Создан новый FAISS индекс размерности %d", dim)

        self.index.add(embedding)
        self.chunk_ids.append(chunk_id)
        logger.debug("Текущие chunk_ids: %s", self.chunk_ids)
        self._save()

    def search(self, query: str, top_k: int = 5):
        logger.debug("Поиск по запросу: '%s'", query)
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)
        results = [self.chunk_ids[i] for i in I[0]]
        logger.debug("Результаты поиска: %s", results)
        return results
