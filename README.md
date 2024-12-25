### Description

Trading bot that exposes webhooks meant to be used to connect TradingView alerts with Interactive Brokers, providing the ability to trigger round-the-clock stop loss strategies.

This bot is only configured to trade on SMART eligible exchanges in USD. Extend the bot if you wish to trade other exchanges, currencies, or specialized instruments (like mutual funds).

#### Original Purpose

Stop orders cannot be placed outside of regular trading hours for most/all brokers. This is because the stop price may be easily breached due to low volume and wide bid-ask spreads. Stop limit orders can be used, but there is risk of non-execution in volatile markets.

The idea is to circumvent this by using 3rd party services (like TradingView) to ensure capital preservation via almost 24/7 "stop losses" put in place in the form of constant automated monitoring, which creates sell market orders upon specific price alerts. E.g. If you hold NVDA and it tanks during the pre-market due to sudden bad news that affects its sentiment, you can guarantee a sell market order if it dips below a certain price (configured via a TradingView alert). This guarantees the closing of the position (although likely with some price slippage).

#### Problems

In fast-moving or illiquid markets, the bot may trigger a sell market order at a significantly lower price than expected, e.g. when the stop price is $50 and the stock opens at $25 at the start of the pre-market session, the market order will execute at $25. If this behavior is not desired, extend the bot account for such scenarios.

#### Features

Each trade/account interaction/error with the webhooks/IBKR will result in a Telegram notification.

**Webhooks:**

1. Fetch current holdings and send the data via Telegram to a user (smoke test for IBKR Trading API).
2. Create a sell market order for a specific share at a specific quantity.

### Setup

#### Pre-requisites

1. Ensure that you have a paid version of TradingView that supports webhooks. You may replace TradingView with another price alert service that can send HTTP POST requests.
2. Ensure that you have an active and funded IBKR Pro account. API access must be enabled in Trader Workstation (TWS) or IB Gateway.
3. For best results, ensure that you are subscribed to some form of real-time US market data, either via TradingView or via broker integration.
4. In TWS, configure API access to 'enable ActiveX and Socket Clients', as well as set the correct port number.
5. Setup a telegram bot via BotFather. Retrieve the bot token, start a chat, and retrieve the chat id.
6. Setup the application

#### Local Application Setup

Requirements: Python 3.9 or later, pip, venv, and OpenSSL (optional)

1. Clone repository

```bash
git clone https://github.com/ryo-wijaya/ibkr-tv-tradebot
cd ibkr-tv-tradebot
```

2. Create and activate virtual environment

```bash
python -m venv env
.\env\Scripts\activate (windows) or source ./env/bin/activate (Linux/Mac)
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Define or export environment variables

```bash
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
CLIENT_ID=1001
WEBHOOK_SECRET=your-secure-webhook-secret
```

5. Start the application

```bash
uvicorn main:app --reload --port 8080
```

#### Usage

1. Ensure the bot is up, running, and configured correctly, whether locally or deployed. For testing, its best to try out with a paper account first.
2. In TradingView (or any other alternative), create a price alert for a stock you own.
3. [Local] Perform tests for each price alert in the Webhook section:
   - For a connection smoke test, set up the webhook: `http://localhost:8000/webhook/fetch-portfolio` with payload:
     ```json
     {
       "key": "your-webhook-secret"
     }
     ```
     You should receive a Telegram message containing your positions. This is a sanity tests for the IBKR API connection.
   - For a live sell market order test, set up the webhook: `http://localhost:8000/webhook/sell-market-order` with payload:
     ```json
     {
       "key": "your-webhook-secret",
       "symbol": "{{ticker}}",
       "quantity": 1
     }
     ```
     You should receive a Telegram message indicating the close and success status.

#### Deployment

If deploying to a server or cloud provider (e.g., GCP, AWS):

- Update the webhook URL in TradingView to point to your publicly accessible endpoint.
- Use a process manager (e.g., gunicorn, pm2) to run the bot in production mode.

#### Security Best Practices

- Keep the WEBHOOK_SECRET and Telegram bot token confidential.
- Use HTTPS for production deployments to secure webhook requests.
- Periodically rotate sensitive credentials (e.g., WEBHOOK_SECRET, TELEGRAM_BOT_TOKEN).

### Development (helpful commands for me)

- Activate the virtual environment (for windows)

```bash
.\env\Scripts\activate
```

- Run a file from root

```bash
python -m <sub-folder-name>.<file-name>
```

- Start a local dev server

```bash
uvicorn main:app --reload --port 8080
```

- Generate a new 32 byte hexadecimal string (64 characters) to use as webhook secret

```bash
openssl rand -hex 32
```
