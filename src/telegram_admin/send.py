from datetime import datetime
from decimal import Decimal

import requests

TELEGRAM_TOKEN = '6511068813:AAH87e6RbHYy6rXlumEX7KsmNqpvC1d_cxg'
CHAT_ID = '1165117404'

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=payload)


def custom_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, Decimal):
        return str(o)
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
