from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from server.api.v1.api import api_router
from server.core.config import settings
from server.core.utils import format_date_for_api
from server.schemas.enam_data_response import TradeDataResponse
from server.scripts.enam_raw_scrapper import run_scraper_for_date
from server.core.queries import fetch_filtered_data, build_filter_query, get_unique_values

app = FastAPI(title="eNAM Data Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "eNAM Server is running"}

app.include_router(api_router, prefix="/api/v1")