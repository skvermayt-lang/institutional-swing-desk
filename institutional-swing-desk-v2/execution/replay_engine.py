from data_engine.price_loader import load_price
from core.signal_engine import generate_signal
from core.oi_engine import get_oi_data
from core.capital_engine import build_trade_plan
from core.portfolio_engine import can_take_trade, register_trade
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

    print("===================================")
    print("   SCANNING LIVE MARKET")
    print("===================================")

    signals_found = 0

    for symbol in WATCHLIST:

        try:
            print(f"Scanning {symbol}...")

            # Load price data
            df = load_price(symbol)

            if df is None or len(df) < 50:
                print(f"Insufficient data for {symbol}")
                continue

            # Load OI data
            oi = get_oi_data(symbol)

            # Generate raw signal
            signal = generate_signal(df, oi, symbol)

            if not signal:
                print(f"No signal for {symbol}")
                continue

            # Build trade plan (includes drawdown control)
            trade = build_trade_plan(
                symbol=signal["symbol"],
                entry=signal["entry"],
                atr=signal["atr"],
                direction=signal["direction"]
            )

            # Drawdown engine may halt trading
            if trade is None:
                print("Trading halted due to maximum drawdown limit.")
                return

            # Portfolio risk control
            if not can_take_trade(trade):
                print(f"Trade skipped due to portfolio limits: {symbol}")
                continue

            # Register trade internally
            register_trade(trade)

            # Build Telegram message
            message = f"""
📊 SWING TRADE SIGNAL

Stock: {trade['symbol']}
Direction: {trade['direction']}

Entry: ₹{trade['entry']}
Stop: ₹{trade['stop']}
Target: ₹{trade['target']}

Quantity: {trade['quantity']}
Capital Used: ₹{trade['capital_used']}
Risk: ₹{trade['risk_amount']}

Risk-Reward: 1:{trade['rr']}
"""

            print(message)
            send_message(message)

            signals_found += 1

        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    print("===================================")
    print(f"Total signals today: {signals_found}")
    print("===================================")
