import pandas as pd
import glob

COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base",
    "taker_buy_quote",
    "ignore"
]

def load_multiple_csv(folder_path):

    all_files = glob.glob(f"{folder_path}/*.csv")

    dfs = []

    for file in all_files:
        df = pd.read_csv(file)

        if "open_time" not in df.columns:
            df = pd.read_csv(file, header=None)
            df.columns = COLUMNS

        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

        dfs.append(df)

    combined_df = pd.concat(dfs)
    combined_df = combined_df.sort_values("open_time")
    combined_df = combined_df.reset_index(drop=True)

    return combined_df