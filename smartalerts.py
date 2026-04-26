import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

#product classes
class product:
    def __init__(self, product_id, name, price, quantity, threshold=5):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.threshold = threshold

class perishableProduct(product):
    def __init__(self, product_id, name, price, quantity, expiry_date, threshold=5):
        super().__init__(product_id, name, price, quantity, threshold)
        self.expiry_date = expiry_date

#smart alerts logic
def get_low_stock_items(inventory):
    return [item for item in inventory if item.quantity <= item.threshold]

def show_low_stock_alert(inventory):
    low_items = get_low_stock_items(inventory)
    if not low_items:
        return
    message = "Low Stock Alert:\n\n"
    for item in low_items:
        message += f"{item.name} (Qty: {item.quantity})\n"
    messagebox.showwarning("Low Stock Alert", message)

def get_expiring_items(inventory, days=7):
    expiring_items = []
    today = datetime.today()
    for item in inventory:
        if hasattr(item, "expiry_date") and item.expiry_date:
            try:
                expiry_date = datetime.strptime(item.expiry_date, "%Y-%m-%d")
                if today <= expiry_date <= today + timedelta(days=days):
                    expiring_items.append(item)
            except ValueError:
                continue
    return expiring_items

def show_expiry_window(inventory):
    expiring_items = get_expiring_items(inventory)
    if not expiring_items:
        messagebox.showinfo("Expiry Check", "No items expiring within 7 days.")
        return
    window = tk.Toplevel()
    window.title("Expiring Soon")
    window.geometry("400x300")
    tk.Label(window, text="Items expiring within 7 days:").pack(pady=5)
    listbox = tk.Listbox(window, width=50)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)
    for item in expiring_items:
        listbox.insert(tk.END, f"{item.name} - Expiry: {item.expiry_date}")

def run_smart_alerts(inventory):
    show_low_stock_alert(inventory)
    show_expiry_window(inventory)

#sample for testing
inventory = [
    perishableProduct("1", "Milk", 1.50, 2, "2026-05-01"),
    perishableProduct("2", "Cheese", 2.00, 10, "2026-05-03"),
    product("3", "Rice", 5.00, 3)
]

#gui
root = tk.Tk()
root.title("Inventory System")
root.geometry("400x300")

def add_dummy_product():
    #example of adding item
    new_item = perishableProduct("4", "Yogurt", 1.20, 1, "2026-05-02")
    inventory.append(new_item)

    messagebox.showinfo("Added", "Dummy product added.")

    #after adding it auto runs
    run_smart_alerts(inventory)

#buttons
tk.Button(root, text="Run Smart Alerts",
        command=lambda: run_smart_alerts(inventory)
).pack(pady=10)
tk.Button(root, text="Add Test Product",
        command=add_dummy_product
).pack(pady=10)
root.mainloop()
