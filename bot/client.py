import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    raise ValueError("API credentials not found in .env")

client = Client(api_key, api_secret)


client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"


def get_current_position(symbol):
    positions = client.futures_position_information(symbol=symbol)

    for pos in positions:
        qty = float(pos["positionAmt"])
        # print(qty)
        if qty != 0:
            return qty

    return 0.0


def get_futures_equity():
    account = client.futures_account()

    total_balance = float(account["totalWalletBalance"])

    unrealized_pnl = float(account["totalUnrealizedProfit"])

    equity = total_balance + unrealized_pnl

    return {
        "equity": equity
    }

