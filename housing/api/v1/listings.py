from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from starlette.status import HTTP_404_NOT_FOUND

from housing import models
from housing.db import engine

router = APIRouter()


@router.get("/listing/{id}", response_model=models.Listing)
async def listing(id: int) -> models.Listing:
    with Session(engine) as session:
        listing = session.get(models.Listing, id)
        if not listing:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Listing not found"
            )
        return listing
