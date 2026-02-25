from core.drawdown_engine import get_dynamic_risk

TOTAL_CAPITAL = 200000


def calculate_position_size(capital, risk_per_trade, entry, stop):

    risk_amount = capital * risk_per_trade
    per_share_risk = abs(entry - stop)

    if per_share_risk == 0:
        return 0

    quantity = int(risk_amount / per_share_risk)
    return max(quantity, 1)


def build_trade_plan(symbol, entry, atr, direction):

    dynamic_risk = get_dynamic_risk()

    if dynamic_risk == 0:
        return None

    if direction == "LONG":
        stop = entry - atr * 1.5
        target = entry + atr * 3
    else:
        stop = entry + atr * 1.5
        target = entry - atr * 3

    quantity = calculate_position_size(
        TOTAL_CAPITAL,
        dynamic_risk,
        entry,
        stop
    )

    trade = {
        "symbol": symbol,
        "direction": direction,
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "target": round(target, 2),
        "quantity": quantity,
        "capital_used": round(quantity * entry, 2),
        "risk_amount": round(abs(entry - stop) * quantity, 2),
        "rr": 2
    }

    return trade
