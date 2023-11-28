from contextlib import asynccontextmanager

from fastapi import FastAPI

from housing.api import v1
from housing.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(v1.router, prefix="/v1")
