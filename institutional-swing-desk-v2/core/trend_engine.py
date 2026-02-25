def trend_filter(df):

    if len(df) < 20:
        return False

    ema20 = df["Close"].ewm(span=20).mean()

    latest_close = float(df["Close"].iloc[-1])
    latest_ema = float(ema20.iloc[-1])

    return latest_close > latest_ema