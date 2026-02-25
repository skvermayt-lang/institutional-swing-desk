MAX_OPEN_POSITIONS = 3
MAX_CAPITAL_EXPOSURE = 0.40   # 40% of total capital

TOTAL_CAPITAL = 200000

open_positions = []
current_capital_used = 0


def can_take_trade(trade):

    global current_capital_used

    if len(open_positions) >= MAX_OPEN_POSITIONS:
        return False

    projected_capital = current_capital_used + trade["capital_used"]

    if projected_capital > TOTAL_CAPITAL * MAX_CAPITAL_EXPOSURE:
        return False

    for pos in open_positions:
        if pos["symbol"] == trade["symbol"]:
            return False

    return True


def register_trade(trade):
    global current_capital_used

    open_positions.append(trade)
    current_capital_used += trade["capital_used"]
