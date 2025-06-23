from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
try:
    from backend.models import Bid
    from backend.crud import list_products, get_product, place_bid
    from backend.seeder import seed_if_collection_empty
except Exception as e:
    from models import Bid
    from crud import list_products, get_product, place_bid
    from seeder import seed_if_collection_empty

app = FastAPI(title="Voice Auction API")

app.mount(
    "/static",                                  # anything under /static/…
    StaticFiles(directory="VoiceAuctionSystem/frontend"),
    name="static",
) 

@app.get("/", include_in_schema=False)          # keeps it out of the OpenAPI docs
async def serve_login():
    return FileResponse(
        "VoiceAuctionSystem/frontend/login.html",
        media_type="text/html",
    )                                            # technique discussed in SO answer[3]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _startup_seed():
    """
    Automatically seed MongoDB the first time the API boots.
    """
    await seed_if_collection_empty()


@app.get("/products")
async def _products():
    return await list_products()


@app.get("/products/{pid}")
async def _get_product(pid: str):
    prod = await get_product(pid)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod


@app.post("/products/{pid}/bids")
async def _post_bid(pid: str, bid: Bid):
    updated = await place_bid(pid, bid)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bid too low or auction closed",
        )
    return {"message": "Bid accepted", "highestBid": updated["highestBid"]}


@app.get("/stats")
async def _stats():
    prods = await list_products()
    return [
        {"productId": p.id, "highestBid": p.highestBid, "bidCount": len(p.bids)}
        for p in prods
    ]

# Optional
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)