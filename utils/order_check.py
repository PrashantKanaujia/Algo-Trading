import time
def is_order_filled(order):
    if order is None:
        return False

    status = order.get("status", "")

    return status == "FILLED"

import time

def wait_for_fill(client, symbol, order_id, timeout=10):
    start = time.time()

    while time.time() - start < timeout:
        try:
            order = client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )

            status = order.get("status")

            if status == "FILLED":
                return order

            elif status in ["CANCELED", "REJECTED", "EXPIRED"]:
                return None

        except Exception as e:
            print("Error checking order:", e)

        time.sleep(1)

    return None  # timeout