from pathlib import Path
from typing import List
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


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
            self._load()

    def _load(self):
        self.index = faiss.read_index(str(self.faiss_file))
        # Загружаем метаданные
        with open(self.meta_file, "rb") as f:
            data = pickle.load(f)
            self.doc_ids = data.get("doc_ids", [])
            self.chunk_ids = data.get("chunk_ids", [])

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, str(self.faiss_file))
        data = {"doc_ids": self.doc_ids, "chunk_ids": self.chunk_ids}
        with open(self.meta_file, "wb") as f:
            pickle.dump(data, f)

    def add_chunk(self, chunk_id: int, text: str):
        embedding = self.model.encode([text], convert_to_numpy=True)
        if self.index is None:
            dim = embedding.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embedding)
        self.chunk_ids.append(chunk_id)
        self._save()

    def search(self, query: str, top_k: int = 5):
        if self.index is None or not self.chunk_ids:
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)
        return [self.chunk_ids[i] for i in I[0]]
