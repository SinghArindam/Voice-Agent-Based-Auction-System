from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Bid(BaseModel):
    amount: float
    bidder: str
    ts: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel):
    id: str
    name: str
    desc: str
    endTime: datetime
    highestBid: float
    bids: List[Bid] = []
