"""
All database I/O in one place so main.py stays slim.
"""

import datetime as dt
from typing import List
from pymongo import ReturnDocument

try:
    from backend.models import Product, Bid
    from backend.database import products_coll
except Exception as e:
    from models import Product, Bid
    from database import products_coll


async def list_products() -> List[Product]:
    return [Product(**p) async for p in products_coll.find()]


async def get_product(pid: str) -> Product | None:
    doc = await products_coll.find_one({"id": pid})
    return Product(**doc) if doc else None


async def place_bid(pid: str, bid: Bid):
    """
    Only succeed if:
      – auction still open
      – bid.amount > current highestBid
    Atomic update via find_one_and_update.
    """
    doc = await products_coll.find_one_and_update(
        {
            "id": pid,
            "highestBid": {"$lt": bid.amount},
            "endTime": {"$gt": dt.datetime.utcnow()},
        },
        {
            "$push": {"bids": bid.model_dump()},
            "$set": {"highestBid": bid.amount},
        },
        return_document=ReturnDocument.AFTER,
    )
    return doc  # None means rejected
