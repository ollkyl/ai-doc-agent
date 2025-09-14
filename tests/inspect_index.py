import pickle
from pathlib import Path
import faiss
import numpy as np

INDEX_FILE = Path("data/index/document.index.pkl")

with open(INDEX_FILE, "rb") as f:
    data = pickle.load(f)

print("Ключи в файле:", data.keys())
print("Количество документов:", len(data["documents"]))
print("Документы:")
for doc in data["documents"]:
    print("-", doc)

index = data["index"]
print("\nТип индекса:", type(index))
print("Количество векторов в индексе:", index.ntotal)
