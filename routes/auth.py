from fastapi import APIRouter
from db import db
import random
import string

router = APIRouter()

@router.post("/register")
def register_user(email, name, username, password, gender, age, phone):
    print("DB URL:", db.url)
    check = db.table('users').select('*').or_(f"username.eq.{username},email.eq.{email}").execute()
    if check.data:
        return {"success": False, "message": "User already exists"}
    else:
        data = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'gender': gender,
            'age': age,
            'phone': phone
        }
        res = db.table('users').insert(data).execute()
        user_id = db.table('users').select('id').eq('username', username).execute()
        user_id = user_id.data[0]['id']
        wallet = db.table('wallet').insert({
            'user_id': user_id,
            'balance': 100000
        }).execute()
        return {"success": True, "message": "User registered successfully"}


def generate_phrase(length=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@router.post("/login")
def login_user(identifier,password):
    check = db.table('users').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").execute()
    user = check.data[0] if check.data else None
    if user and user['password'] == password:
        phrase = generate_phrase()
        db.table("users").update({"login_token": phrase}).eq("id", user["id"]).execute()
        return {"success": True, "message": "Login successful", "token": phrase, "user": user}
    else:
        return {"success": False, "message": "Invalid username/email or password"}
