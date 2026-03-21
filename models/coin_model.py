from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CoinData(BaseModel):
    coin_id: str
    name: str
    symbol: str
    rank: int
    price: float
    market_cap: float
    volume_24h: float
    ath: float
    percent_from_ath: float
    total_supply: float
    coin_image_url: str
    updated_at: Optional[datetime] = None
