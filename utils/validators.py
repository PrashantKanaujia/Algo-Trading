def validate_symbol(symbol: str):
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    return symbol.upper()


def validate_side(side: str):
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side


def validate_order_type(order_type: str):
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT","TAKE_PROFIT_MARKET","STOP_MARKET"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: float):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    return quantity


def validate_price(price, order_type: str):
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("LIMIT orders require a valid price")
    return price
