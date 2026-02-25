import pandas as pd
from data_engine.fo_universe_loader import load_fo_universe
from data_engine.price_loader import load_price
from data_engine.bhavcopy_loader import load_oi

from core.signal_engine import generate_signal
from core.position_engine import size_position
from execution.trade_simulator import simulate


class Replay:

    def run(self):

        capital = 100000
        universe = load_fo_universe()

        days = pd.date_range("2023-01-01", "2023-12-31", freq="B")

        for d in days:

            print("Processing", d.date())

            oi = load_oi(d)
            if oi is None:
                continue

            for s in universe:

                df = load_price(s)
                if df is None:
                    continue

                df = df[df.index <= d]

                if len(df) < 40:
                    continue

                signal = generate_signal(df, oi, s)
                if signal is None:
                    continue

                qty = size_position(capital, signal["atr"])

                exit_price = simulate(signal, d)
                if exit_price is None:
                    continue

                pnl = (exit_price - signal["entry"]) * qty
                capital += pnl

                print("TRADE:", s, pnl, "Capital:", capital)