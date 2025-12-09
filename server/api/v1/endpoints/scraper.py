from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from server.core.utils import format_date_for_api
from server.scripts.enam_raw_scrapper import run_scraper_for_date

router = APIRouter()

@router.post("/trigger")
def trigger_scrape(
    background_tasks: BackgroundTasks, 
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    try:
        formatted_date = format_date_for_api(date)
        background_tasks.add_task(run_scraper_for_date, target_date=formatted_date)
        return {"status": "queued", "message": f"Scraping started for {formatted_date}."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))