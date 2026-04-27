import tkinter as tk
import csv
from product_classes import (
    Product,
    PerishableProduct,
    ElectronicProduct,
)
from tkinter import messagebox
from smartalerts import run_smart_alerts

InventoryFile = "inventory.csv"

# window
root = tk.Tk()
root.title("Smartstock Dashboard")
root.geometry("800x850")  # fixed smart art not showing

# storage
inventory = []


tk.Label(
    root, text="Product Type"
).pack()  # Added options for the user to select the type of product they want to add
type_var = tk.StringVar(value="Product")
type_dropdown = tk.OptionMenu(root, type_var, "Product", "Perishable", "Electronic")
type_dropdown.pack()


# -------inputs------------
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Price").pack()
price_entry = tk.Entry(root)
price_entry.pack()

tk.Label(root, text="Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()


"""added fields for the perishable and electronic products"""
# Perishable fields
tk.Label(root, text="Expiry Date (YYYY-MM-DD)").pack()
expiry_entry = tk.Entry(root)
expiry_entry.pack()

tk.Label(root, text="Storage Temp").pack()
storage_entry = tk.Entry(root)
storage_entry.pack()

# Electronic fields
tk.Label(root, text="Warranty (months)").pack()
warranty_entry = tk.Entry(root)
warranty_entry.pack()

tk.Label(root, text="Power Usage (W)").pack()
power_entry = tk.Entry(root)
power_entry.pack()


# ---------list display------
listbox = tk.Listbox(root, width=120)
listbox.pack(pady=10)

# ------dashboard--------
total_label = tk.Label(root, text="Total Items: 0")
total_label.pack()

low_stock_label = tk.Label(root, text="low stock: 0")
low_stock_label.pack()

value_label = tk.Label(root, text="Total Value: £0")
value_label.pack()

status_label = tk.Label(root, text="", fg="white", bg="#3498db", width=80)#Rays code for the status label
status_label.pack(pady=5)

units_label = tk.Label(root, text="Total Units: 0")#added units label to the dashboard to show the total number of units in stock, not just the number of different products
units_label.pack()

"""------------------------------
-------------------------------
----------funcitions-----------
-------------------------------
-------------------------------"""


def update_listbox():
    """
    updates the listbox with the data in inventory
    """

    listbox.delete(0, tk.END)
    for item in inventory:
        listbox.insert(tk.END, item.to_display_string())


def update_dashboard():
    """
    updates the dashboard "price, ammount of items, stock"
    """
    total_items = len(inventory)
    total_units = sum(item.quantity for item in inventory) #ray added total units

    low_stock = sum(1 for item in inventory if item.quantity < 5)

    total_value = sum(item.calculate_value() for item in inventory)

    total_label.config(text=f"Total Items: {total_items}")
    units_label.config(text=f"Total Units: {total_units}")#ray unit label
    low_stock_label.config(
        text=f"Low stock: {low_stock}"
    ) 
    value_label.config(text=f"Total Value: £{total_value}")


def show_status(message, status_type="info"):#inserted rays code here
    colors = {
        "error": "#e74c3c",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "info": "#3498db"
    }

    status_label.config(
        text=message,
        bg=colors.get(status_type, "#3498db")
    )

    # Cancel previous timer
    if hasattr(show_status, "after_id"):
        root.after_cancel(show_status.after_id)

    # Auto-clear after 3 seconds
    show_status.after_id = root.after(3000, clear_status)

def clear_status():
    status_label.config(text="", bg="gray")

#end of rays code


def add_product():
    """
    adds products to the inventory, creates a new object of the product class
    """

    try:
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())

        product_type = (
            type_var.get().strip().lower()
        )  # get the selected product type and convert to lowercase
        new_id = len(inventory) + 1

        if product_type == "product":
            product = Product(new_id, name, price, quantity)

        elif product_type == "perishable":
            expiry = expiry_entry.get()
            storage = storage_entry.get()
            product = PerishableProduct(new_id, name, price, quantity, expiry, storage)

        elif product_type == "electronic":
            warranty = int(warranty_entry.get())
            power = int(power_entry.get())
            product = ElectronicProduct(new_id, name, price, quantity, warranty, power)

        inventory.append(product)

        with open("log.txt", "a") as f:
            f.write(f"Added: {product.to_display_string()}\n")

        update_listbox()
        update_dashboard()

        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        expiry_entry.delete(0, tk.END)
        storage_entry.delete(0, tk.END)
        warranty_entry.delete(0, tk.END)
        power_entry.delete(0, tk.END)

    except:
        print("Invalid input")


