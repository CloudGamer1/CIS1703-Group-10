import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_value(self):
        return self.price * self.quantity

    def get_type(self):
        return "Product"

    def to_display_string(self):
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: £{self.price:.2f} | "
            f"Qty: {self.quantity} | "
            f"Type: {self.get_type()}"
        )