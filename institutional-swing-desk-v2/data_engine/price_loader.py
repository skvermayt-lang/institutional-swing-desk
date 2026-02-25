import yfinance as yf
import pandas as pd
import os

CACHE = "data_price"

def load_price(symbol):

    os.makedirs(CACHE, exist_ok=True)
    f = f"{CACHE}/{symbol}.csv"

    # ---------- LOAD OR DOWNLOAD ----------
    if os.path.exists(f):
        df = pd.read_csv(f)
    else:
        df = yf.download(symbol + ".NS", period="5y", interval="1d")
        df.to_csv(f)

    # ---------- FIX MULTI-LEVEL COLUMNS ----------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ---------- DATE INDEX NORMALIZATION ----------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
    else:
        df.index = pd.to_datetime(df.index)

    # ---------- KEEP ONLY REQUIRED COLUMNS ----------
    required = ["Open", "High", "Low", "Close", "Volume"]

    for col in required:
        if col not in df.columns:
            return None   # data invalid

    df = df[required]

    # ---------- NUMERIC CAST ----------
    for col in required:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    return df