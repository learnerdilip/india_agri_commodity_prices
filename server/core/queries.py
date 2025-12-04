from typing import List, Optional
from server.core.database import get_enam_price_collection

def build_filter_query(
    date: Optional[str] = None,
    state: Optional[str] = None,
    apmc: Optional[str] = None,
    commodity: Optional[str] = None
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

def fetch_filtered_data(
    query: dict, 
    limit: int = 100, 
    skip: int = 0
) -> List[dict]:
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