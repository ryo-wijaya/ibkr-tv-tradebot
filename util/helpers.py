from datetime import datetime
import pytz


def get_current_timestamp():
    """
    Get the current timestamp in Singapore time in the format of "hh:mm AM/PM dd/mm/yy"
    """
    sgt = pytz.timezone("Asia/Singapore")
    current_time = datetime.now(sgt)
    return current_time.strftime("%I:%M %p %d/%m/%y")
