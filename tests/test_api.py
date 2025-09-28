import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


load_dotenv()

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"  # можно проверить другую версию
HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY не найден в .env")

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ["HF_API_KEY"],
)

completion = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

print(completion.choices[0].message)
