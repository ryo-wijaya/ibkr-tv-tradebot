### Info

Trading bot that exposes webhooks meant to be used to connect TradingView alerts with Interactive Brokers, providing the ability to trigger round-the-clock stop loss strategies.

Meant to be hosted on GCP.

### Features

Each trade/account interaction with IBKR will result in a Telegram notification.

**Planned Webhooks:**

1. Fetch current holdings and send the data via Telegram to a user (smoke test for IBKR Trading API).
2. Create a sell order at market price for a specific share at a specific quantity.

### Setup

1. Setup a telegram bot via BotFather. Retrieve the bot token, start a chat, and retrieve the chat id.

### Development

1. Run a file from root

```py
    python -m <sub-folder-name>.<file-name>
```
