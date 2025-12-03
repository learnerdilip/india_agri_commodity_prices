import requests
import pandas as pd
from datetime import datetime

# The endpoint
API_URL = "https://enam.gov.in/web/Ajax_ctrl/trade_data_list"

def fetch_all_prices(from_date, to_date):
    """
    Fetches ALL data for the given date range using the "Magic Strings" 
    observed in the browser network tab.
    """
    
    # 1. EXACT Payload matching the browser's "Raw Form Data"
    # We ask for "Everything" (-- All --)
    payload = {
        "language": "en",
        "stateName": "-- All --",
        "apmcName": "-- Select APMCs --",
        "commodityName": "-- Select Commodity --",
        "fromDate": from_date,
        "toDate": to_date
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://enam.gov.in",
        "Referer": "https://enam.gov.in/web/dashboard/trade-data",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        print(f"Fetching ALL data for {from_date}...")
        response = requests.post(API_URL, data=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            return []

        data = response.json()
        
        # The key is 'data' based on standard datatable responses
        return data.get('data', [])

    except Exception as e:
        print(f"Exception: {e}")
        return []

if __name__ == "__main__":
    # 1. Configuration
    TARGET_STATE = "MAHARASHTRA"
    TARGET_COMMODITY = "Onion"
    
    # Use the date you saw working in the browser
    # (Or use datetime.now().strftime('%Y-%m-%d') for today)
    search_date = "2025-12-02" 

    # 2. Fetch Everything
    raw_data = fetch_all_prices(search_date, search_date)
    
    if not raw_data:
        print("❌ No data returned from server.")
    else:
        print(f"✅ Downloaded {len(raw_data)} total records from across India.")
        
        # 3. Load into Pandas for Filtering
        df = pd.DataFrame(raw_data)
        
        # Clean column names (strip whitespace just in case)
        df.columns = df.columns.str.strip()
        
        # 4. Filter for what you actually want
        # Note: We use str.contains(..., case=False) to be flexible
        filtered_df = df[
            (df['state'].str.upper() == TARGET_STATE.upper()) & 
            (df['commodity'].str.contains(TARGET_COMMODITY, case=False))
        ]
        
        if not filtered_df.empty:
            print(f"\n--- Found {len(filtered_df)} matches for {TARGET_COMMODITY} in {TARGET_STATE} ---")
            # Select useful columns to display
            display_cols = ['state', 'apmc_name', 'commodity', 'min_price', 'modal_price', 'max_price']
            # Only pick columns that actually exist in the dataframe
            actual_cols = [c for c in display_cols if c in df.columns]
            
            print(filtered_df[actual_cols].to_string(index=False))
        else:
            print(f"\n⚠️ No matches for {TARGET_COMMODITY} in {TARGET_STATE}.")
            print("Here are 5 random records to verify what the data looks like:")
            print(df[['state', 'commodity', 'modal_price']].sample(5))