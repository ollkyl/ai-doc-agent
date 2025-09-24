from app.services.vectorstore import VectorStore


def test_vectorstore():
    vs = VectorStore()

    # добавляем документы
    vs.add_documents(
        [
            "Сегодня солнечная погода",
            "Завтра будет дождь",
            "Машинное обучение помогает в анализе данных",
            "FastAPI удобен для создания API",
        ]
    )

    # делаем запрос
    results = vs.search("Какая будет погода?", top_k=2)

    print("Результаты поиска:", results)
    assert len(results) == 2


if __name__ == "__main__":
    test_vectorstore()
