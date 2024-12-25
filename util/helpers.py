from datetime import datetime
import pytz


def get_current_timestamp():
    """
    Get the current timestamp in Singapore time in the format of "hh:mm AM/PM dd/mm/yy"
    """
    sgt = pytz.timezone("Asia/Singapore")
    current_time = datetime.now(sgt)
    return current_time.strftime("%I:%M %p %d/%m/%y")


def format_telegram_trade_notification(symbol, quantity, status):
    return (
        "🚨 Stop-loss Trade Alert 🚨\n"
        "======================\n"
        f"Symbol: {symbol}\n"
        f"Quantity: {quantity}\n"
        f"Status: {status}\n"
    )


def format_telegram_error_notification(endpoint, error_message):
    return (
        "⚠️ Error Notification ⚠️\n"
        "===================\n"
        f"Endpoint: {endpoint}\n"
        f"Error: {error_message}\n"
    )
