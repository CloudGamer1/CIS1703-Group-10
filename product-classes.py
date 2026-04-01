import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity