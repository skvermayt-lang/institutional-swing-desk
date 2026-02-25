import pandas as pd
import os

OI_DATA_PATH = "data_oi"


def get_oi_data(symbol):

    """
    Loads latest Open Interest classification for a symbol.
    If not available, returns neutral OI state.
    """

    try:
        file_path = os.path.join(OI_DATA_PATH, "oi_latest.csv")

        if not os.path.exists(file_path):
            return {
                "symbol": symbol,
                "oi_trend": "NEUTRAL",
                "oi_change": 0
            }

        df = pd.read_csv(file_path)

        df_symbol = df[df["SYMBOL"] == symbol]

        if df_symbol.empty:
            return {
                "symbol": symbol,
                "oi_trend": "NEUTRAL",
                "oi_change": 0
            }

        latest = df_symbol.iloc[-1]

        return {
            "symbol": symbol,
            "oi_trend": latest.get("classification", "NEUTRAL"),
            "oi_change": latest.get("oi_change", 0)
        }

    except Exception as e:
        print(f"OI load error for {symbol}: {e}")

        return {
            "symbol": symbol,
            "oi_trend": "NEUTRAL",
            "oi_change": 0
        }
