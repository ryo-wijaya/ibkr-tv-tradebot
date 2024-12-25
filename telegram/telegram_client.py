import requests
import logging

from util.helpers import get_current_timestamp


logging.basicConfig(level=logging.INFO)


class TelegramClient:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_message(self, message):
        """
        Send a message to the Telegram chat via a configured Telegram bot.
        """
        payload = {"chat_id": self.chat_id, "text": message}
        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                logging.info(
                    f"Message: '{message}' sent successfully to Telegram at {get_current_timestamp()}"
                )
                return True
            else:
                logging.error(f"Failed to send message: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False
