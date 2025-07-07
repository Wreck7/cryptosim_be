from fastapi import APIRouter
from db import db


router = APIRouter()

@router.get("/transactions")
def get_transactions(token: str):
    user = db.table('users').select('id').eq('login_token', token).execute()
    if not user:
        return {"message": "Invalid token"}
    user_id = user.data[0]['id']
    result = db.table("transactions").select("*").eq("user_id", user_id).execute()
    print(result)
    if result:
        return result.data
    else:
        return 'user not found!'
 
 
@router.get("/coin_transactions")
def get_transactions_by_coin(token: str, coin_id: str):
    user = db.table('users').select('id').eq('login_token', token).execute()
    if not user:
        return {"message": "Invalid token"}
    user_id = user.data[0]['id']
    result = db.table("transactions").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute()
    if result.data:
        return result.data
    else:
        return 'transactions not found!'