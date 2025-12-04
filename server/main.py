from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, HTTPException, Query

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


# --- READ ENDPOINTS ---
@app.get("/api/data")
def get_trade_data(
    date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    state: Optional[str] = Query(None, description="Filter by State Name"),
    apmc: Optional[str] = Query(None, description="Filter by APMC"),
    commodity: Optional[str] = Query(None, description="Filter by Commodity"),
    limit: int = 100,
    skip: int = 0
):
    """
    Search data with filters. All filters are optional.
    If no filters are provided, returns the most recent 100 records.
    """
    # 1. Build the query object
    query = build_filter_query(date, state, apmc, commodity)
    
    # 2. Fetch results
    results = fetch_filtered_data(query, limit, skip)
    
    return results

@app.get("/api/states")
def get_all_states():
    """Returns a list of all unique states in the DB."""
    return get_unique_values("state")

@app.get("/api/commodities")
def get_all_commodities():
    """Returns a list of all unique commodities in the DB."""
    return get_unique_values("commodity")


# --- SCRAPPER ENDPOINTS ---
@app.post("/api/scrape")
def trigger_scrape(
    background_tasks: BackgroundTasks, 
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    """
    Trigger the scraper for a specific date.
    Input: ?date=2023-12-05
    """
    try:
        # 1. Use Helper to Validate/Format
        formatted_date = format_date_for_api(date)
        
        # 2. Add to Background Tasks
        background_tasks.add_task(run_scraper_for_date, target_date=formatted_date)
        
        return {
            "status": "queued", 
            "message": f"Scraping started for {formatted_date}. Check logs for progress."
        }
        
    except ValueError as e:
        # If the helper fails (bad date format), return a 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))