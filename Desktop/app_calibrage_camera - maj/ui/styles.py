"""Module de gestion des styles de l'application."""
from tkinter import ttk

class StyleManager:
    """Classe pour gérer les styles de l'application."""
    BG_MAIN = "#F5F6FA"
    BG_SIDEBAR = "#2C3E50"
    PRIMARY = "#2C3E50"
    ACCENT = "#D35400" 
    ACCENT_HOVER = "#BA4A00" 
    TEXT = "#2F3640"
    BORDER = "#DCDDE1"
    FONT_FAMILY = "Segoe UI"

    def __init__(self, root):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()
        root.configure(bg=self.BG_MAIN)

    def _configure_styles(self):
        self.style.configure("TFrame", background=self.BG_MAIN)
        self.style.configure("Sidebar.TFrame", background=self.BG_SIDEBAR, relief="flat")
        self.style.configure("TLabel", background=self.BG_MAIN, foreground=self.TEXT, font=(self.FONT_FAMILY, 10))
        self.style.configure("Sidebar.TLabel", background=self.BG_SIDEBAR, foreground="white", font=(self.FONT_FAMILY, 10))
        self.style.map("Sidebar.TLabel", 
                       background=[('disabled', self.BG_SIDEBAR), ('!disabled', self.BG_SIDEBAR)],
                       foreground=[('disabled', 'white'), ('!disabled', 'white')])         
        self.style.configure("Sidebar.TCheckbutton", background=self.BG_SIDEBAR, foreground="white")
        self.style.map("Sidebar.TCheckbutton", 
                       background=[('disabled', self.BG_SIDEBAR), ('!disabled', self.BG_SIDEBAR)],
                       foreground=[('disabled', '#7F8C8D'), ('!disabled', 'white')],
                       indicatorcolor=[('disabled', '#7F8C8D'), ('!selected', '#bdc3c7'), ('selected', self.ACCENT)])
        self.style.configure("Sidebar.TRadiobutton", background=self.BG_SIDEBAR, foreground="white")
        self.style.map("Sidebar.TRadiobutton", 
                       background=[('disabled', self.BG_SIDEBAR), ('!disabled', self.BG_SIDEBAR)],
                       foreground=[('disabled', 'white'), ('!disabled', 'white')],
                       indicatorcolor=[('!selected', '#bdc3c7'), ('selected', self.ACCENT)])         
        self.style.configure("Title.TLabel", font=(self.FONT_FAMILY, 12, "bold"), foreground=self.PRIMARY)
        self.style.configure("Sidebar.Title.TLabel", background=self.BG_SIDEBAR, font=(self.FONT_FAMILY, 12, "bold"), foreground="white")
        # Styles de sous-titre et affichage numérique pour Measurements
        self.style.configure("Sidebar.Subtitle.TLabel", background=self.BG_SIDEBAR, font=(self.FONT_FAMILY, 9, "bold"), foreground="white")
        self.style.map("Sidebar.Subtitle.TLabel", 
                       foreground=[('disabled', '#7F8C8D'), ('!disabled', 'white')],
                       background=[('disabled', self.BG_SIDEBAR), ('!disabled', self.BG_SIDEBAR)])
        
        self.style.configure("Value.TLabel", background="#34495E", foreground=self.ACCENT, font=(self.FONT_FAMILY, 14, "bold"))
        self.style.configure("DisabledValue.TLabel", background=self.BG_SIDEBAR, foreground="#7F8C8D", font=(self.FONT_FAMILY, 14, "bold"))
        self.style.map("DisabledValue.TLabel", background=[('disabled', self.BG_SIDEBAR)])
        
        self.style.configure("Unit.TLabel", background="#34495E", foreground="#BDC3C7", font=(self.FONT_FAMILY, 8))
        self.style.configure("DisabledUnit.TLabel", background=self.BG_SIDEBAR, foreground="#7F8C8D", font=(self.FONT_FAMILY, 8))
        self.style.map("DisabledUnit.TLabel", background=[('disabled', self.BG_SIDEBAR)])
        # Primary Button (Accentual)
        self.style.configure("TButton", font=(self.FONT_FAMILY, 9, "bold"))
        self.style.map("TButton", 
                       background=[('disabled', "#7F8C8D"), ('active', self.ACCENT_HOVER), ('!disabled', self.ACCENT)], 
                       foreground=[('disabled', '#BDC3C7'), ('!disabled', 'white')])
        # Secondary Button (Bordered or normal)
        self.style.configure("Secondary.TButton", font=(self.FONT_FAMILY, 9))
        self.style.map("Secondary.TButton",
                       background=[('disabled', "#DCDDE1"), ('active', "#DCDDE1"), ('!disabled', "#ECF0F1")],
                       foreground=[('disabled', '#7F8C8D'), ('!disabled', '#2C3E50')])
        # Icon Button (Transparent)
        self.style.configure("Icon.TButton", background=self.BG_SIDEBAR, borderwidth=0, relief="flat", focuscolor="none", padding=0)
        self.style.map("Icon.TButton",
                       background=[('active', "#34495E"), ('!disabled', self.BG_SIDEBAR)],
                       relief=[('pressed', 'flat')])
        self.style.configure("TEntry", fieldbackground="#FFFFFF", borderwidth=1)
