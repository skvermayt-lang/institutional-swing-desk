def size_position(capital,atr):

    risk=capital*0.02
    qty=risk/atr
    return int(qty)