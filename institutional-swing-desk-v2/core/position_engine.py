import math

# ===== SYSTEM CAPITAL CONFIG =====
ACCOUNT_CAPITAL = 200000
RISK_PER_TRADE = 0.015
ATR_STOP_MULTIPLIER = 1.5
ATR_TARGET_MULTIPLIER = 3
MAX_OPEN_POSITIONS = 5


def build_trade_plan(symbol, entry, atr, direction):

    stop_distance = atr * ATR_STOP_MULTIPLIER

    if direction == "LONG":
        stop = entry - stop_distance
        target = entry + (atr * ATR_TARGET_MULTIPLIER)
    else:
        stop = entry + stop_distance
        target = entry - (atr * ATR_TARGET_MULTIPLIER)

    risk_amount = ACCOUNT_CAPITAL * RISK_PER_TRADE

    quantity = math.floor(risk_amount / stop_distance)

    capital_used = quantity * entry

    rr = abs(target - entry) / abs(entry - stop)

    return {
        "symbol": symbol,
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "target": round(target, 2),
        "atr": round(atr, 2),
        "quantity": quantity,
        "capital_used": round(capital_used, 2),
        "risk_amount": round(risk_amount, 2),
        "rr": round(rr, 2),
        "direction": direction
    }
