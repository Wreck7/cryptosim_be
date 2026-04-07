import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth import router as auth_router
from routes.dashboard import router as dashboard_router
from routes.profile import router as profile_router
from routes.portfolio import router as portfolio_router
from routes.wallet import router as wallet_router
from routes.transactions import router as transactions_router
from routes.wishlist import router as wishlist_router

from services.coin_stream import start_coin_stream

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (replaces deprecated @app.on_event) ────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch the background coin price streamer
    logger.info("App startup — launching coin price streamer")
    stream_task = asyncio.create_task(start_coin_stream())
    yield
    # Shutdown: cancel the background task gracefully
    logger.info("App shutdown — cancelling coin price streamer")
    stream_task.cancel()
    try:
        await stream_task
    except asyncio.CancelledError:
        pass


# ── App ──────────────────────────────────────────────────────────────
app = FastAPI(title="Crypto Dashboard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://cryptosim-frontend.streamlit.app", "https://id-preview--3cfcc438-d89c-4905-9ab4-cc62e5ca9198.lovable.app"],
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
