"""Module de gestion de la fenetre principale"""

import tkinter as tk
from core.state import AppState
from ui.canvas_view import FenetreImage
from ui.components import Interraction
from ui.styles import StyleManager


class ApplicationCalibrage(tk.Tk):
    """Fenêtre principale de l'application de calibration"""
    def __init__(self):
        super().__init__()
        self.app = AppState()
        self.title("CIMES Calibration Suite")
        self.iconbitmap("assets/image.ico")
        self.geometry("1300x900")
        self.minsize(1300, 900)
        self.resizable(True, True)
        # Application du StyleManager
        self.style_manager = StyleManager(self)
        # Layout principal
        self.sidebar = Interraction(
            self, self.app, width=350, bg=self.style_manager.BG_SIDEBAR
        )
        self.canvas_view = FenetreImage(
            self, self.app, bg=self.style_manager.BG_MAIN, bd=0, highlightthickness=0
        )
        # Sidebar à gauche (colonne 0)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        self.sidebar.grid_propagate(False)
        # Canvas à droite (colonne 1)
        self.canvas_view.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
