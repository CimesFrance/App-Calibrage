"""Ce module contient les composants graphiques personnalisés utilisés dans l'application.
Il inclut des classes pour les cartes d'affichage, les cadres d'importation d'image, les
cadres d'étalonnage, et le conteneur principal d'interaction avec la barre latérale."""

import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from utils.import_manager import importer_image_tk


class Card(tk.Frame):
    """Conteneur transparent pour la sidebar"""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, bg="#2C3E50", pady=10, **kwargs)
        if title:
            lbl = ttk.Label(self, text=title, style="Sidebar.Title.TLabel")
            lbl.pack(anchor="w", pady=(0, 10))


class ImportImg(Card):
    """Carte d'importation d'image avec un bouton pour charger une image depuis le disque"""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, title="Source de l'image", **kwargs)
        self.app = app
        self.tk_charger_logo = importer_image_tk("logodownload.png")
        self._build()

    def _build(self):
        f = ttk.Frame(self, style="Sidebar.TFrame")
        f.pack(fill="x")
        ttk.Label(f, text="Sélectionnez une image", style="Sidebar.TLabel").pack(
            side="left"
        )
        ttk.Button(
            f,
            image=self.tk_charger_logo,
            command=self._import_tk_img,
            style="Icon.TButton",
        ).pack(side="right")

    def _import_tk_img(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            self.app.img.reboot()
            self.app.zoom_factor.set(1.0)
            self.app.img.img_path.set(path)
            self.app.flag_EchelleFrame.set(True)
            self.app.flag_save_btn_affiche.set(True)


class EchelleFrame(Card):
    """Carte d'étalonnage avec un bouton pour appliquer l'échelle"""
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, title="Étalonnage", **kwargs)
        self.app = app
        self.app.mesure_echelle.created = True
        self._build()
        self.app.flag_EchelleFrame.trace_add("write", self.update_view)

    def _build(self):
        # Frame pour la mesure d'échelle
        self.app.mesure_echelle.mesure_frame = tk.Frame(self, bg="#2C3E50")
        self.app.mesure_echelle.mesure_frame.pack(fill="x")
        self.app.mesure_echelle.mesure_gui()
        # Zone de saisie
        self.input_f = tk.Frame(self, bg="#2C3E50", pady=10)
        self.input_f.pack(fill="x")
        self.lbl = ttk.Label(
            self.input_f, text="Longueur réelle (mm)", style="Sidebar.TLabel"
        )
        self.lbl.pack(side="left")
        self.ent = ttk.Entry(
            self.input_f, textvariable=self.app.distance_saisie, width=10
        )
        self.ent.pack(side="right")
        self.btn = ttk.Button(
            self, text="Appliquer l'Échelle", command=self.apply_scale, style="TButton"
        )
        self.btn.pack(fill="x", pady=(10, 0))

    def update_view(self, *args):
        """Met à jour l'affichage de la carte d'étalonnage"""
        state = "normal" if self.app.flag_EchelleFrame.get() else "disabled"
        self.btn.config(state=state)
        self.ent.config(state=state)

    def apply_scale(self):
        """Applique l'échelle"""
        try:
            val_reelle = float(self.app.distance_saisie.get())
            m_ech = self.app.mesure_echelle
            if m_ech.pts["pt1"].created and m_ech.pts["pt2"].created:
                p1, p2 = m_ech.pts["pt1"].coord_pt_img, m_ech.pts["pt2"].coord_pt_img
                dist_px = np.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)
                if dist_px > 0:
                    nouveau_facteur = val_reelle / dist_px
                    self.app.facteur_conversion.set(nouveau_facteur)
                    # Mise à jour immédiate de tous les affichages de mesures
                    for m in self.app.list_mesures:
                        if m.created:
                            m.longueur.set(str(m.calcul_distance()))
        except ValueError:
            pass


class Interraction(tk.Frame):
    """Conteneur principal de la barre latérale, 
    avec scrollbar intégrée pour les cartes d'interaction"""

    def __init__(self, parent, app, **kwargs):
        # On extrait la largeur pour la fixer
        width = kwargs.get("width", 350)
        self.bg_color = kwargs.get("bg", "#2C3E50")
        super().__init__(parent, bg=self.bg_color, width=width)
        self.app = app
        
        # Initialisation des cadres de mesures
        self._setup_measurements()
        self.interraction_gui()

    def _setup_measurements(self):
        self.app.MesureSupp.mesures_supp_frame = tk.Frame(
            self, bg=self.bg_color
        )
        for m in self.app.MesureSupp.mes_mesures_supp.values():
            m.mesure_frame = tk.Frame(
                self.app.MesureSupp.mesures_supp_frame, bg=self.bg_color
            )

    def interraction_gui(self):
        """Initialise l'interface graphique de la barre latérale"""
        ImportImg(self, self.app).pack(
            fill="x", padx=15, pady=(10, 5)
        )
        tk.Frame(self, height=1, bg="#34495E").pack(
            fill="x", padx=15, pady=15
        )
        EchelleFrame(self, self.app).pack(fill="x", padx=15, pady=5)
        tk.Frame(self, height=1, bg="#34495E").pack(
            fill="x", padx=15, pady=15
        )
        self.m_card = Card(self, title="Mesures de contrôle")
        self.m_card.pack(fill="x", padx=15, pady=5)
        self.app.MesureSupp.mesures_supp_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.app.MesureSupp.mesures_supp_gui()

