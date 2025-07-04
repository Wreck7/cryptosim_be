from fastapi import APIRouter
from cryptosim_be.db import db


router = APIRouter()

@router.get('/profile')
def name(token):
    res = db.table('users').select('*').eq('login_token', token).execute()
    return res.data[0]
    
