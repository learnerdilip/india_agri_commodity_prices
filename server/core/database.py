from pymongo import MongoClient

from server.core.config import settings


client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

def get_enam_price_collection():
    enam_price_collection = db[settings.ENAM_PRICES_COLLECTION]
    return enam_price_collection