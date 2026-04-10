"""
Supabase service layer for coin operations.
Encapsulates all database interactions for the coins table.
"""

import logging
from db import db

logger = logging.getLogger(__name__)


def upsert_coins(coins: list[dict]) -> None:
    """
    Batch upsert a list of coin dicts into the coins table.
    Uses on_conflict='coin_id' so existing rows are updated in-place
    and new rows are inserted — no duplicates.
    """
    if not coins:
        return

    db.table("coins").upsert(coins, on_conflict="coin_id").execute()
    logger.info("Upserted %d coins into Supabase", len(coins))


def get_all_coins() -> list[dict]:
    """Return all coins ordered by rank ascending."""
    response = db.table("coins").select(
        "*").order("rank", desc=False).execute()
    return response.data


def get_coin(coin_id: str) -> dict | None:
    """Return a single coin by coin_id, or None if not found."""
    response = db.table("coins").select("*").eq("coin_id", coin_id).execute()
    if response.data:
        return response.data[0]
    return None
