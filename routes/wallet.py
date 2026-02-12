from fastapi import APIRouter, HTTPException
from db import db

router = APIRouter()

@router.get('/wallet')
def get_balance(token):
    users = db.table('users').select('id').eq('login_token', token).execute()
    if users.data:
        user_id = users.data[0]['id']
        res = db.table('wallet').select('*').eq('user_id', user_id).execute()
        return res.data[0]
    else:
        # return {'message': 'token invalid!'}
        raise HTTPException(status_code=401, detail="token invalid")