from http.client import HTTPException
from fastapi import APIRouter, Query
from typing import Any, Dict, List, Optional

from server.schemas.enam_data_response import TradeDataResponse
from server.core.queries import (
    fetch_filtered_data,
    build_filter_query,
    fetch_pivoted_trends_optimized,
    get_unique_values,
)

# Create the router instance
router = APIRouter()


@router.get("/")
def get_trade_data(
    date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    state: Optional[str] = Query(None, description="Filter by State Name"),
    apmc: Optional[str] = Query(None, description="Filter by APMC"),
    commodity: Optional[str] = Query(None, description="Filter by Commodity"),
    limit: int = 100,
    skip: int = 0,
):
    query = build_filter_query(date, state, apmc, commodity)
    return fetch_filtered_data(query, limit, skip)


@router.get("/states")
def get_all_states():
    return get_unique_values("state")


@router.get("/commodities")
def get_all_commodities():
    return get_unique_values("commodity")


@router.get("/trends", response_model=List[Dict[str, Any]])
def get_price_trends(
    state: Optional[str] = Query(None, description="Filter by State"),
    apmc: Optional[str] = Query(
        None, description="Fixed Location to compare commodities"
    ),
    commodity: Optional[str] = Query(
        None, description="Fixed Commodity to compare locations"
    ),
):
    """
    Returns pivoted data for charting.

    - If you provide `apmc`: Returns prices of all commodities in that APMC.
    - If you provide `commodity`: Returns prices of that commodity across all APMCs.
    """
    if not apmc and not commodity:
        raise HTTPException(
            status_code=400,
            detail="Please provide either an APMC or a Commodity to analyze trends.",
        )

    trends = fetch_pivoted_trends_optimized(state=state, apmc=apmc, commodity=commodity)
    return trends
