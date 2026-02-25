import requests

BOT_TOKEN = "8547730307:AAFgbHvJt93xFkWeXtp1AWFBWnnNvPILrMQ"
CHAT_ID = "8367543111"

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=payload)