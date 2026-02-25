from execution.replay_engine import run_live_scan
from core.position_engine import build_trade_plan
from core.telegram_engine import send_message


def main():

    print("SCANNING LIVE MARKET...")

    signals = run_live_scan()

    if not signals:
        print("No valid signals today.")
        return

    for s in signals:

        plan = build_trade_plan(
            symbol=s["symbol"],
            entry=s["entry"],
            atr=s["atr"],
            direction=s["direction"]
        )

        send_message(plan)

    print(f"Total Signals Sent: {len(signals)}")


if __name__ == "__main__":
    main()
