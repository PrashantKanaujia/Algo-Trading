def calculate_sma(df, period):
    return df["close"].rolling(window=period).mean()
