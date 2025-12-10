from typing import List, Optional

from server.core.database import get_enam_price_collection


def build_filter_query(
    date: Optional[str] = None,
    state: Optional[str] = None,
    apmc: Optional[str] = None,
    commodity: Optional[str] = None,
) -> dict:
    """
    Constructs a MongoDB query dictionary based on provided filters.
    """
    query = {}

    # Add filters only if the user provided them
    if date:
        query["recording_date"] = date

    if state:
        # Case-insensitive search using Regex
        # e.g., "maharashtra" finds "Maharashtra"
        query["state"] = {"$regex": state, "$options": "i"}

    if apmc:
        query["apmc"] = {"$regex": apmc, "$options": "i"}

    if commodity:
        query["commodity"] = {"$regex": commodity, "$options": "i"}

    return query


def fetch_filtered_data(query: dict, limit: int = 100, skip: int = 0) -> List[dict]:
    """
    Executes the query and converts ObjectIds to strings.
    """
    collection = get_enam_price_collection()

    # Fetch data with pagination (limit/skip) to avoid crashing the server
    cursor = collection.find(query).skip(skip).limit(limit)

    results = []
    for doc in cursor:
        # Convert ObjectId to string so JSON can serialize it
        doc["_id"] = str(doc["_id"])
        results.append(doc)

    return results


def get_unique_values(field_name: str) -> List[str]:
    """
    Helper to get list of all States, APMCs, or Commodities.
    Useful for frontend dropdown menus.
    """
    collection = get_enam_price_collection()
    return collection.distinct(field_name)


def fetch_pivoted_trends_optimized(
    state: str = None, apmc: str = None, commodity: str = None
) -> list[dict]:
    collection = get_enam_price_collection()

    match_stage = {}
    if state:
        match_stage["state"] = {"$regex": state, "$options": "i"}
    if apmc:
        match_stage["apmc"] = {"$regex": apmc, "$options": "i"}
    if commodity:
        match_stage["commodity"] = {"$regex": commodity, "$options": "i"}

    # If APMC is fixed, we group by Commodity. If Commodity fixed, group by APMC.
    group_by_field = "$apmc" if commodity and not apmc else "$commodity"

    pipeline = [
        # 1. Filter Data (Reduce set immediately)
        {"$match": match_stage},
        # 2. Sort by Date (Crucial for ordered line charts)
        {"$sort": {"created_at": 1}},
        # 3. Group by Date to create the "Row" for that day
        # We push all items for this day into an array called "items"
        {
            "$group": {
                "_id": "$created_at",
                "items": {
                    "$push": {
                        "k": group_by_field,  # The Key (e.g., "Onion" or "Mumbai")
                        "v": "$modal_price",  # The Value (Price)
                    }
                },
            }
        },
        # 4. Transform the array into a Root Object (The "Pivot" magic)
        # This converts [{"k": "Onion", "v": 100}, {"k": "Potato", "v": 20}]
        # INTO -> {"Onion": 100, "Potato": 20}
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        {"created_at": "$_id"},  # Keep the date
                        {"$arrayToObject": "$items"},  # Pivot the array
                    ]
                }
            }
        },
        # 5. Final Sort (Optional, ensures API returns dates in order)
        {"$sort": {"created_at": 1}},
    ]

    # Execute Pipeline
    results = list(collection.aggregate(pipeline))
    return results
