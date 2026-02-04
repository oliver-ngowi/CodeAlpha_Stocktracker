"""Shared stock data and helper functions used by the CLI and UI.

Move the hardcoded `stock_info` and portfolio helper functions here to
avoid circular imports between `Stocktracker.py` and `Stocktracker_ui.py`.
"""
from typing import Dict

# Hardcoded stock information (shared data)
# Each entry contains a company/display name and a unit price (sample Tshs values).
# These are example/default prices for the app; update them with real market prices as needed.
stock_info: Dict[str, Dict] = {
    "CRDB": {"name": "CRDB Bank", "price": 1200},
    "NMB": {"name": "NMB Bank", "price": 1500},
    "VODA": {"name": "Vodacom Tanzania", "price": 800},
    "TBL": {"name": "Tanzania Breweries Limited", "price": 3500},
    "TCC": {"name": "Tanzania Cigarette Company", "price": 9000},
    "TWIGA": {"name": "Tanzania Portland Cement Company", "price": 2500},
    "TOL": {"name": "Tol Gases Limited", "price": 500},
    "TATEPA": {"name": "Tanzania Tea Packers", "price": 700},
    "DCB": {"name": "Dar es Salaam Community Bank", "price": 300},
    "KCB": {"name": "KCB Group (cross-listed)", "price": 1100},
    "PAL": {"name": "Precision Air Services", "price": 400},
    "SWALA": {"name": "Swala Oil & Gas", "price": 600},
    "NICO": {"name": "National Investments Company (NICO)", "price": 2000},
    "DSE": {"name": "Dar es Salaam Stock Exchange (DSE)", "price": 1000},
    "SWIS": {"name": "Swissport Tanzania", "price": 450},
    "ACA": {"name": "Acacia / African Barrick (historic)", "price": 1800},
    "USL": {"name": "Uchumi Supermarkets (cross-listed)", "price": 120},
    "EABL": {"name": "East African Breweries (cross-listed)", "price": 5000},
    "SIMBA": {"name": "Tanga Cement (Simba)", "price": 1800},
    "MKCB": {"name": "Mkombozi Commercial Bank", "price": 250},
    "MCB": {"name": "Mwalimu Commercial Bank", "price": 220},
    "MBP": {"name": "Maendeleo Bank", "price": 210},
    "YETU": {"name": "Yetu Microfinance", "price": 90},
    "MUCOB": {"name": "MUCOBA Bank", "price": 160},
    "JATU": {"name": "Jatu PLC", "price": 70},
    "TICL": {"name": "TCCIA Investment PLC", "price": 1300},
}

# Backwards-compatible mapping of tickers to prices
stock_prices = {k: v["price"] for k, v in stock_info.items()}


def calculate_investment(portfolio: dict) -> int:
    """Return total investment value for the given portfolio.

    portfolio: dict mapping stock ticker -> quantity (int)
    """
    return sum(stock_prices.get(s, 0) * q for s, q in portfolio.items())


def save_portfolio(portfolio: dict, filename: str = "Stock_portfolio.txt") -> int:
    """Save the portfolio summary to a text file and return total investment."""
    total = calculate_investment(portfolio)
    with open(filename, "w", encoding="utf-8") as file:
        file.write("YOUR PORTFOLIO SUMMARY\n")
        for stock, quantity in portfolio.items():
            value = stock_prices.get(stock, 0) * quantity
            file.write(f"{stock}, quantity: {quantity}, value: Tshs{value}\n")
        file.write(f"\nTotal Investment: Tshs {total}\n")
    return total
