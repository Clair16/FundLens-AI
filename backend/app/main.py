from fastapi import FastAPI

from app.api.v1.documents import router as documents_router
from app.database.connection import engine, Base
from app.database import models

Base.metadata.create_all(
    bind = engine
)

app = FastAPI(
    title="FundLens AI API",
    description="Backend API for FundLens AI",
    version="1.0.0"
)


app.include_router(
    documents_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "FundLens AI API is running"
    }