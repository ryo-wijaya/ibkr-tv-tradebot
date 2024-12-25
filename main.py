from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from ibkr.ibkr_client import IBKRClient
from telegram.telegram_client import TelegramClient
from util.models import TradeRequest, FetchPortfolioRequest
from util.helpers import (
    format_telegram_trade_notification,
    format_telegram_error_notification,
)
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(level=logging.INFO)

ibkr_client = IBKRClient()
telegram_client = TelegramClient(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)


def lifespan(app: FastAPI):
    yield
    ibkr_client.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    try:
        return {"status": "Backend server is healthy and running :)"}
    except Exception as e:
        logging.error(f"Failed to perform health check: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform health check")


@app.post("/webhook/fetch-portfolio")
async def fetch_portfolio(request: FetchPortfolioRequest):
    if request.key != ibkr_client.secret_key:
        logging.warning("Unauthorized webhook request for fetch-portfolio.")
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        portfolio = ibkr_client.fetch_portfolio()
        telegram_client.send_message(portfolio)
        return {"status": "Portfolio sent to Telegram"}
    except Exception as e:
        logging.error(f"Failed to fetch portfolio: {e}")
        error_message = format_telegram_error_notification(
            "/webhook/fetch-portfolio", str(e)
        )
        telegram_client.send_message(error_message)
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio")


@app.post("/webhook/sell-market-order")
async def sell_market_order(trade_request: TradeRequest):
    if trade_request.key != ibkr_client.secret_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        response = ibkr_client.place_market_order(
            trade_request.symbol, trade_request.quantity
        )

        notification_message = format_telegram_trade_notification(
            trade_request.symbol,
            trade_request.quantity,
            response["status"],
        )
        telegram_client.send_message(notification_message)
        return {"status": "Order placed", "details": response}
    except Exception as e:
        logging.error(f"Failed to place order: {e}")
        error_message = format_telegram_error_notification(
            "/webhook/sell-market-order", str(e)
        )
        telegram_client.send_message(error_message)
        raise HTTPException(status_code=500, detail="Failed to place order")
