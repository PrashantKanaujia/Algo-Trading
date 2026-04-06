MAX_TRADE_USDT = 300  # change as needed


def validate_position_size(quantity, price):
    position_value = quantity * price

    if position_value > MAX_TRADE_USDT:
        raise ValueError(
            f"Trade value {position_value} exceeds max allowed {MAX_TRADE_USDT} USDT"
        )
