import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta


class Product:
    def __init__(self, product_id, name, price, quantity, threshold=5):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.threshold = threshold

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


class PerishableProduct(Product):
    def __init__(
        self, product_id, name, price, quantity, expiry_date, storage_temp, threshold=5
    ):
        super().__init__(product_id, name, price, quantity, threshold)
        self.expiry_date = expiry_date
        self.storage_temp = storage_temp

    def get_type(self):
        return "Perishable"

    def to_display_string(self):
        return (
            super().to_display_string()
            + f" | Expiry: {self.expiry_date}"
            + f" | Storage Temp: {self.storage_temp}"
        )


class ElectronicProduct(Product):
    def __init__(self, product_id, name, price, quantity, warranty_months, power_usage):
        super().__init__(product_id, name, price, quantity)
        self.warranty_months = warranty_months
        self.power_usage = power_usage

    def get_type(self):
        return "Electronic"

    def calculate_value(self):
        depreciated_price = self.price * 0.90
        return depreciated_price * self.quantity

    def to_display_string(self):
        return (
            super().to_display_string()
            + f" | Warranty: {self.warranty_months} months"
            + f" | Power: {self.power_usage}W"
        )
