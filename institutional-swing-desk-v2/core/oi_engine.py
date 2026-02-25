def oi_strength(oi_df,symbol):

    s=oi_df[oi_df["SYMBOL"]==symbol]
    if s.empty:
        return False

    return s["CHG_IN_OI"].iloc[0] > 0