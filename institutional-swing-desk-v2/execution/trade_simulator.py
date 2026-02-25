from data_engine.price_loader import load_price

def simulate(trade, date):

    df = load_price(trade["symbol"])
    df = df[df.index > date]

    entry = trade["entry"]
    atr = trade["atr"]
    direction = trade["direction"]

    stop = entry - atr if direction == "LONG" else entry + atr
    target = entry + 2*atr if direction == "LONG" else entry - 2*atr

    holding_days = 7
    days_passed = 0

    for _, row in df.iterrows():

        days_passed += 1

        # STOP
        if direction == "LONG" and row["Low"] <= stop:
            return stop

        if direction == "SHORT" and row["High"] >= stop:
            return stop

        # TARGET
        if direction == "LONG" and row["High"] >= target:
            return target

        if direction == "SHORT" and row["Low"] <= target:
            return target

        # TIME EXIT
        if days_passed >= holding_days:
            return float(row["Close"])

    return None