from fastapi import APIRouter

from housing.api.v1 import health_check, listings

router = APIRouter()

router.include_router(health_check.router, tags=["Health Check"])
router.include_router(listings.router, tags=["Listings"])
