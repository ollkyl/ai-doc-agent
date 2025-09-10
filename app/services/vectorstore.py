from pathlib import Path
from typing import List
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


DATA_DIR = Path("data/uploads")
INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(exist_ok=True)


INDEX_FILE = INDEX_DIR / "document.index.pkl"


class VectorStore:
    def __init__(self, index_file=INDEX_FILE):
        self.index_file = index_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

        if self.index_file.exists():
            self._load()

    def _load(self):
        with open(self.index_file, "rb") as f:
            data = pickle.load(f)
            self.index = data["index"]
            self.documents = data["documents"]

    def _save(self):
        data = {"index": self.index, "documents": self.documents}
        with open(self.index_file, "wb") as f:
            pickle.dump(data, f)

    def add_documents(self, texts: List[str]):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)
        self.documents.extend(texts)
        self.save()

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)
        results = [self.documents[i] for i in I[0]]
        return results
