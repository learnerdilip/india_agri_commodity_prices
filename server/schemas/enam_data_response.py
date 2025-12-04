from pydantic import BaseModel, Field
from typing import Optional

# This defines the structure of a single trade record in the API response
class TradeDataResponse(BaseModel):
    id: str = Field(..., alias="_id") # Maps MongoDB's '_id' to 'id'
    stateName: str
    apmcName: str
    commodityName: str
    min_price: float | str # Data sometimes comes as string or int
    max_price: float | str
    modal_price: float | str
    fetched_date: str
    
    class Config:
        # This tells Pydantic to read data as if it were a dictionary
        from_attributes = True
        populate_by_name = True

# This is for generic success messages
class Msg(BaseModel):
    message: str