import os
import csv
from datetime import datetime ,timezone
from binance.client import Client


class PerformanceTracker:

    def __init__(self, client: Client, symbol: str):

        self.client = client
        self.symbol = symbol

        self.csv_file = "trades.csv"
        self._initialize_csv()

        self.cumulative_pnl = 0.0
        self.trade_count = 0
        self.win_count = 0
        self.loss_count = 0


    def _initialize_csv(self):

        if not os.path.exists(self.csv_file):

            with open(self.csv_file, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "symbol",
                    "trade_number",
                    "realized_pnl",
                    "cumulative_pnl",
                    "result"
                ])


    def fetch_last_realized_pnl(self):

        income = self.client.futures_income_history(
            symbol=self.symbol,
            incomeType="REALIZED_PNL",
            limit=1
        )

        if income:
            return float(income[0]["income"])

        return 0.0


    def record_trade(self):

        realized = self.fetch_last_realized_pnl()

        self.trade_count += 1
        self.cumulative_pnl += realized

        if realized > 0:
            self.win_count += 1
            result = "WIN"

        elif realized < 0:
            self.loss_count += 1
            result = "LOSS"

        else:
            result = "BREAKEVEN"

        self._write_to_csv(realized, result)
        self.print_summary(realized)


    def _write_to_csv(self, realized, result):

        with open(self.csv_file, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                self.symbol,
                self.trade_count,
                realized,
                self.cumulative_pnl,
                result
            ])


    def print_summary(self, realized):

        win_rate = (
            (self.win_count / self.trade_count) * 100
            if self.trade_count > 0 else 0
        )

        print("------------------------------------------------")
        print(f"Trade #{self.trade_count}")
        print(f"Realized PnL: {realized:.4f} USDT")
        print(f"Cumulative PnL: {self.cumulative_pnl:.4f} USDT")
        print(f"Wins: {self.win_count} | Losses: {self.loss_count}")
        print(f"Win Rate: {win_rate:.2f}%")
        print("------------------------------------------------")