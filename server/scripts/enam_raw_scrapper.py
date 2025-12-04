import requests
import pandas as pd
from pymongo.errors import BulkWriteError

from server.core.database import get_enam_price_collection

API_URL = "https://enam.gov.in/web/Ajax_ctrl/trade_data_list"

def fetch_raw_data(date_str: str):
    """
    Internal function to hit the API.
    """
    payload = {
        "language": "en",
        "stateName": "-- All --",
        "apmcName": "-- Select APMCs --",
        "commodityName": "-- Select Commodity --",
        "fromDate": date_str,  # Start Date
        "toDate": date_str     # End Date (Same as start for single day)
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://enam.gov.in",
        "Referer": "https://enam.gov.in/web/dashboard/trade-data",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        response = requests.post(API_URL, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"❌ API Error {response.status_code} for {date_str}")
            return []
    except Exception as e:
        print(f"❌ Exception fetching {date_str}: {e}")
        return []

def run_scraper_for_date(target_date: str):
    """
    Main logic to fetch data for a specific date and save to MongoDB.
    """
    print(f"--- Processing Single Date: {target_date} ---")
    
    collection = get_enam_price_collection()
    
    # 1. Fetch
    raw_data = fetch_raw_data(target_date)
    
    if raw_data:
        # 2. Process
        df = pd.DataFrame(raw_data)
        
        # Inject metadata
        df['recording_date'] = target_date
        
        # Convert to dictionary records
        records = df.to_dict('records')
        
        # 3. Save to DB
        if records:
            try:
                collection.insert_many(records, ordered=False)
                print(f"✅ Inserted {len(records)} new records.")
            except BulkWriteError as bwe:
                # This error triggers if SOME records were duplicates
                inserted_count = bwe.details['nInserted']
                print(f"⚠️ specific records already existed. Ignored duplicates.")
                print(f"✅ Successfully added {inserted_count} NEW records.")
    else:
        print(f"⚠️ No data found for {target_date}.")