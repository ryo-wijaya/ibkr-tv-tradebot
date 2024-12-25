from ib_insync import IB, Stock
import logging
from config import IBKR_HOST, IBKR_PORT, CLIENT_ID, WEBHOOK_SECRET
from util.errors import TradeBotError


class IBKRClient:
    def __init__(self):
        self.host = IBKR_HOST
        self.port = IBKR_PORT
        self.client_id = CLIENT_ID
        self.secret_key = WEBHOOK_SECRET
        self.ib = IB()
        self.connected = False

    def connect(self, retries=3):
        """
        Connect to the IBKR API
        """
        for attempt in range(retries):
            try:
                if not self.ib.isConnected():
                    self.ib.run(self.ib.connect(self.host, self.port, self.client_id))
                    self.connected = True
                    logging.info(f"Connected to IBKR API (Client ID: {self.client_id})")
                    return
            except Exception as e:
                self.connected = False
                logging.error(
                    f"Failed to connect to IBKR API (Attempt {attempt + 1}): {e}"
                )
        raise TradeBotError("Could not establish connection to IBKR API after retries")

    def disconnect(self):
        """
        Disconnect from the IBKR API if connected.
        """
        try:
            if self.ib.isConnected():
                self.ib.disconnect()
                self.connected = False
                logging.info("Disconnected from IBKR API")
        except Exception as e:
            raise TradeBotError(f"Error during disconnection: {e}")

    def fetch_portfolio(self):
        """
        Fetch the current portfolio from IBKR.
        """
        if not self.ib.isConnected():
            self.connect()

        try:
            portfolio = self.ib.portfolio()
            if not portfolio:
                logging.warning("Portfolio is empty.")
                return "Portfolio is empty."

            logging.info(
                f"Portfolio fetched successfully with {len(portfolio)} positions."
            )
            summary = [
                f"Symbol: {item.contract.symbol}, Quantity: {item.position}, Market Value: {item.marketValue}"
                for item in portfolio
            ]
            return "\n".join(summary)
        except Exception as e:
            raise TradeBotError(f"Error fetching portfolio from IBKR API: {e}")

    def place_market_order(self, symbol, quantity):
        """
        Place a market sell order for a specific stock immediately and ensure it executes whenever possible.
        """
        if not self.ib.isConnected():
            self.connect()

        # Validate portfolio holdings before placing the order
        portfolio = self.ib.portfolio()
        holdings = {item.contract.symbol: item.position for item in portfolio}

        if symbol not in holdings or holdings[symbol] < quantity:
            available = holdings.get(symbol, 0)
            raise TradeBotError(
                f"Insufficient shares of {symbol} to sell. Available: {available}, Requested: {quantity}"
            )

        # Qualify the stock symbol and handle invalid symbols
        try:
            contract = self.ib.qualifyContracts(Stock(symbol, "SMART", "USD"))[0]
        except IndexError:
            raise TradeBotError(f"Invalid stock symbol: {symbol}")

        logging.info(
            f"Placing market sell order: Symbol: {symbol}, Quantity: {quantity}, TIF: GTC, OutsideRTH: True"
        )

        # Create the market order
        try:
            order = self.ib.MarketOrder("SELL", quantity)
            order.tif = "GTC"  # Good 'Til Canceled
            order.outsideRth = True  # Allow trading outside regular trading hours
            trade = self.ib.placeOrder(contract, order)

            # Wait for order status update
            self.ib.sleep(2)
            logging.info(
                f"Market order placed successfully: Symbol: {symbol}, Quantity: {quantity}, Status: {trade.orderStatus.dict()}"
            )
            return trade.orderStatus.dict()
        except Exception as e:
            raise TradeBotError(f"Error placing market order for {symbol}: {e}")
