
from fastapi import APIRouter
from datetime import datetime
from db import db

router = APIRouter()


# ---- Endpoint: Get Portfolio ----

@router.get("/portfolio")
def get_portfolio(token: str):
    user = db.table("users").select("id").eq("login_token", token).single().execute().data
    if not user:
        return {"message": "Invalid token"}

    user_id = user["id"]
    portfolio = db.table("portfolio").select("*").eq("user_id", user_id).execute().data

    for p in portfolio:
        coin = db.table("coins").select("*").eq("coin_id", p["coin_id"]).single().execute().data
        current_price = coin["price"]
        profit_loss = (current_price - p["avg_price"]) * p["quantity"]
        p["current_price"] = current_price
        p["profit_loss"] = profit_loss
        p["coin_image_url"] = coin.get("coin_image_url")
        db.table('portfolio').update({"current_price": current_price, 'profit_loss': profit_loss}).eq('portfolio_id', p['portfolio_id']).execute()
        
    return {"portfolio": portfolio}


# ---- Endpoint: Buy Coin ----

@router.post("/portfolio/buy")
def buy_coin(token: str, quantity: int, coin_id: str):
    user_getting = db.table("users").select('*').eq('login_token', token).execute()
    if not user_getting.data:
        return {"message": "Invalid token"}

    user_id = user_getting.data[0]['id']

    coin = db.table('coins').select('*').eq('coin_id', coin_id).execute().data
    if not coin:
        return {"message": "Coin not found"}
    coin = coin[0]

    user = db.table("wallet").select("*").eq("user_id", user_id).single().execute().data
    if not user:
        return {"message": "User wallet not found"}

    total_cost = quantity * coin['price']
    if user["balance"] < total_cost:
        return {"message": "Insufficient balance"}

    existing = db.table("portfolio").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data

    if existing:
        old = existing[0]
        new_qty = old["quantity"] + quantity
        new_total = (old["avg_price"] * old["quantity"]) + total_cost
        new_avg = new_total / new_qty
        db.table("portfolio").update({
            "quantity": new_qty,
            "avg_price": new_avg
        }).eq("portfolio_id", old["portfolio_id"]).execute()
    else:
        db.table("portfolio").insert({
            "user_id": user_id,
            "coin_id": coin_id,
            "quantity": quantity,
            'avg_price': coin['price'],
            
        }).execute()

    db.table("wallet").update({
        "balance": user["balance"] - total_cost
    }).eq("user_id", user_id).execute()

    db.table("transactions").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "quantity": quantity,
        "price_per_unit": coin['price'],
        'total_value': total_cost,
        "type": "buy"
    }).execute()

    return {"message": "Coin bought successfully"}


# ---- Endpoint: Sell Coin ----

@router.post("/portfolio/sell")
def sell_coin(token: str, quantity: int, coin_id: str):
    user_getting = db.table("users").select('*').eq('login_token', token).execute()
    if not user_getting.data:
        return {"message": "Invalid token"}

    user_id = user_getting.data[0]['id']

    coin = db.table('coins').select('*').eq('coin_id', coin_id).execute().data
    if not coin:
        return {"message": "Coin not found"}
    coin = coin[0]

    user = db.table("wallet").select("*").eq("user_id", user_id).single().execute().data
    if not user:
        return {"message": "User wallet not found"}

    existing = db.table("portfolio").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data
    if not existing:
        return {"message": "You don't hold this coin"}

    old = existing[0]
    if quantity > old["quantity"]:
        return {"message": "Not enough quantity to sell"}

    remaining_qty = old["quantity"] - quantity
    if remaining_qty == 0:
        db.table("portfolio").delete().eq("portfolio_id", old["portfolio_id"]).execute()
    else:
        db.table("portfolio").update({
            "quantity": remaining_qty
        }).eq("portfolio_id", old["portfolio_id"]).execute()

    total_gain = quantity * coin['price']

    db.table("wallet").update({
        "balance": user["balance"] + total_gain
    }).eq("user_id", user_id).execute()

    db.table("transactions").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "quantity": quantity,
        "price_per_unit": coin['price'],
        "total_value": total_gain,
        "type": "sell"
    }).execute()

    return {"message": "Coin sold successfully"}
