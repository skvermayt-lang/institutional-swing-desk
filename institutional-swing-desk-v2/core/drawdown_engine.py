import json
import os

STATE_FILE = "capital_state.json"

INITIAL_CAPITAL = 200000
MAX_DRAWDOWN_ALLOWED = 0.15     # 15% hard stop
BASE_RISK = 0.01                # 1% normal risk


def load_state():

    if not os.path.exists(STATE_FILE):
        state = {
            "peak_capital": INITIAL_CAPITAL,
            "current_capital": INITIAL_CAPITAL
        }
        save_state(state)
        return state

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def update_after_trade(pnl):

    state = load_state()

    state["current_capital"] += pnl

    if state["current_capital"] > state["peak_capital"]:
        state["peak_capital"] = state["current_capital"]

    save_state(state)


def get_dynamic_risk():

    state = load_state()

    peak = state["peak_capital"]
    current = state["current_capital"]

    drawdown = (peak - current) / peak

    if drawdown >= MAX_DRAWDOWN_ALLOWED:
        return 0   # stop trading

    # Reduce risk proportionally
    adjusted_risk = BASE_RISK * (1 - drawdown * 2)

    return max(adjusted_risk, 0.003)   # never below 0.3%
