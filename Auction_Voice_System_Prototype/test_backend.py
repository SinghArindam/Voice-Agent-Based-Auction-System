# tests/test_backend.py
"""
Async end-to-end tests for the FastAPI + MongoDB auction backend.
Works on pytest-8, pytest-asyncio-0.21+, httpx-0.24 … 0.28+.

Run:  pytest -q
"""
from __future__ import annotations
import asyncio, inspect, uuid, datetime as dt
import pytest, pytest_asyncio, httpx
from backend.main import app      # ← be sure backend/__init__.py exists


# ------------------------------------------------------------------
# One event-loop for the whole session – keeps Motor on a live loop
# ------------------------------------------------------------------
@pytest_asyncio.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:    # noqa: D401
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ------------------------------------------------------------------
# httpx client wired to FastAPI (handles httpx versions automatically)
# ------------------------------------------------------------------
def _transport():
    sig = inspect.signature(httpx.ASGITransport)
    return (
        httpx.ASGITransport(app=app, lifespan="on")
        if "lifespan" in sig.parameters
        else httpx.ASGITransport(app=app)
    )


@pytest_asyncio.fixture
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(transport=_transport(),
                                 base_url="http://test") as cli:
        yield cli


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------
async def _first_product(cli: httpx.AsyncClient) -> dict:
    resp = await cli.get("/products")
    resp.raise_for_status()
    data = resp.json()
    assert data, "Seeder did not insert any products"
    return data[0]


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------
@pytest.mark.asyncio
async def test_list_products(client):
    prod = await _first_product(client)
    assert {"id", "highestBid"} <= prod.keys()


@pytest.mark.asyncio
async def test_place_higher_bid(client):
    prod = await _first_product(client)
    higher = prod["highestBid"] + 25
    payload = {
        "amount": higher,
        "bidder": f"pytest-{uuid.uuid4()}",
        "ts": dt.datetime.utcnow().isoformat() + "Z",
    }
    r = await client.post(f"/products/{prod['id']}/bids", json=payload)
    assert r.status_code == 200
    assert r.json()["highestBid"] == higher


@pytest.mark.asyncio
async def test_reject_equal_or_lower_bid(client):
    prod = await _first_product(client)
    payload = {
        "amount": prod["highestBid"],      # equal → reject
        "bidder": f"pytest-low-{uuid.uuid4()}",
        "ts": dt.datetime.utcnow().isoformat() + "Z",
    }
    r = await client.post(f"/products/{prod['id']}/bids", json=payload)
    assert r.status_code == 400
