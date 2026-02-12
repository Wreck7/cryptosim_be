
from fastapi import APIRouter
from db import db

router = APIRouter()


@router.post("/wishlist/add")
def add_to_wishlist(token: str, coin_id: str):
    user = db.table("users").select("id").eq("login_token", token).single().execute().data
    if not user:
        return {"message": "Invalid token"}
    user_id = user["id"]
    existing = db.table("wishlist").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data
    if existing:
        return {"message": "Coin already in wishlist"}
    db.table("wishlist").insert({
        "user_id": user_id,
        "coin_id": coin_id,
    }).execute()
    return {"message": "Coin added to wishlist"}



@router.get("/wishlist")
def get_wishlist(token: str):
    user = db.table("users").select("id").eq("login_token", token).single().execute().data
    if not user:
        return {"message": "Invalid token"}
    user_id = user["id"]
    wishlist = db.table("wishlist").select("*").eq("user_id", user_id).execute().data
    if wishlist:
        coins = []
        for item in wishlist:
            coin = db.table("coins").select("*").eq("coin_id", item["coin_id"]).single().execute().data
            coins.append(coin)
        return {"wishlist": coins}
    else:
        return {'message': 'Wishlist is empty!'}



@router.delete("/wishlist/remove")
def remove_from_wishlist(token: str, coin_id: str):
    user = db.table("users").select("id").eq("login_token", token).single().execute().data
    if not user:
        return {"message": "Invalid token"}
    user_id = user["id"]
    exists = db.table("wishlist").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data
    if not exists:
        return {"message": "Coin doesn't exist in wishlist"}
    db.table("wishlist").delete().eq("user_id", user_id).eq("coin_id", coin_id).execute()
    return {"message": "Coin removed from wishlist"}
        
