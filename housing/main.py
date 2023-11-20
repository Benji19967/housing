from fastapi import FastAPI

from housing.api import v1

app = FastAPI()

app.include_router(v1.router, prefix="/v1")


if __name__ == "__main__":
    pass