def remove_product():
    """
    removes the product from the inventory
    """
    # try:
    selected_index = listbox.curselection()[0]
    removed_item = inventory.pop(selected_index)

    # log
    with open("log.txt", "a") as f:
        f.write(f"Removed: {removed_item.to_display_string()}\n")
    update_listbox()
    update_dashboard()

    # except:
    #    print("No item selected")


def edit_product():
    """
    edits the product in the inventory
    """
    try:
        selected_index = listbox.curselection()[0]
        item = inventory[selected_index]

        new_quantity = quantity_entry.get()
        item.quantity = int(new_quantity)

        # log
        with open("log.txt", "a") as f:
            f.write(f"Updated: {item.name} -> {new_quantity}\n")

        update_listbox()
        update_dashboard()

    except:
        print("Error editing item")


def save_inventory(
    InventoryFile, data
):  # added the new fields for the perishable and electronic products to the save_inventory function
    TempData = []

    for item in data:

        row = {
            "product_id": item.product_id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity,
            "type": item.get_type(),
        }

        if item.get_type() == "Perishable":
            row["expiry_date"] = item.expiry_date
            row["storage_temp"] = item.storage_temp

        if item.get_type() == "Electronic":
            row["warranty_months"] = item.warranty_months
            row["power_usage"] = item.power_usage

        TempData.append(row)

    fields = [
        "product_id",
        "name",
        "price",
        "quantity",
        "type",
        "warranty_months",
        "power_usage",
        "expiry_date",
        "storage_temp",
    ]

    with open(InventoryFile, "w", newline="") as InventoryData:
        writer = csv.DictWriter(InventoryData, fields)
        writer.writeheader()
        writer.writerows(TempData)


def load_inventory(
    InventoryFile,
):  # added the new fields for the perishable and electronic products to the load_inventory function and added error handling for missing file
    TempInventory = []

    try:
        with open(InventoryFile, "r") as InventoryData:
            reader = csv.DictReader(InventoryData)

            for row in reader:
                ptype = row.get("type", "Product")

                if ptype == "Perishable":
                    Data = PerishableProduct(
                        int(row["product_id"]),
                        row["name"],
                        float(row["price"]),
                        int(row["quantity"]),
                        row.get("expiry_date"),
                        row.get("storage_temp"),
                    )

                elif ptype == "Electronic":
                    Data = ElectronicProduct(
                        int(row["product_id"]),
                        row["name"],
                        float(row["price"]),
                        int(row["quantity"]),
                        int(row.get("warranty_months", 0)),
                        int(row.get("power_usage", 0)),
                    )

                else:
                    Data = Product(
                        int(row["product_id"]),
                        row["name"],
                        float(row["price"]),
                        int(row["quantity"]),
                    )

                TempInventory.append(Data)

    except FileNotFoundError:
        TempInventory = []

    listbox.delete(0, tk.END)  # clears the listbox to stop duplicates
    for item in TempInventory:
        listbox.insert(tk.END, item.to_display_string())

    return TempInventory


def on_closing():
    if messagebox.askokcancel("Quit", "Do you realy want to exit the program?"):
        root.destroy()


"""------------------------------
-------------------------------
----------buttons-----------
-------------------------------
-------------------------------"""

tk.Button(root, text="Add product", command=add_product).pack(
    pady=10
) 
tk.Button(root, text="Remove selected", command=remove_product).pack(pady=5)
tk.Button(root, text="Update Quantity", command=edit_product).pack(pady=5)
tk.Button(
    root, text="Save", command=lambda: save_inventory("Inventory.csv", inventory)
).pack(pady=5)
tk.Button(
    root, text="Run Smart Alerts", command=lambda: run_smart_alerts(inventory)
).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)


inventory = load_inventory("Inventory.csv")
update_dashboard()
