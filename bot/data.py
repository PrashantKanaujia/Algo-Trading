import pandas as pd
from bot.client import client


def get_klines(symbol, interval="1m", limit=100):
    klines = client.futures_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )
    # print(klines)

    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])
    # print(df)

    df["close"] = df["close"].astype(float)
    return df