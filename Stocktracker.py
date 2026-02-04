
from stock_data import stock_info, stock_prices, calculate_investment, save_portfolio


def cli_main():
    """Command-line interface preserved for compatibility."""
    print("WELCOME TO STOCK PORTFOLIO TRACKER")
    print("Available stocks and their prices:\n")
    for stock, price in stock_prices.items():
        print(stock, "@Tshs", price)

    portfolio = {}
    total_investment = 0

    try:
        num_stocks = int(input("\nHow many different stocks do you want to invest? "))
    except ValueError:
        print("Invalid number, exiting.")
        return

    for _ in range(num_stocks):
        stock_name = input("Enter stock name: ").upper()
        if stock_name not in stock_prices:
            print("Stock not available, please choose from the available stocks.")
            continue

        try:
            quantity = int(input("Enter quantity to buy: "))
        except ValueError:
            print("Invalid quantity, skipping.")
            continue

        investment_value = stock_prices[stock_name] * quantity
        total_investment += investment_value
        portfolio[stock_name] = portfolio.get(stock_name, 0) + quantity

    print("\nYOUR PORTFOLIO SUMMARY")
    for stock, qty in portfolio.items():
        print(stock, "quantity:", qty, "\nStock value", stock_prices[stock] * qty)
    print("\nTotal Investment value: Tshs", total_investment)

    save_portfolio(portfolio)


if __name__ == "__main__":
    import sys
    # If user passes 'cli' as an argument, run the existing CLI.
    # Otherwise launch the graphical UI from the main module.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        cli_main()
    else:
        try:
            # Import local UI module and run its main entrypoint
            import Stocktracker_ui

            if hasattr(Stocktracker_ui, "main"):
                Stocktracker_ui.main()
            else:
                # Fallback to CLI if UI not present
                cli_main()
        except Exception:
            # If for any reason GUI fails, fallback to CLI to keep functionality available
            cli_main()


