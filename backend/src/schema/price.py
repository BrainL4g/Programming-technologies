from pydantic import BaseModel
from typing import Optional, List

class PriceHistoryEntry(BaseModel):
    date: str
    average_price: float

class ProductPricesResponse(BaseModel):
    product_id: int
    current_average_price: Optional[float]
    price_history: List[PriceHistoryEntry]