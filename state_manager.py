import json
import time
import os
from pathlib import Path

STATE_DIR = Path("State")
STATE_DIR.mkdir(exist_ok=True)
print("CURRENT DIR:", os.getcwd())
print("FILES:", os.listdir())

def write_json(filename, data):
    path = STATE_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def read_json(filename, default=None):

    path = STATE_DIR / filename

    print("Trying to open:", filename)
    print("Absolute path:", path.resolve())
    print("Exists:", path.exists())

    if not path.exists():
        return {} if default is None else default

    try:
        with open(path) as f:
            return json.load(f)

    except Exception as e:
        print("JSON ERROR:", e)
        return {} if default is None else default
    


def save_open_position(symbol, side, price, qty):

    trade = {
        "symbol": symbol,
        "side": side,
        "entry_price": price,
        "qty": qty,
        "entry_time": time.time()
    }

    write_json("open_position.json", trade)


import time

def close_position(exit_price):

    trade = read_json("open_position.json")

    if not trade:
        return None

    entry_price = float(trade["entry_price"])
    qty = float(trade["qty"])
    side = trade["side"]

    if side == "LONG":
        pnl = (exit_price - entry_price) * qty
    else:
        pnl = (entry_price - exit_price) * qty

    closed_trade = {
        "symbol": trade["symbol"],
        "side": side,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "qty": qty,
        "pnl": pnl,
        "entry_time": trade["entry_time"],
        "exit_time": time.time()
    }

    # store trade history
    history = read_json("closed_trades.json", [])
    history.append(closed_trade)
    write_json("closed_trades.json", history)

    # update stats
    stats = read_json("stats.json", {
        "total_trades": 0,
        "wins": 0,
        "losses": 0,
        "win_rate": 0,
        "total_pnl": 0
    })

    stats["total_trades"] += 1
    stats["total_pnl"] += pnl

    if pnl > 0:
        stats["wins"] += 1
    else:
        stats["losses"] += 1

    stats["win_rate"] = (stats["wins"] / stats["total_trades"]) * 100

    write_json("stats.json", stats)

    write_json("open_position.json", None)

    return