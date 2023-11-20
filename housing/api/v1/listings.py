import time

from fastapi import APIRouter

from housing import models
from housing.config import settings

router = APIRouter()


@router.get("/listing/{id}")
async def listing(id: int) -> models.Listing:
    start = time.time()


    print(time.time() - start)
