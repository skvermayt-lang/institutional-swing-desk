import json
import os

TRADES_FILE = "open_trades.json"


def load_trades():
    if not os.path.exists(TRADES_FILE):
        return []

    with open(TRADES_FILE, "r") as f:
        return json.load(f)


def save_trades(trades):
    with open(TRADES_FILE, "w") as f:
        json.dump(trades, f)


def is_trade_active(symbol):
    trades = load_trades()
    for t in trades:
        if t["symbol"] == symbol:
            return True
    return False


def register_trade(trade):
    trades = load_trades()
    trades.append(trade)
    save_trades(trades)


def remove_trade(symbol):
    trades = load_trades()
    trades = [t for t in trades if t["symbol"] != symbol]
    save_trades(trades)
