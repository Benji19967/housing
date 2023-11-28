from typing import List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from housing import models
from housing.db import engine

router = APIRouter()


@router.get("/listings/{id}", response_model=models.Listing)
async def get_listing(id: int) -> models.Listing:
    """
    Example query: `curl <host>:<port>/v1/listings/97`
    """
    with Session(engine) as session:
        listing = session.get(models.Listing, id)
        if not listing:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Listing not found"
            )
        return listing


@router.get("/listings", response_model=List[models.Listing])
async def get_listings(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Sequence[models.Listing]:
    """
    Example query: `curl "<host>:<port>/v1/listings?offset=500&limit=2"`
    """
    with Session(engine) as session:
        listings = session.exec(
            select(models.Listing).offset(offset).limit(limit)
        ).all()
        return listings
