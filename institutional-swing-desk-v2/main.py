from data_engine.fo_universe_loader import load_fo_universe
from data_engine.price_loader import load_price
from data_engine.bhavcopy_loader import load_oi
from core.signal_engine import generate_signal
from core.position_engine import size_position
from core.telegram_engine import send_message

import pandas as pd

CAPITAL = 100000


def score_signal(df, atr):
    volume_strength = df["Volume"].iloc[-1] / df["Volume"].rolling(20).mean().iloc[-1]
    range_strength = (df["High"].iloc[-1] - df["Low"].iloc[-1]) / atr
    return volume_strength + range_strength


def run_live_scan():

    today = pd.Timestamp.today().normalize()

    universe = load_fo_universe()
    oi = load_oi(today)

    signals = []

    for s in universe:

        df = load_price(s)
        if df is None or len(df) < 40:
            continue

        signal = generate_signal(df, oi, s)

        if signal:

            atr = float(signal["atr"])
            entry = float(signal["entry"])
            direction = signal["direction"]

            stop = entry - atr if direction == "LONG" else entry + atr
            target = entry + 2*atr if direction == "LONG" else entry - 2*atr

            qty = size_position(CAPITAL, atr)

            score = score_signal(df, atr)

            signals.append({
                "symbol": s,
                "direction": direction,
                "entry": round(entry, 2),
                "stop": round(stop, 2),
                "target": round(target, 2),
                "qty": qty,
                "score": score
            })

    if len(signals) == 0:
        send_message("No swing setups today.")
        return

    # Sort by score descending
    signals = sorted(signals, key=lambda x: x["score"], reverse=True)

    top_signals = signals[:3]

    message = "*TOP SWING SETUPS TODAY*\n\n"

    for i, s in enumerate(top_signals, start=1):
        message += (
            f"{i}) {s['symbol']} - {s['direction']}\n"
            f"Entry: {s['entry']}\n"
            f"Stop: {s['stop']}\n"
            f"Target: {s['target']}\n"
            f"Qty: {s['qty']}\n\n"
        )

    send_message(message)


if __name__ == "__main__":
    run_live_scan()