import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(plan):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials missing")
        return

    message = f"""
📊 SWING SIGNAL — {plan['symbol']}

Direction: {plan['direction']}

Entry: ₹{plan['entry']}
Stop: ₹{plan['stop']}
Target: ₹{plan['target']}

ATR: {plan['atr']}

Position Size: {plan['quantity']} shares
Capital Used: ₹{plan['capital_used']}

Risk Per Trade: ₹{plan['risk_amount']}
Risk Reward: 1 : {plan['rr']}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)
