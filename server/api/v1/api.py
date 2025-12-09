from fastapi import APIRouter
from server.api.v1.endpoints import enam_data, scraper

# This router holds ALL endpoints for V1
api_router = APIRouter()

# 1. Enam Data
# Prefix based on filename: /enam-data
api_router.include_router(
    enam_data.router, 
    prefix="/enam-data", 
    tags=["Enam Data"]
)

# 2. Scraper
# Prefix based on filename: /scraper
api_router.include_router(
    scraper.router, 
    prefix="/scraper", 
    tags=["Scraper"]
)