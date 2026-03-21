"""
Background coin price streamer.
Polls Coinpaprika every POLL_INTERVAL seconds and upserts
the top 20 coins into Supabase via the supabase_service layer.
"""

import asyncio
import logging
from datetime import datetime, timezone

import httpx

from services.supabase_service import upsert_coins

logger = logging.getLogger(__name__)

COINPAPRIKA_TICKERS_URL = "https://api.coinpaprika.com/v1/tickers"
POLL_INTERVAL = 5  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds (doubles each retry)


def _coin_image_url(coin_id: str) -> str:
    return f"https://static.coinpaprika.com/coin/{coin_id}/logo.png"


def _format_coins(raw_coins: list[dict]) -> list[dict]:
    """Extract and format the top 20 coins from the raw API response."""
    top_20 = sorted(raw_coins, key=lambda c: c["rank"])[:20]
    now = datetime.now(timezone.utc).isoformat()

    formatted = []
    for coin in top_20:
        usd = coin["quotes"]["USD"]
        formatted.append({
            "coin_id": coin["id"],
            "name": coin["name"],
            "symbol": coin["symbol"],
            "rank": coin["rank"],
            "price": usd["price"],
            "market_cap": usd["market_cap"],
            "volume_24h": usd["volume_24h"],
            "ath": usd.get("ath_price", 0),
            "percent_from_ath": usd.get("percent_from_price_ath", 0),
            "total_supply": coin.get("total_supply", 0),
            "coin_image_url": _coin_image_url(coin["id"]),
            "updated_at": now,
        })
    return formatted


async def _fetch_tickers(client: httpx.AsyncClient) -> list[dict]:
    """Fetch tickers from Coinpaprika with retry logic."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = await client.get(COINPAPRIKA_TICKERS_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.TimeoutException) as exc:
            logger.warning(
                "Coinpaprika fetch attempt %d/%d failed: %s",
                attempt, MAX_RETRIES, exc,
            )
            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_BACKOFF * attempt)
    # All retries exhausted — return empty so the cycle is skipped
    logger.error("All %d retries exhausted. Skipping this cycle.", MAX_RETRIES)
    return []


async def start_coin_stream() -> None:
    """
    Main loop: runs forever, fetching prices and upserting them.
    Designed to be launched via asyncio.create_task() at app startup.
    """
    logger.info("Starting coin price streaming (every %ds)...", POLL_INTERVAL)

    async with httpx.AsyncClient() as client:
        while True:
            try:
                raw = await _fetch_tickers(client)
                if raw:
                    coins = _format_coins(raw)
                    upsert_coins(coins)
            except asyncio.CancelledError:
                logger.info("Coin stream task cancelled. Shutting down.")
                break
            except Exception as exc:
                # Catch-all so the background task never crashes the server
                logger.exception("Unexpected error in coin stream: %s", exc)

            await asyncio.sleep(POLL_INTERVAL)
