import logging


class TradeBotError(Exception):
    """
    Custom exception class for TradeBot-specific errors.
    """

    def __init__(self, message):
        super().__init__(message)
        logging.error(message)


class TelegramBotError(Exception):
    """
    Custom exception class for Telegram bot-specific errors.
    """

    def __init__(self, message):
        super().__init__(message)
        logging.error(message)
