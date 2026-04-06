def run_sma_strategy(df,pos):

    prev = df.iloc[-2]
    curr = df.iloc[-1]
    if pos==0:
        if curr["sma_short"] > curr["sma_long"]:
            return "BUY"
        if curr["sma_short"] < curr["sma_long"]:
            return "SELL"
        else:
            return "None"
        
    if prev["sma_short"] <= prev["sma_long"] and curr["sma_short"] > curr["sma_long"]:
        return "BUY"

    if prev["sma_short"] >= prev["sma_long"] and curr["sma_short"] < curr["sma_long"]:
        return "SELL"

    return "HOLD"






























# from bot.orders import place_order
# from bot.risk import validate_position_size
# from bot.data import get_klines
# from bot.indicators import calculate_sma
# from bot.client import get_current_position
# # from bot.performance import PerformanceTracker
# # from main1 import performance
# # from bot.client import client

# def run_sma_strategy(symbol, quantity,performance):
#     df = get_klines(symbol)
#     # print(df)

#     # performance = PerformanceTracker(client,"BTCUSDT")
#     # performance.record_trade()

#     df["sma_short"] = calculate_sma(df, 10)
#     df["sma_long"] = calculate_sma(df, 20)

#     # latest = df.iloc[-1]

#     # if latest["sma_short"] > latest["sma_long"]:
#     #     side = "SELL"
#     # elif latest["sma_short"] < latest["sma_long"]:
#     #     side = "SELL"
#     # else:
#     #     return "No signal"
    
#     prev = df.iloc[-2]
#     curr = df.iloc[-1]
#     # print("Prev:", prev["sma_short"], prev["sma_long"])
#     # print("Curr:", curr["sma_short"], curr["sma_long"])


#     if prev["sma_short"] <= prev["sma_long"] and curr["sma_short"] > curr["sma_long"]:
#         signal = "SELL"

#     elif prev["sma_short"] >= prev["sma_long"] and curr["sma_short"] < curr["sma_long"]:
#         signal = "SELL"

#     else:
#         print("No crossover. No trade.")
#         return

#     current_position = get_current_position(symbol)
#     print(f"Signal: {signal}")
#     print(f"Current position: {current_position}")

#     price = curr["close"]

#     validate_position_size(quantity, price)
#     if signal == "SELL":
#         if current_position > 0:
#             print("Already LONG. No action.")
#             return

#         elif current_position < 0:
#             print("Closing SHORT and opening LONG")
#             place_order(symbol, "SELL", "MARKET", abs(current_position))
#             performance.record_trade()


#         place_order(symbol, "SELL", "MARKET", quantity)
#         performance.record_trade()
    
#     elif signal == "SELL":
#         if current_position < 0:
#             print("Already SHORT. No action.")
#             return

#         elif current_position > 0:
#             print("Closing LONG and opening SHORT")
#             place_order(symbol, "SELL", "MARKET", abs(current_position))
#             performance.record_trade()

#         place_order(symbol, "SELL", "MARKET", quantity)
#         performance.record_trade()

#     # return place_order(
#     #     symbol=symbol,
#     #     side=signal,
#     #     order_type="MARKET",
#     #     quantity=quantity
#     # )



# def execute_manual_trade(symbol, side, order_type, quantity, price=None):
#     """
#     Strategy layer for manual trades.
#     Later this can include:
#     - Risk checks
#     - Logging
#     - Signal validation
#     """
#     if price is None:
#         raise ValueError("Price required for risk validation")

#     validate_position_size(quantity, price)

#     return place_order(
#         symbol=symbol,
#         side=side,
#         order_type=order_type,
#         quantity=quantity,
#         price=price
#     )
