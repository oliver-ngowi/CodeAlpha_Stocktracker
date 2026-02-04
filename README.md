# Stock Portfolio Tracker

A simple Python application for managing and tracking a stock portfolio focused on Tanzanian stocks (DSE - Dar es Salaam Stock Exchange).

## Features

- **Interactive GUI** - User-friendly graphical interface for portfolio management
- **25+ Stocks** - Browse popular Tanzanian stocks (banks, beverages, cement, energy, etc.)
- **Portfolio Management** - Add/remove stocks and specify quantities
- **Investment Tracking** - Automatic calculation of total portfolio value
- **Data Persistence** - Save your portfolio for future sessions

## Quick Start

### Run the GUI (Recommended)
```bash
python Stocktracker.py
```

### Run the CLI
```bash
python Stocktracker.py cli
```

## How It Works

1. **Browse stocks** - View all 25+ available stocks with their prices (in Tanzanian Shillings)
2. **Build portfolio** - Select stocks and enter quantities you want to buy
3. **Track value** - See your total investment value calculated automatically
4. **Save portfolio** - Store your portfolio data locally

## Project Files

- **Stocktracker.py** - Main application entry point (GUI launcher and CLI support)
- **Stocktracker_ui.py** - Tkinter-based graphical interface
- **stock_data.py** - Stock information and portfolio utilities
- **Stock_portfolio.txt** - Auto-generated file when saving your portfolio

## Available Stocks

Banks, breweries, cement companies, energy providers, microfinance institutions, and more from the Tanzanian market.

## Design

- **Theme:** Olive green, white, and black interface
- **Built with:** Python 3 + Tkinter
- **Target audience:** Individual investors tracking personal stock portfolios
