import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()                                     # read .env
MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URI)            # Motor async client
db = client["voice_auction"]
products_coll = db["products"]
