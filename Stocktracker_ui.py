import tkinter as tk
from tkinter import ttk, messagebox
import os
import stock_data as Stocktracker


class StockTrackerUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Portfolio Tracker")
        self.configure(bg="#556B2F")
        # allow window to be resized so layout can adapt
        self.resizable(True, True)

        self.portfolio = {}

        self._build_ui()
        self._populate_stocks()
        self.update_summary()

    def _build_ui(self):
        pad = 10
        # Frames
        left = tk.Frame(self, bg="#556B2F", padx=pad, pady=pad)
        left.grid(row=0, column=0, sticky="nsew")
        mid = tk.Frame(self, bg="#556B2F", padx=pad, pady=pad)
        mid.grid(row=0, column=1, sticky="nsew")
        right = tk.Frame(self, bg="#556B2F", padx=pad, pady=pad)
        right.grid(row=0, column=2, sticky="nsew")

        # make main grid responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=3)

        # Available stocks
        tk.Label(left, text="Available Stocks", bg="#556B2F", fg="white", font=(None, 12, "bold")).pack()
        self.stocks_tree = ttk.Treeview(left, columns=("symbol", "company", "price"), show="headings")
        self.stocks_tree.heading("symbol", text="Symbol")
        self.stocks_tree.heading("company", text="Company")
        self.stocks_tree.heading("price", text="Price")
        self.stocks_tree.column("symbol", width=70, anchor="center")
        self.stocks_tree.column("company", width=180, anchor="w")
        self.stocks_tree.column("price", width=90, anchor="e")
        # allow the treeview to expand with the window
        self.stocks_tree.pack(fill="both", expand=True)

        # Controls
        tk.Label(mid, text="Add to Portfolio", bg="#556B2F", fg="white", font=(None, 12, "bold")).pack(pady=(0, 8))
        # Combobox shows "SYMBOL - Company" for clarity
        self.symbol_var = tk.StringVar()
        combo_values = [f"{s} - {info['name']}" for s, info in Stocktracker.stock_info.items()]
        self.symbol_cb = ttk.Combobox(mid, textvariable=self.symbol_var, values=combo_values, state="readonly", width=28)
        self.symbol_cb.pack(pady=4)
        if combo_values:
            self.symbol_cb.current(0)

        qty_frame = tk.Frame(mid, bg="#556B2F")
        qty_frame.pack(pady=4)
        tk.Label(qty_frame, text="Quantity:", bg="#556B2F", fg="white").pack(side="left")
        self.qty_var = tk.StringVar(value="1")
        self.qty_spin = tk.Spinbox(qty_frame, from_=1, to=1000000, width=8, textvariable=self.qty_var)
        self.qty_spin.pack(side="left", padx=6)

        # Live price preview
        self.unit_price_lbl = tk.Label(mid, text="Unit price: Tshs 0", bg="#556B2F", fg="white")
        self.unit_price_lbl.pack(pady=(6, 2))
        self.line_total_lbl = tk.Label(mid, text="Line total: Tshs 0", bg="#556B2F", fg="white", font=(None, 10, "bold"))
        self.line_total_lbl.pack(pady=(0, 8))

        add_btn = tk.Button(mid, text="Add", command=self.add_to_portfolio, bg="white", fg="black")
        add_btn.pack(fill="x", pady=(6, 6))

        rm_btn = tk.Button(mid, text="Remove Selected", command=self.remove_selected, bg="white", fg="black")
        rm_btn.pack(fill="x")

        # Portfolio
        tk.Label(right, text="Your Portfolio", bg="#556B2F", fg="white", font=(None, 12, "bold")).pack()
        # Portfolio columns: Symbol, Company, Quantity, Unit price, Value
        self.port_tree = ttk.Treeview(right, columns=("symbol", "company", "qty", "unit_price", "value"), show="headings")
        self.port_tree.heading("symbol", text="Symbol")
        self.port_tree.heading("company", text="Company")
        self.port_tree.heading("qty", text="Quantity")
        self.port_tree.heading("unit_price", text="Unit Price")
        self.port_tree.heading("value", text="Value")
        self.port_tree.column("symbol", width=70, anchor="center")
        self.port_tree.column("company", width=140, anchor="w")
        self.port_tree.column("qty", width=70, anchor="center")
        self.port_tree.column("unit_price", width=100, anchor="e")
        self.port_tree.column("value", width=110, anchor="e")
        # allow the portfolio tree to expand with the window
        self.port_tree.pack(fill="both", expand=True)

        self.total_label = tk.Label(right, text="Total: Tshs 0", bg="#556B2F", fg="white", font=(None, 11, "bold"))
        self.total_label.pack(pady=(8, 4))

        save_btn = tk.Button(right, text="Save to File", command=self.save_to_file, bg="black", fg="white")
        save_btn.pack(fill="x")

        # Update column widths when window size changes
        self.bind("<Configure>", lambda e: self._on_resize())

    def _populate_stocks(self):
        for symbol, info in Stocktracker.stock_info.items():
            price = info.get("price", 0)
            company = info.get("name", "")
            self.stocks_tree.insert("", "end", iid=symbol, values=(symbol, company, f"Tshs {price:,}"))

        # ensure the preview reflects the initial selection
        self.symbol_var.trace_add("write", lambda *a: self.update_price_preview())
        self.qty_var.trace_add("write", lambda *a: self.update_price_preview())
        self.update_price_preview()

    def add_to_portfolio(self):
        sel = self.symbol_var.get()
        if not sel:
            messagebox.showerror("Selection required", "Please select a stock.")
            return
        symbol = sel.split(" - ")[0]

        try:
            qty = int(self.qty_var.get())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Please enter a valid integer quantity.")
            return

        if symbol not in Stocktracker.stock_info:
            messagebox.showerror("Unknown stock", "Selected stock is not available.")
            return

        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + qty
        self._refresh_portfolio_view()
        self.update_summary()

    def _refresh_portfolio_view(self):
        for i in self.port_tree.get_children():
            self.port_tree.delete(i)
        for symbol, qty in self.portfolio.items():
            info = Stocktracker.stock_info.get(symbol, {})
            company = info.get("name", "")
            unit_price = info.get("price", 0)
            value = unit_price * qty
            self.port_tree.insert("", "end", iid=symbol, values=(symbol, company, qty, f"Tshs {unit_price:,}", f"Tshs {value:,}"))

    def remove_selected(self):
        sel = self.port_tree.selection()
        if not sel:
            return
        for iid in sel:
            self.portfolio.pop(iid, None)
        self._refresh_portfolio_view()
        self.update_summary()

    def update_summary(self):
        total = Stocktracker.calculate_investment(self.portfolio)
        self.total_label.config(text=f"Total: Tshs {total:,}")

    def update_price_preview(self):
        sel = self.symbol_var.get()
        if not sel:
            self.unit_price_lbl.config(text="Unit price: Tshs 0")
            self.line_total_lbl.config(text="Line total: Tshs 0")
            return
        symbol = sel.split(" - ")[0]
        info = Stocktracker.stock_info.get(symbol, {})
        unit = info.get("price", 0)
        try:
            qty = int(self.qty_var.get())
        except Exception:
            qty = 0
        line = unit * qty
        self.unit_price_lbl.config(text=f"Unit price: Tshs {unit:,}")
        self.line_total_lbl.config(text=f"Line total: Tshs {line:,}")

    def save_to_file(self):
        filename = os.path.join(os.getcwd(), "Stock_portfolio.txt")
        total = Stocktracker.save_portfolio(self.portfolio, filename)
        messagebox.showinfo("Saved", f"Portfolio saved to {filename}\nTotal: Tshs {total}")

    def _on_resize(self):
        # Adjust column widths proportionally for better responsiveness
        try:
            # Stocks tree columns: symbol 15%, company 60%, price 25%
            left_w = max(200, self.winfo_width() // 3)
            s_w = max(50, int(left_w * 0.15))
            c_w = max(100, int(left_w * 0.60))
            p_w = max(70, int(left_w * 0.25))
            self.stocks_tree.column("symbol", width=s_w)
            self.stocks_tree.column("company", width=c_w)
            self.stocks_tree.column("price", width=p_w)

            # Portfolio tree columns: symbol 10%, company 45%, qty 10%, unit_price 20%, value 15%
            right_w = max(300, self.winfo_width() // 3)
            rs = max(50, int(right_w * 0.10))
            rc = max(100, int(right_w * 0.45))
            rq = max(50, int(right_w * 0.10))
            rup = max(80, int(right_w * 0.20))
            rv = max(80, int(right_w * 0.15))
            self.port_tree.column("symbol", width=rs)
            self.port_tree.column("company", width=rc)
            self.port_tree.column("qty", width=rq)
            self.port_tree.column("unit_price", width=rup)
            self.port_tree.column("value", width=rv)
        except Exception:
            pass


def main():
    app = StockTrackerUI()
    app.mainloop()


if __name__ == "__main__":
    main()
