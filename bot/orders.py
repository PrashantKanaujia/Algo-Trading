from bot.client import client
import os
from utils.logger import logger


def place_order(symbol, side, order_type, quantity, price=None):

    # logger=setup_logger()

    logger.info(
        f"Request -> Symbol: {symbol}, Side: {side}, "
        f"Type: {order_type}, Quantity: {quantity}, Price: {price}"
    )
    try:
        if order_type == "MARKET":

            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity,
                reduce_only=True
            )
            print(side,quantity,order_type)
            logger.info(f"Order placed successfully: {response}")
            return response

        elif order_type == "LIMIT":

            if price is None:
                raise ValueError("LIMIT order requires price")

            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC",
                reduce_only=True
            )
            print(side,quantity,order_type)

            logger.info(f"Order placed successfully: {response}")
            return response
        
        elif order_type == "STOP_MARKET":

            if price is None:
                raise ValueError("STOP_MARKET requires stop price")

            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                stopPrice=price,
                closePosition=False,
                reduceOnly=True,
                workingType="CONTRACT_PRICE"
            )
            print(side,quantity,order_type)

            logger.info(f"Order placed successfully: {response}")
            return response
        
        elif order_type == "TAKE_PROFIT_MARKET":
            if price is None:
                raise ValueError("TAKE_PROFIT_MARKET requires trigger price")

            response = client.futures_create_order(
                symbol=symbol,
                side=side,          
                type="TAKE_PROFIT_MARKET",
                stopPrice=price,     
                closePosition=False,
                reduceOnly=True,     
                workingType="CONTRACT_PRICE"
            )
            print(side,quantity,order_type)

            logger.info(f"Order placed successfully: {response}")
            return response

    except Exception as e:
        logger.error(f"Order failed: {str(e)}")
        raise


def place_bracket_order(client, symbol, side, qty, entry_price,
                        sl_percent=0.02, tp_percent=0.04):

    # Calculate SL / TP
    if side == "BUY":
        sl_price = entry_price * (1 - sl_percent)
        tp_price = entry_price * (1 + tp_percent)
        exit_side = "SELL"

    else:  # SHORT
        sl_price = entry_price * (1 + sl_percent)
        tp_price = entry_price * (1 - tp_percent)
        exit_side = "BUY"

    # STOP LOSS
    client.create_order(
        symbol=symbol,
        side=exit_side,
        type="STOP_MARKET",
        stopPrice=round(sl_price, 2),
        quantity=qty
    )

    # TAKE PROFIT
    client.create_order(
        symbol=symbol,
        side=exit_side,
        type="TAKE_PROFIT_MARKET",
        stopPrice=round(tp_price, 2),
        quantity=qty
    )