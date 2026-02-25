def volume_spike(df):

    avg=df["Volume"].rolling(20).mean().iloc[-1]
    return df["Volume"].iloc[-1] > 1.5*avg