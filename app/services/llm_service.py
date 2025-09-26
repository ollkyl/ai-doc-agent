import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
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

    answer = completion.choices[0].message["content"]
    print("Answer:", answer)
    return answer
