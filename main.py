from fastapi import FastAPI
from cryptosim_be.routes.auth import router as auth_router
from cryptosim_be.routes.dashboard import router as dashboard_router
from cryptosim_be.routes.profile import router as profile_router
from cryptosim_be.routes.portfolio import router as portfolio_router
from cryptosim_be.routes.wallet import router as wallet_router
from cryptosim_be.routes.transactions import router as transactions_router
from cryptosim_be.routes.wishlist import router as wishlist_router


app = FastAPI(title="Crypto Dashboard API")


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(portfolio_router)
app.include_router(wallet_router)
app.include_router(transactions_router)
app.include_router(wishlist_router)

