from fastapi import APIRouter, HTTPException
from services.supabase_service import upsert_coins, get_all_coins, get_coin

import logging
import httpx

logger = logging.getLogger(__name__)

router = APIRouter()

COIN_TICKERS_URL = "https://api.coinpaprika.com/v1/tickers"


def _coin_image_url(coin_id: str) -> str:
    return f"https://static.coinpaprika.com/coin/{coin_id}/logo.png"


def _fetch_and_format_coins() -> list[dict]:
    """Synchronous fetch used only by the manual /refresh-dashboard endpoint."""
    from datetime import datetime, timezone

    response = httpx.get(COIN_TICKERS_URL, timeout=10)
    response.raise_for_status()
    all_coins = response.json()
    top_20 = sorted(all_coins, key=lambda c: c["rank"])[:20]
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


@router.get("/refresh-dashboard")
def refresh_dashboard():
    """Manual override: fetch latest prices and upsert immediately."""
    try:
        coins = _fetch_and_format_coins()
        upsert_coins(coins)
        return {"success": True, "message": "Dashboard updated", "count": len(coins)}
    except Exception as exc:
        logger.exception("Failed to refresh dashboard: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to refresh dashboard")


@router.get("/coins")
def get_all_coins_route():
    return get_all_coins()


@router.get("/coins/{coin_id}")
def get_specific_coin(coin_id: str):
    coin = get_coin(coin_id)
    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found")
    return coin
