import typer
import time
from state_manager import write_json ,read_json, save_open_position,close_position
import controller
from bot.client import get_current_position,get_futures_equity ,client
from bot.strategy import  run_sma_strategy
from utils.retry import safe_api_call
from utils.order_check import is_order_filled,wait_for_fill

from bot.data import get_klines
from bot.indicators import calculate_sma
from bot.orders import place_order ,place_bracket_order
from bot.risk import validate_position_size

from bot.Performance_Tracker import PerformanceTracker
from utils.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)


def execute_and_confirm(client, symbol, side, quantity,flag):
    order = safe_api_call(
        lambda: place_order(symbol, side, "MARKET", quantity),
        critical=True
    )

    if not order or "orderId" not in order:
        print("Invalid order response")
        return False

    filled = wait_for_fill(client, symbol, order["orderId"])

    if not filled:
        print("Order not filled / timeout")
        return False
    print(filled)

    trades_data=read_json("trades.json")
    trades_data.append({
        "ID":filled["orderId"],
        "timestamp":filled["time"],
        "symbol":filled["symbol"],
        "side":filled["side"],
        "quantity":float(filled["executedQty"]),
        "price":float(filled["price"]),
        "avgPrice":float(filled["avgPrice"]),
        "cumQuote":float(filled["cumQuote"])
    })
    write_json("trades.json",trades_data)
    print("Order filled:", filled["executedQty"])

    if flag=="open":
        save_open_position(symbol,side,float(filled["avgPrice"]),float(filled["executedQty"]))
    elif flag=="close":
        close_position(float(filled["avgPrice"]))
    return True

app = typer.Typer(help="Binance Futures Trading Bot CLI")


# AUTO STRATEGY
def run_bot(symbol: str = "BTCUSDT", quantity: float = 0.002, interval: int = 60):
    """
    Run SMA strategy continuously.
    """
    print(f"Starting automated strategy for {symbol}")
    performance=PerformanceTracker(client,"BTCUSDT")

    last_trade_time = 0
    cooldown = 30   
    while True:
        
        if not controller.bot_running:
            time.sleep(2)
            continue
        
        current_time = time.time()

        if current_time - last_trade_time < cooldown:
            print("Cooldown active, skipping trade")
            time.sleep(interval)
            continue
        try:
            trade_executed=False
            # 1. Fetch market data
            df = safe_api_call(lambda:get_klines(symbol))

            # 2. Calculate indicators
            df["sma_short"] = calculate_sma(df, 10)
            df["sma_long"] = calculate_sma(df, 20)

            current_position = safe_api_call(lambda:get_current_position(symbol),critical=True)
            # 3. Get strategy signal
            signal = run_sma_strategy(df,current_position)
            print(signal)
            data = {
                "signal": signal,
                "timestamp": time.time()
                }
            write_json("signals.json", data)

            # 4. Current price
            price = df.iloc[-1]["close"]

            # 5. Check current position
            print(current_position)
            positions = [{
                "symbol": symbol,
                "size": current_position
            }]
            
            write_json("positions.json", positions)

            equity=read_json("equity.json")
            eq=safe_api_call(lambda:get_futures_equity())
            equity.append({
            "time": time.time(),          
            "equity": eq["equity"]   
        })
            
            write_json("equity.json",equity)

            

            print(f"Signal: {signal}")
            print(f"Position: {current_position}")

            # 6. Risk check
            validate_position_size(quantity, price)

            # 7. Trading logic
            if signal == "BUY":

                if current_position > 0:
                    print("Already LONG")

                elif current_position < 0:
                    print("Closing SHORT")

                    if not execute_and_confirm(client, symbol, "BUY", abs(current_position),"close"):
                        continue
                    performance.record_trade()

                    if not execute_and_confirm(client, symbol, "BUY", quantity,"open"):
                        continue
                    performance.record_trade()

                    trade_executed = True

                else:
                    if not execute_and_confirm(client, symbol, "BUY", quantity,"open"):
                        continue
                    performance.record_trade()

                    trade_executed = True


            elif signal == "SELL":

                if current_position < 0:
                    print("Already SHORT")

                elif current_position > 0:
                    print("Closing LONG")
                    if not execute_and_confirm(client, symbol, "SELL", abs(current_position),"close"):
                        continue
                    performance.record_trade()

                    if not execute_and_confirm(client, symbol, "SELL", quantity,"open"):
                        continue
                    performance.record_trade()

                    trade_executed = True

                else:
                    if not execute_and_confirm(client, symbol, "SELL", quantity,"open"):
                        continue
                    performance.record_trade()

                    trade_executed = True
                    

            else:
                print("No signal")

            if trade_executed:
                last_trade_time = current_time
            print("Cycle complete.")
            time.sleep(interval)

        except Exception as e:
            print("Error in auto mode:", e)
            time.sleep(10)
       

if __name__ == "__main__":
    app()

