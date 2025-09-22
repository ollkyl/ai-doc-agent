import re
from typing import List


def split_into_chunks_by_paragraphs(text: str, max_words: int = 100) -> List[str]:
    chunks = []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    for para in paragraphs:
        words = para.split()
        if len(words) <= max_words:
            chunks.append(para)
        else:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            chunk = []
            word_count = 0
            for sent in sentences:
                sent_words = sent.split()
                chunk.append(sent)
                word_count += len(sent_words)
                if word_count >= max_words:
                    chunks.append(" ".join(chunk))
                    chunk = []
                    word_count = 0
            if chunk:
                chunks.append(" ".join(chunk))
    return chunks
