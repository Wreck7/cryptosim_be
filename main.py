from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.dashboard import router as dashboard_router
from routes.profile import router as profile_router
from routes.portfolio import router as portfolio_router
from routes.wallet import router as wallet_router
from routes.transactions import router as transactions_router
from routes.wishlist import router as wishlist_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Crypto Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8501', ""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(portfolio_router)
app.include_router(wallet_router)
app.include_router(transactions_router)
app.include_router(wishlist_router)
