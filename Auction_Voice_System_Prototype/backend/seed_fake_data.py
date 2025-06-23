"""
Bulk-seed MongoDB with fake auctions & bids for load-testing.

Run:  python seed_fake_data.py  --products 20  --max-bids 30
"""

import argparse
import asyncio
import random
import uuid
from datetime import datetime, timedelta

from faker import Faker  # pip install faker

try:
    from backend.models import Product, Bid  # same models file you have[1]
    from backend.database import products_coll  # motor collection[4]
except Exception as e:
    from models import Product, Bid  # same models file you have[1]
    from database import products_coll  # motor collection[4]

fake = Faker()


async def seed(products: int, max_bids: int):
    await products_coll.delete_many({})  # clean slate

    now = datetime.utcnow()
    prod_docs = []

    for _ in range(products):
        pid = str(uuid.uuid4())
        start_price = random.randint(50, 500)

        prod = Product(
            id=pid,
            name=fake.catch_phrase(),
            desc=fake.text(max_nb_chars=60),
            endTime=now + timedelta(minutes=random.randint(3, 10)),
            highestBid=start_price,
            bids=[],
        )

        # random bidding history
        bid_count = random.randint(0, max_bids)
        price = start_price
        for _ in range(bid_count):
            increment = random.randint(5, 50)
            price += increment
            bid = Bid(amount=price, bidder=fake.first_name())
            prod.bids.append(bid)
            prod.highestBid = price

        prod_docs.append(prod.model_dump())

    await products_coll.insert_many(prod_docs)
    print(f"[seed_fake_data] ✔ Inserted {len(prod_docs)} products.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--products", type=int, default=10)
    parser.add_argument("--max-bids", type=int, default=20)
    args = parser.parse_args()

    asyncio.run(seed(products=args.products, max_bids=args.max_bids))
