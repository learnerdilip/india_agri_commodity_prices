from fastapi import APIRouter, Query
from typing import List, Optional

from server.schemas.enam_data_response import TradeDataResponse
from server.core.queries import fetch_filtered_data, build_filter_query, get_unique_values

# Create the router instance
router = APIRouter()

@router.get("/")
def get_trade_data(
    date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    state: Optional[str] = Query(None, description="Filter by State Name"),
    apmc: Optional[str] = Query(None, description="Filter by APMC"),
    commodity: Optional[str] = Query(None, description="Filter by Commodity"),
    limit: int = 100,
    skip: int = 0
):
    query = build_filter_query(date, state, apmc, commodity)
    return fetch_filtered_data(query, limit, skip)

@router.get("/states")
def get_all_states():
    return get_unique_values("stateName")

@router.get("/commodities")
def get_all_commodities():
    return get_unique_values("commodityName")