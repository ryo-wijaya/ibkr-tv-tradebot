import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(key, required=True, default=None):
    """
    Validate and return the value of an environment variable.
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise EnvironmentError(
            f"Required environment variable '{key}' is missing from application runtime."
        )
    return value


# IBKR Configuration
IBKR_HOST = get_env_variable("IBKR_HOST")
IBKR_PORT = int(get_env_variable("IBKR_PORT"))
CLIENT_ID = int(get_env_variable("CLIENT_ID"))
WEBHOOK_SECRET = get_env_variable("WEBHOOK_SECRET")

# Telegram Configuration
TELEGRAM_BOT_TOKEN = get_env_variable("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = get_env_variable("TELEGRAM_CHAT_ID")
