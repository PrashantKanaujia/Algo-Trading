import pandas as pd

class SMAStrategy:

    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def apply_indicators(self, df):

        df["sma_short"] = df["close"].rolling(self.short_window).mean()
        df["sma_long"] = df["close"].rolling(self.long_window).mean()

        return df
    
    def generate_signal(self, df, i):

        # skip until indicators valid
        if i == 0:
            return None

        prev_short = df["sma_short"].iloc[i - 1]
        prev_long = df["sma_long"].iloc[i - 1]
        curr_short = df["sma_short"].iloc[i]
        curr_long = df["sma_long"].iloc[i]

        # Avoid NaN zone
        if any(pd.isna([prev_short, prev_long, curr_short, curr_long])):
            return None

        # Bullish crossover
        if prev_short < prev_long and curr_short > curr_long:
            if abs(curr_short - curr_long) / curr_long > 0.0001:
                return "LONG"

        # Bearish crossover
        if prev_short > prev_long and curr_short < curr_long:
                if abs(curr_short - curr_long) / curr_short > 0.0001:
                    return "SHORT"

        return None