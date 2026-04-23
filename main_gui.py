import tkinter as tk
from product_classes import Product  # changed product to product_classes

# window
root = tk.Tk()  # fixed it from tk.TK to tk.Tk()
root.title("Smartstock Dashboard")
root.geometry("500x500")  # fixed typo

# storage
inventory = []

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

# ---------list display------
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

# ------dashboard--------
total_label = tk.Label(root, text="Total Items: 0")
total_label.pack()

low_stock_label = tk.Label(root, text="low stock: 0")
low_stock_label.pack()

value_label = tk.Label(root, text="Total Value: £0")
value_label.pack()


# ----------functions-------
def update_listbox():
    listbox.delete(0, tk.END)
    for item in inventory:
        listbox.insert(
            tk.END, item.to_display_string()
        )  # fixed it from item.display-string() to item.display_string()


def update_dashboard():
    total_items = len(inventory)

    low_stock = sum(1 for item in inventory if item.quantity < 5)

    total_value = sum(item.calculate_value() for item in inventory)

    total_label.config(text=f"Total Items: {total_items}")
    low_stock_label.config(
        text=f"Low stock: {low_stock}"
    )  # changed Total_stock_label to low_stock_label and added "_" to low_stock
    value_label.config(text=f"Total Value: £{total_value}")


def add_product():
    try:
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())

        product = Product(len(inventory) + 1, name, price, quantity)  # removed "#"
        inventory.append(product)  # removed ~
        # log
        with open("log.txt", "a") as f:
            f.write(
                f"Added: {product.to_display_string()}\n"
            )  # made sure f is under the with block

        update_listbox()
        update_dashboard()

        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

    except:
        print("Invalid input")


def remove_product():
    try:
        selected_index = listbox.curselection()[0]
        removed_item = inventory.pop(selected_index)

        # log
        with open("log.txt", "a") as f:
            f.write(f"Removed: {removed_item.to_display_string()}\n")

        update_listbox()
        update_dashboard()

    except:
        print("No item selected")


def edit_product():
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


# -------- buttons---------
tk.Button(root, text="Add product", command=add_product).pack(
    pady=10
)  # added "_" to add product and added "=" to pady10"
tk.Button(root, text="Remove selected", command=remove_product).pack(pady=5)
tk.Button(root, text="Update Quantity", command=edit_product).pack(pady=5)

# ----run-----
root.mainloop()
