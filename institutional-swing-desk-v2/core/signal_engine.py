from core.trend_engine import trend_filter
from core.volatility_engine import atr


def range_expansion(df):

    if len(df) < 20:
        return False

    today_range = df["High"].iloc[-1] - df["Low"].iloc[-1]
    avg_range = (df["High"] - df["Low"]).rolling(20).mean().iloc[-1]

    return today_range > 1.3 * avg_range


def volume_event(df):

    avg = df["Volume"].rolling(20).mean().iloc[-1]
    return df["Volume"].iloc[-1] > 1.1 * avg


def generate_signal(df, oi_df, symbol):

    if not (range_expansion(df) or volume_event(df)):
        return None

    direction = "LONG" if trend_filter(df) else "SHORT"

    entry = float(df["Close"].iloc[-1])
    atr_val = atr(df)

    return {
        "symbol": symbol,
        "entry": entry,
        "atr": atr_val,
        "direction": direction
    }