from data_engine.price_loader import load_price
from core.signal_engine import generate_signal
from core.oi_engine import get_oi_data
from core.capital_engine import build_trade_plan
from core.portfolio_engine import can_take_trade
from core.telegram_engine import send_message
from core.trade_memory_engine import is_trade_active, register_trade
from core.exit_tracker_engine import check_trade_exits


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

    print("RUNNING TRADE MANAGEMENT...")

    # STEP 1 — check exits first
    check_trade_exits()

    print("SCANNING FOR NEW TRADES...")

    for symbol in WATCHLIST:

        try:
            if is_trade_active(symbol):
                continue

            df = load_price(symbol)
            oi = get_oi_data(symbol)

            signal = generate_signal(df, oi, symbol)

            if not signal:
                continue

            trade = build_trade_plan(
                symbol=signal["symbol"],
                entry=signal["entry"],
                atr=signal["atr"],
                direction=signal["direction"]
            )

            if trade is None:
                print("Trading halted due to drawdown")
                return

            if not can_take_trade(trade):
                continue

            register_trade(trade)

            message = f"""
SWING TRADE SIGNAL

Stock: {trade['symbol']}
Direction: {trade['direction']}

Entry: {trade['entry']}
Stop: {trade['stop']}
Target: {trade['target']}

Qty: {trade['quantity']}
Capital Used: ₹{trade['capital_used']}
Risk: ₹{trade['risk_amount']}
"""

            print(message)
            send_message(message)

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
