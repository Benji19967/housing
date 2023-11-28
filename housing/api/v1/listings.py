import time

from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from housing import models
from housing.config import settings
from housing.db import engine

router = APIRouter()


@router.get("/listing/{id}", response_model=models.Listing)
async def listing(id: int) -> models.Listing:
    with Session(engine) as session:
        listing = session.get(models.Listing, id)
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        return listing
