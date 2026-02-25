import yfinance as yf
import pandas as pd
from core.signal_engine import generate_signal


WATCHLIST = [
    "RELIANCE",
    "SBIN",
    "ICICIBANK",
    "LT",
    "TATASTEEL",
    "JSWSTEEL",
    "ADANIPORTS"
]


def fetch_price(symbol):
    df = yf.download(symbol + ".NS", period="3mo", interval="1d", progress=False)
    df.dropna(inplace=True)
    return df


def calculate_atr(df, period=14):
    high_low = df["High"] - df["Low"]
    high_close = abs(df["High"] - df["Close"].shift())
    low_close = abs(df["Low"] - df["Close"].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    atr = true_range.rolling(period).mean().iloc[-1]
    return float(atr)


def run_live_scan():

    signals = []

    for symbol in WATCHLIST:

        try:
            df = fetch_price(symbol)

            if len(df) < 50:
                continue

            signal = generate_signal(df)

            if not signal:
                continue

            atr = calculate_atr(df)

            signals.append({
                "symbol": symbol,
                "entry": float(df["Close"].iloc[-1]),
                "atr": atr,
                "direction": signal
            })

        except Exception as e:
            print("Error processing", symbol, e)

    return signals
