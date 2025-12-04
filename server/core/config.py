from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "ENAM Data API"
    DEBUG_MODE: bool = False
    
    # MongoDB Atlas Settings
    MONGO_URI: str 
    DB_NAME: str = "enam_prices_db"
    ENAM_PRICES_COLLECTION: str = "enam_prices"

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()