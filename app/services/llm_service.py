# app/services/llm_service.py
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY не найден. Проверьте файл .env")

client = InferenceClient(
    provider="featherless-ai",
    api_key=HF_API_KEY,
)


def query_hf_model(question: str, context: str = "") -> str:
    prompt = f"Вот информация:\n{context}\n\nВопрос: {question}\nПереведи вопрос на русский и ответь на русском:"
    print("Prompt:", prompt)
    messages = [{"role": "user", "content": prompt}]

    # Запрос к Hugging Face через InferenceClient
    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2", messages=messages
    )

    # Возвращаем текст ответа
    return completion.choices[0].message["content"]
