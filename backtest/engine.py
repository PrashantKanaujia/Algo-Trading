import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from backtest.data_loader import load_multiple_csv
from backtest.strategy import SMAStrategy


class BacktestEngine:
    def __init__(self, df, strategy, initial_balance=1000,
                 position_percent=0.1, fee=0.0004,cd=10):

        self.df = df
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position_percent = position_percent
        self.fee = fee
        self.cooldown=cd

        self.position = None
        self.position_size = 0
        self.entry_price = 0
        
        self.stop_loss = 0.02      # 2%
        self.take_profit = 0.04    # 4%
        self.slippage = 0.001   # 0.1%
        self.equity_curve = []
        self.trades = []

    def run(self):
        cooldown=0
        for i in range(50, len(self.df)):
            if cooldown==0:
                current_price = self.df["close"].iloc[i]
                self._check_sl_tp(current_price)
                signal = self.strategy.generate_signal(self.df,i)
                if signal !=None:
                    cooldown=self.cooldown

                self._process_signal(signal, current_price)
                self._mark_to_market(current_price)
            else:
                current_price = self.df["close"].iloc[i]
                self._check_sl_tp(current_price)
                self._mark_to_market(current_price)
                cooldown-=1

        
        # close any open position at final price
        if self.position is not None:
            final_price = self.df["close"].iloc[-1]
            self._close_position(final_price)

        return self._results()
    


    
    def _process_signal(self, signal, price):

        if signal is None:
            return

        # If no position
        if self.position is None:
            self._open_position(signal, price)
            return

        # If opposite signal → flip
        if (self.position == "LONG" and signal == "SHORT") or \
        (self.position == "SHORT" and signal == "LONG"):

            self._close_position(price)
            self._open_position(signal, price)
    
    def _open_position(self, side, price):

        capital_to_use = self.balance * self.position_percent
        if side == "LONG":
            price = price * (1 + self.slippage)
        elif side == "SHORT":
            price = price * (1 - self.slippage)

        quantity = capital_to_use / price

        self.position = side
        self.position_size = quantity
        self.entry_price = price

        # fee on entry
        self.balance -= capital_to_use * self.fee

    def _close_position(self, price):

        if self.position == "LONG":
            price = price * (1 - self.slippage)
        elif self.position == "SHORT":
            price = price * (1 + self.slippage)

        if self.position == "LONG":
            pnl = (price - self.entry_price) * self.position_size
        else:
            pnl = (self.entry_price - price) * self.position_size

        trade_value = self.position_size * price
        fee_cost = trade_value * self.fee

        self.balance += pnl
        self.balance -= fee_cost

        self.trades.append({
            "entry": self.entry_price,
            "exit": price,
            "side": self.position,
            "pnl": pnl,
            "time": len(self.equity_curve)
        })

        self.position = None
        self.position_size = 0
        self.entry_price = 0


    def _check_sl_tp(self, price):

        if self.position is None:
            return

        # LONG position
        if self.position == "LONG":

            sl_price = self.entry_price * (1 - self.stop_loss)
            tp_price = self.entry_price * (1 + self.take_profit)

            if price <= sl_price:
                self._close_position(price)
                return

            elif price >= tp_price:
                self._close_position(price)
                return 

        # SHORT position
        elif self.position == "SHORT":

            sl_price = self.entry_price * (1 + self.stop_loss)
            tp_price = self.entry_price * (1 - self.take_profit)

            if price >= sl_price:
                self._close_position(price)
                return

            elif price <= tp_price:
                self._close_position(price)
                return 
    
    def _mark_to_market(self, price):

        equity = self.balance

        if self.position is not None:
            if self.position == "LONG":
                unrealized = (price - self.entry_price) * self.position_size
            else:
                unrealized = (self.entry_price - price) * self.position_size

            equity += unrealized

        self.equity_curve.append(equity)



    def _sharpe_ratio(self):

        equity = np.array(self.equity_curve)

        if len(equity) < 2:
            return 0

        returns = np.diff(equity) / equity[:-1]

        if np.std(returns) == 0:
            return 0

        sharpe = (np.mean(returns) / np.std(returns)) * np.sqrt(252)

        return sharpe

    def _results(self):

        total_return = (self.balance - self.initial_balance) / self.initial_balance * 100
        
        pnl_list = [t["pnl"] for t in self.trades]
        wins = [p for p in pnl_list if p > 0]
        losses = [p for p in pnl_list if p < 0]

        win_rate = len(wins) / len(self.trades) * 100 if self.trades else 0

        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0

        profit_factor = abs(sum(wins) / sum(losses)) if losses else 0

        expectancy = np.mean(pnl_list) if pnl_list else 0

        drawdown = self._max_drawdown()
        sharpe = self._sharpe_ratio()
        return {
            "Total Return %": round(total_return, 2),
            "Win Rate %": round(win_rate, 2),
            "Avg Win": round(avg_win, 4),
            "Avg Loss": round(avg_loss, 4),
            "Profit Factor": round(profit_factor, 2),
            "Expectancy per Trade": round(expectancy, 4),
            "Max Drawdown %": round(drawdown, 2),
            "Total Trades": len(self.trades),
            "Sharpe Ratio": round(sharpe, 2)
        }
    
    def _max_drawdown(self):

        equity = np.array(self.equity_curve)
        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak

        return abs(drawdown.min()) * 100
    
def run_backtest(cd):

    df = load_multiple_csv("historical_data")

    strategy = SMAStrategy(20, 50)
    df = strategy.apply_indicators(df)

    engine = BacktestEngine(
        df=df,
        strategy=strategy,
        initial_balance=1000,
        position_percent=0.1,
        fee=0.0004,
        cd=cd
    )

    results = engine.run()
    print("\nTrades:")
    for t in engine.trades:
        print(t)

    print("\n===== BACKTEST RESULTS =====")
    for k, v in results.items():
        print(f"{k}: {v}")
    
    pd.DataFrame(engine.trades).to_csv("trades.csv", index=False)
    plt.plot(engine.equity_curve)
    plt.title("Equity Curve")
    plt.show()
    return results["Profit Factor"]


if __name__ == "__main__":
    run_backtest(30)