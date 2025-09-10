import fastapi
from app.api import routes_documents
from app.api import routes_query


app = fastapi.FastAPI()

app.include_router(routes_documents.router, prefix="/documents", tags=["documents"])
app.include_router(routes_query.router, prefix="/query", tags=["query"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
