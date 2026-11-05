from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Financial Text Sentiment API",
    description="Financial sentiment classification powered by FinBERT.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)
