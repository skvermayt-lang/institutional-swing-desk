from core.trade_memory_engine import load_trades, remove_trade
from core.drawdown_engine import update_after_trade
from data_engine.price_loader import load_price


def check_trade_exits():

    trades = load_trades()

    for trade in trades:

        symbol = trade["symbol"]
        df = load_price(symbol)

        if df is None:
            continue

        latest_price = float(df["Close"].iloc[-1])

        entry = trade["entry"]
        stop = trade["stop"]
        target = trade["target"]
        qty = trade["quantity"]

        pnl = 0
        exit_reason = None

        if trade["direction"] == "LONG":

            if latest_price <= stop:
                pnl = (stop - entry) * qty
                exit_reason = "STOP HIT"

            elif latest_price >= target:
                pnl = (target - entry) * qty
                exit_reason = "TARGET HIT"

        else:

            if latest_price >= stop:
                pnl = (entry - stop) * qty
                exit_reason = "STOP HIT"

            elif latest_price <= target:
                pnl = (entry - target) * qty
                exit_reason = "TARGET HIT"

        if exit_reason:
            print(f"{symbol} exited: {exit_reason}")
            update_after_trade(pnl)
            remove_trade(symbol)
