from datetime import datetime

def format_date_for_api(date_input: str) -> str:
    """
    Validates the input string and ensures it matches the format 
    required by the eNAM API (YYYY-MM-DD).
    
    Raises ValueError if the format is incorrect.
    """
    try:
        # 1. Try to parse the string to ensure it is a real date
        # We expect input like "2023-12-05"
        dt_object = datetime.strptime(date_input, "%Y-%m-%d")
        
        # 2. Convert it back to string to be safe
        return dt_object.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_input}. Expected YYYY-MM-DD.")