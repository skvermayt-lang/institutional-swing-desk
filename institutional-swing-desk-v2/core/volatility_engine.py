def atr(df):

    tr=(df["High"]-df["Low"]).rolling(14).mean()
    return tr.iloc[-1]