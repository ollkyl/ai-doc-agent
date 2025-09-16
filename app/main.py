import fastapi
from app.api import routes_documents
from app.api import routes_query
from app.core.config import engine, Base
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(routes_documents.router, prefix="/documents", tags=["documents"])
app.include_router(routes_query.router, prefix="/query", tags=["query"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
