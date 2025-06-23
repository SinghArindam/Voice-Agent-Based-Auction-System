# backend/mongo_dump.py
"""
Dump every collection in the existing **voice_auction** database to JSON.

The script re-uses the   `db`   object that is already created in
backend/database.py, so it relies on the same   MONGO_URI   and needs no
extra connection logic.

Usage
-----
# activate your venv first
python backend/mongo_dump.py                 # → mongo_dump.json
python backend/mongo_dump.py my_dump.json    # → custom file name
"""

from __future__ import annotations
import asyncio, json, sys
from pathlib import Path
from datetime import datetime

# --------------------------------------------------------------------
#  Import the AsyncIOMotor database that the API already uses
# --------------------------------------------------------------------
try:
    from backend.database import db          # normal package layout
except ModuleNotFoundError:                  # direct run inside backend/
    from database import db                  # fallback for local tests


def _json_default(o):
    """Convert non-serialisable objects (e.g. datetime) to strings."""
    if isinstance(o, datetime):
        return o.isoformat()
    return str(o)


async def dump_to_json(out_path: Path):
    """Collect every collection (no _id) and write one JSON file."""
    dump: dict[str, list] = {}

    for name in await db.list_collection_names():       # Motor async call[6]
        cursor = db[name].find({}, {"_id": 0})          # projection: exclude _id
        dump[name] = await cursor.to_list(None)         # fetch all docs

    out_path.write_text(json.dumps(dump, default=_json_default, indent=2))
    print(f"✔ Mongo export written to {out_path.resolve()}")


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mongo_dump.json")
    asyncio.run(dump_to_json(output))
