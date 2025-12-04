from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from server.core.config import settings
from server.core.utils import format_date_for_api
from server.scripts.enam_raw_scrapper import run_scraper_for_date

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