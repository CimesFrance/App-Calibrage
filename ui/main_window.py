"""Fenêtre principale de l'application de calibration"""

import tkinter as tk
from tkinter import ttk
from core.state import AppState
from ui.canvas_view import FenetreImage
from ui.components import Interraction


class ApplicationCalibrage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app = AppState()
        self.title("App Calibrage Image")
        self.geometry("1200x800")
        self.iconbitmap("assets/image.ico")
        self.configure(bg="#F0F2F5")  # Fond de l'application
        # Configuration des styles TTK
        style = ttk.Style()
        style.theme_use("clam")
        # Bouton Principal
        style.configure(
            "Primary.TButton",
            padding=10,
            font=("Segoe UI", 9, "bold"),
            background="#0056B3",
            foreground="white",
        )
        style.map("Primary.TButton", background=[("active", "#004494")])
        # Bouton Secondaire
        style.configure("Secondary.TButton", padding=8, font=("Segoe UI", 9))
        # Entry
        style.configure("TEntry", fieldbackground="#FFFFFF", borderwidth=1)
        # Layout principal
        self.canvas_view = FenetreImage(
            self, self.app, bg="#FFFFFF", bd=0, highlightthickness=0
        )
        self.sidebar = Interraction(self, self.app, width=320, bg="#F0F2F5")
        self.canvas_view.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.sidebar.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("Calibration Suite | Pro Edition")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.minsize(1000, 600)  # Taille minimale pour ne pas écraser l'UI
        self.canvas_view = FenetreImage(
            self, self.app, bg="#FFFFFF", bd=0, highlightthickness=0
        )
        self.sidebar = Interraction(self, self.app, width=320, bg="#F0F2F5")
        self.canvas_view.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.sidebar.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
