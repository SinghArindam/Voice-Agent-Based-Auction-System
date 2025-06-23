"""
Seed two demo products if the collection is empty.

– Called in main.py during FastAPI startup.
– Can also be run directly:  python backend/seeder.py
"""

import uuid
from datetime import datetime, timedelta
import asyncio
try:
    from backend.models import Product
    from backend.database import products_coll
except Exception as e:
    from models import Product
    from database import products_coll


async def seed_if_collection_empty() -> None:
    if await products_coll.count_documents({}):
        # Already populated
        return

    now = datetime.utcnow()
    docs = [
        Product(
            id=str(uuid.uuid4()),
            name="Vintage Watch",
            desc="Classic mechanical wrist-watch from the 1960s",
            endTime=now + timedelta(minutes=5),
            highestBid=100.0,
        ),
        Product(
            id=str(uuid.uuid4()),
            name="Antique Vase",
            desc="Hand-painted porcelain vase, Qing dynasty style",
            endTime=now + timedelta(minutes=5),
            highestBid=200.0,
        ),
    ]

    await products_coll.insert_many([p.model_dump() for p in docs])
    print(f"[Seeder] ✔ Inserted {len(docs)} demo products.")


if __name__ == "__main__":
    asyncio.run(seed_if_collection_empty())
