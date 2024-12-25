import requests
import logging
from util.helpers import get_current_timestamp
from util.errors import TelegramBotError

logging.basicConfig(level=logging.INFO)


class TelegramClient:
    def __init__(self, bot_token, chat_id):
        """
        Initialize the TelegramClient with the bot token and chat ID.
        """
        if not bot_token or not chat_id:
            raise TelegramBotError("Bot token and chat ID must be provided.")
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message):
        """
        Send a message to the Telegram chat via a configured Telegram bot.
        """
        if not message:
            raise TelegramBotError("Message content cannot be empty.")

        payload = {"chat_id": self.chat_id, "text": message}
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            if response.status_code == 200:
                logging.info(
                    f"Message: '{message}' sent successfully to Telegram at {get_current_timestamp()}"
                )
                return True
            else:
                error_message = (
                    f"Failed to send message to Telegram. Status Code: {response.status_code}, "
                    f"Response: {response.text}"
                )
                raise TelegramBotError(error_message)
        except requests.exceptions.Timeout:
            raise TelegramBotError("Request to Telegram API timed out.")
        except requests.exceptions.RequestException as e:
            raise TelegramBotError(f"An error occurred while sending the message: {e}")
