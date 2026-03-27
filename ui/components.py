"""Ce module contient les composants graphiques personnalisés utilisés dans l'application.
Il inclut des classes pour les cartes d'affichage, les cadres d'importation d'image, les
cadres d'étalonnage, et le conteneur principal d'interaction avec la barre latérale."""

import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from utils.import_manager import importer_image_tk


class Card(tk.Frame):
    """Conteneur minimaliste blanc avec ombre légère"""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(
            parent,
            bg="#FFFFFF",
            padx=20,
            pady=20,
            highlightbackground="#DCDFE3",
            highlightthickness=1,
            **kwargs
        )
        if title:
            lbl = tk.Label(
                self,
                text=title.upper(),
                font=("Segoe UI", 8, "bold"),
                bg="#FFFFFF",
                fg="#6C757D",
            )
            lbl.pack(anchor="w", pady=(0, 15))


class image_frame(Card):
    """Carte d'importation d'image avec un bouton pour charger une image depuis le disque"""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, title="Source de l'image", **kwargs)
        self.app = app
        self.tk_charger_logo = importer_image_tk("logodownload.png")
        self._build()

    def _build(self):
        f = tk.Frame(self, bg="#FFFFFF")
        f.pack(fill="x")
        tk.Label(
            f,
            text="Sélectionnez un fichier .jpg",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#495057",
        ).pack(side="left")
        ttk.Button(
            f,
            image=self.tk_charger_logo,
            command=self._import_tk_img,
            style="Secondary.TButton",
        ).pack(side="right")

    def _import_tk_img(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            self.app.img.reboot()
            self.app.zoom_factor.set(1.0)
            self.app.img.img_path.set(path)
            self.app.flag_echelle_frame.set(True)
            self.app.flag_save_btn_affiche.set(True)


class Echelle_frame(Card):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, title="Étalonnage", **kwargs)
        self.app = app
        self.app.mesure_echelle.created = True
        self._build()
        self.app.flag_echelle_frame.trace_add("write", self.update_view)

    def _build(self):
        # Frame pour la mesure d'échelle
        self.app.mesure_echelle.mesure_frame = tk.Frame(self, bg="#FFFFFF")
        self.app.mesure_echelle.mesure_frame.pack(fill="x")
        self.app.mesure_echelle.mesure_GUI()
        # Zone de saisie
        self.input_f = tk.Frame(self, bg="#FFFFFF", pady=10)
        self.input_f.pack(fill="x")
        self.lbl = tk.Label(
            self.input_f,
            text="Longueur réelle (mm)",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
        )
        self.lbl.pack(side="left")
        self.ent = ttk.Entry(
            self.input_f, textvariable=self.app.distance_saisie, width=10
        )
        self.ent.pack(side="right")
        self.btn = ttk.Button(
            self,
            text="Appliquer l'Échelle",
            command=self.apply_scale,
            style="Primary.TButton",
        )
        self.btn.pack(fill="x", pady=(10, 0))

    def update_view(self, *args):
        state = "normal" if self.app.flag_echelle_frame.get() else "disabled"
        self.btn.config(state=state)
        self.ent.config(state=state)

    def apply_scale(self):
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
    """Conteneur principal de la barre latérale, avec scrollbar intégrée pour les cartes d'interaction"""

    def __init__(self, parent, app, **kwargs):
        # On extrait la largeur pour la fixer
        width = kwargs.get("width", 320)
        super().__init__(parent, bg=kwargs.get("bg"), width=width)
        self.app = app
        self.canvas = tk.Canvas(
            self, bg=kwargs.get("bg"), highlightthickness=0, width=width
        )
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=kwargs.get("bg"))
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw", width=width
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Placement du canvas et de la scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        # Liaison de la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Initialisation des cadres de mesures
        self._setup_measurements()
        self.interraction_GUI()

    def _setup_measurements(self):
        self.app.mesures_supp.mesures_supp_frame = tk.Frame(
            self.scrollable_frame, bg="#F0F2F5"
        )
        for m in self.app.mesures_supp.mes_mesures_supp.values():
            m.mesure_frame = tk.Frame(self.app.mesures_supp.mesures_supp_frame)

    def interraction_GUI(self):
        image_frame(self.scrollable_frame, self.app).pack(
            fill="x", padx=10, pady=(0, 15)
        )
        Echelle_frame(self.scrollable_frame, self.app).pack(
            fill="x", padx=10, pady=(0, 15)
        )
        self.m_card = Card(self.scrollable_frame, title="Mesures de contrôle")
        self.m_card.pack(fill="x", padx=10, pady=(0, 15))
        # Re-parentage de la frame de mesures
        self.app.mesures_supp.mesures_supp_frame.master = self.m_card
        self.app.mesures_supp.mesures_supp_frame.pack(fill="x")
        self.app.mesures_supp.mesures_supp_GUI()

    def _on_mousewheel(self, event):
        """Permet de scroller avec la molette"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
