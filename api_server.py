from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from state_manager import read_json
import controller
import threading
from main1 import run_bot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



bot_thread=None

@app.post("/start")
def start_bot():
    global bot_thread
    controller.bot_running = True

    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = threading.Thread(
            target=run_bot,
            args=("BTCUSDT", 0.002, 60),
            daemon=True
        )
        bot_thread.start()
    return {"status": "running"}

@app.post("/stop")
def stop_bot():
    controller.stop()
    return {"status": "stopped"}

@app.get("/bot-status")
def bot_status():
    return {"status": "running" if controller.is_running() else "stopped"}


@app.get("/positions")
def positions():
    return read_json("positions.json")

@app.get("/trades")
def trades():
    return read_json("trades.json")

@app.get("/equity")
def equity():
    return read_json("equity.json")

@app.get("/signals")
def signals():
    return read_json("signals.json")



@app.post("/close-position")
def close_position_api():
    try:
        from bot.client import get_current_position, client
        from main1 import execute_and_confirm

        symbol = "BTCUSDT"
        current_position = get_current_position(symbol)

        if current_position == 0:
            return {"status": "no position"}

        side = "SELL" if current_position > 0 else "BUY"

        success = execute_and_confirm(
            client=client,
            symbol=symbol,
            side=side,
            quantity=abs(current_position),
            flag="close"
        )

        return {"status": "closed" if success else "failed"}

    except Exception as e:
        return {"error": str(e)}






@app.get("/stats")
def get_stats():
    return read_json("stats.json")
