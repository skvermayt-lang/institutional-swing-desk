from data_engine.price_loader import load_price
from core.signal_engine import generate_signal
from core.oi_engine import get_oi_data
from core.capital_engine import build_trade_plan
from core.telegram_engine import send_message

WATCHLIST = [
    "RELIANCE",
    "SBIN",
    "ICICIBANK",
    "LT",
    "TATASTEEL",
    "JSWSTEEL",
    "ADANIPORTS"
]


def run_live_scan():

    print("SCANNING LIVE MARKET...")

    signals_found = 0

    for symbol in WATCHLIST:

        try:
            df = load_price(symbol)
            oi = get_oi_data(symbol)

            signal = generate_signal(df, oi, symbol)

            if signal:

                trade = build_trade_plan(
                    symbol=signal["symbol"],
                    entry=signal["entry"],
                    atr=signal["atr"],
                    direction=signal["direction"]
                )

                message = f"""
SWING TRADE SIGNAL

Stock: {trade['symbol']}
Direction: {trade['direction']}

Entry: {trade['entry']}
Stop: {trade['stop']}
Target: {trade['target']}

Quantity: {trade['quantity']}
Capital Used: ₹{trade['capital_used']}
Risk: ₹{trade['risk_amount']}

R:R = 1:{trade['rr']}
"""

                print(message)
                send_message(message)

                signals_found += 1

        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    print(f"Total signals today: {signals_found}")
