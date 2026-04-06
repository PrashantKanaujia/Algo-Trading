from backtest.engine import BacktestEngine
from backtest.strategy import SMAStrategy
from backtest.data_loader import load_multiple_csv

def walk_forward(df):

    window_size = int(len(df) * 0.5)   # 50% train
    test_size = int(len(df) * 0.2)     # 20% test
    step = test_size                   # shift each time

    all_results = []

    start = 0

    while start + window_size + test_size <= len(df):

        train_df = df.iloc[start : start + window_size]
        test_df = df.iloc[start + window_size : start + window_size + test_size]

        print(f"\nWindow starting at index {start}")

        # 🔹 optimize on train
        results = []

        for fast in range(10,30,3):
            for slow in range(40,60,3):

                if fast >= slow:
                    continue

                strategy = SMAStrategy(fast, slow)
                data = strategy.apply_indicators(train_df.copy())

                engine = BacktestEngine(data, strategy)
                res = engine.run()

                results.append({
                    "fast": fast,
                    "slow": slow,
                    "pf": float(res["Profit Factor"])
                })

        # 🔹 picking top 3
        top_params = sorted(results, key=lambda x: x["pf"], reverse=True)[:3]

        print("Top params:", top_params)

        # 🔹 test each on unseen data
        for p in top_params:
            strategy = SMAStrategy(p["fast"], p["slow"])
            data = strategy.apply_indicators(test_df.copy())

            engine = BacktestEngine(data, strategy)
            result = engine.run()

            print(f'Test ({p["fast"]},{p["slow"]}) → {result["Total Return %"]}')

            all_results.append(result)

        #  move window
        start += step

    return all_results

import numpy as np

def summarize_results(all_results):

    if not all_results:
        print("No results to summarize")
        return

    returns = [float(r["Total Return %"]) for r in all_results]
    sharpe = [float(r.get("Sharpe Ratio", 0)) for r in all_results]
    drawdown = [float(r["Max Drawdown %"]) for r in all_results]
    trades = [r["Total Trades"] for r in all_results]

    print("\n===== WALK-FORWARD SUMMARY =====")

    print("\n--- RETURNS ---")
    print("Mean Return:", round(np.mean(returns), 3))
    print("Median Return:", round(np.median(returns), 3))
    print("Best Return:", round(max(returns), 3))
    print("Worst Return:", round(min(returns), 3))

    print("\n--- SHARPE ---")
    print("Mean Sharpe:", round(np.mean(sharpe), 3))
    print("Median Sharpe:", round(np.median(sharpe), 3))

    print("\n--- DRAWDOWN ---")
    print("Avg Drawdown:", round(np.mean(drawdown), 3))
    print("Worst Drawdown:", round(max(drawdown), 3))

    print("\n--- TRADES ---")
    print("Avg Trades:", int(np.mean(trades)))

if __name__ == "__main__":
    df = load_multiple_csv("historical_data")
    all_results=walk_forward(df)
    summarize_results(all_results)