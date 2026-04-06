Project Name: BinanceFuturesBot

Description:
A Python-based Binance Futures trading bot with a clean CLI interface. The bot allows users to place MARKET, LIMIT, STOP_MARKET, and TAKE_PROFIT_MARKET orders on the Binance Futures Testnet. It supports BUY and SELL operations, validates user input, logs all API requests and responses, and handles exceptions like invalid input or network errors.

Features:

Interactive CLI for step-by-step order placement

Input validation using a dedicated validators.py module

Structured logging for requests, responses, and errors

Exception handling for API errors, invalid inputs, and network failures

Fully testable on Binance Futures Testnet

Requirements:

Python 3.x

python-binance, typer, python-dotenv

Setup:

Clone the repo

Install dependencies: pip install -r requirements.txt

Configure Binance Testnet API keys in .env file

Run the CLI:

python main.py