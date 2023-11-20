from fastapi import FastAPI

from housing.api import v1
from housing.flatfox import create_db_and_tables

app = FastAPI()

app.include_router(v1.router, prefix="/v1")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    pass
