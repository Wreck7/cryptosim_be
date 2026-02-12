from fastapi import APIRouter
from db import db
import requests


router = APIRouter()

COIN_TICKERS_URL = "https://api.coinpaprika.com/v1/tickers"


def coin_image_url(coin_id):
    return f"https://static.coinpaprika.com/coin/{coin_id}/logo.png"


def fetch_top_20_coin_data():
    response = requests.get(COIN_TICKERS_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from CoinPaprika")
    
    all_coins = response.json()
    top_20 = sorted(all_coins, key=lambda x: x["rank"])[:20]

    formatted = []
    for coin in top_20:
        formatted.append({
            "coin_id": coin["id"],
            "name": coin["name"],
            "rank": coin["rank"],
            "total_supply": coin['total_supply'],
            "price": coin["quotes"]["USD"]["price"],
            "volume_24h": coin["quotes"]["USD"]["volume_24h"],
            "ath": coin["quotes"]["USD"].get("ath_price", 0),
            "percent_from_ath": coin["quotes"]["USD"].get("percent_from_price_ath", 0),
            "market_cap": coin["quotes"]["USD"]["market_cap"],
            "symbol": coin["symbol"],
            "coin_image_url": coin_image_url(coin["id"])
        })
    return formatted

def update_coins_in_db():
    coins = fetch_top_20_coin_data()
    for coin in coins:
        existing = db.table("coins").select("*").eq("coin_id", coin["coin_id"]).execute()
        if existing.data:
            db.table("coins").update(coin).eq("coin_id", coin["coin_id"]).execute()
        else:
            db.table("coins").insert(coin).execute()
    return coins



@router.get("/refresh-dashboard")
def refresh_dashboard():
    coins = update_coins_in_db()
    return {"success": True, "message": "Dashboard updated", "count": len(coins)}

@router.get("/coins")
def get_all_coins():
    response = db.table("coins").select("*").order("rank", desc=False).execute()
    return response.data

@router.get('/coins/{coin_id}')
def get_specific_coin(coin_id):
    res = db.table('coins').select('*').eq('coin_id', coin_id).execute()
    return res.data[0]
    


