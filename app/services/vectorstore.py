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

        if self.index_file.exists():
            self._load()

    def _load(self):
        with open(self.index_file, "rb") as f:
            data = pickle.load(f)
            self.index = data["index"]
            self.doc_ids = data["doc_ids"]

    def _save(self):
        data = {"index": self.index, "doc_ids": self.doc_ids}
        with open(self.index_file, "wb") as f:
            pickle.dump(data, f)

    def add_chunk(self, chunk_id: int, text: str):
        embedding = self.model.encode([text], convert_to_numpy=True)
        if self.index is None:
            dim = embedding.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embedding)
        self.doc_ids.append(chunk_id)
        self._save()

    def search(self, query: str, top_k: int = 5):
        if self.index is None or not self.chunk_ids:
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)

        results = [self.chunk_ids[i] for i in I[0]]
        return results
