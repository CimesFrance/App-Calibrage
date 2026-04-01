"""
Module de gestion des differentes mesures supplémentaires (distance entre 2 points)
Chaque mesure est représentée par une instance de la classe "UneMesure ", qui gère :
- Les points de mesure (pt1 et pt2) avec leurs coordonnées en image et en canvas
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from core.state import PointModel


class UneMesure :
    """Classe représentant une mesure de distance entre 2 points sur l'image.
    Chaque mesure a : - un titre (ex: "Mesure N°1")
    - une couleur d'affichage (ex: rouge)
    - un numéro d'identification (ex: 1)
    - des points de mesure (pt1 et pt2) avec leurs coordonnées en image et en canvas
    - une valeur de longueur calculée
    - des contrôles d'affichage (checkbox pour afficher les points,
    radio pour sélectionner la mesure active)"""

    def __init__(self, title, color, num, app):
        self.title = title
        self.title_label = None
        self.check_affichage = None
        self.label_afficheur_longueure = None
        self.afficheur_longueure = None
        self.color = color
        self.flag_affiche_ptligne = tk.BooleanVar(value=True)
        self.flag_affiche_frame = tk.BooleanVar(value=False)
        self.num = num
        self.longueur = tk.StringVar(value="0.00")
        self.mesure_frame = None
        self.app = app
        self.pts = {"pt1": PointModel(color), "pt2": PointModel(color)}
        self.created = False
        self.flag_affiche_frame.trace_add("write", self.display_state)

    def mesure_gui(self):
        """Construit l'interface graphique de la mesure"""
        if self.mesure_frame:
            self.mesure_frame.configure(bg="#2C3E50", pady=5)
            # Header : Nom + Pastille
            top = tk.Frame(self.mesure_frame, bg="#2C3E50")
            top.pack(fill="x")
            self.title_label = ttk.Label(
                top, text=self.title, style="Sidebar.Subtitle.TLabel"
            )
            self.title_label.pack(side="left")
            self.pastille = tk.Frame(top, bg=self.color, width=10, height=10)
            self.pastille.pack(side="right", padx=5)
            # Dashboard : Valeur en gros
            self.dash = tk.Frame(self.mesure_frame, bg="#34495E", pady=10)
            self.dash.pack(fill="x", pady=5)
            self.lbl_val = ttk.Label(
                self.dash, textvariable=self.longueur, style="Value.TLabel"
            )
            self.lbl_val.pack(side="left", padx=10)
            self.lbl_unit = ttk.Label(self.dash, text="mm", style="Unit.TLabel")
            self.lbl_unit.pack(side="right", padx=10)
            # Contrôles discrets
            btm = tk.Frame(self.mesure_frame, bg="#2C3E50")
            btm.pack(fill="x")
            self.check_affichage = ttk.Checkbutton(
                btm,
                text="Afficher",
                variable=self.flag_affiche_ptligne,
                style="Sidebar.TCheckbutton",
                command=self._affiche_mesure,
            )
            self.check_affichage.pack(side="left")
            self.radio_saisir = ttk.Radiobutton(
                btm,
                text="Saisir",
                value=self.num,
                variable=self.app.choix_mesure,
                style="Sidebar.TRadiobutton",
            )
            self.radio_saisir.pack(side="right")

    def _affiche_mesure(self):
        """Active ou désactive l'affichage de la mesure"""
        current = self.app.modif_canvas.get()
        self.app.modif_canvas.set(not current)

    def display_state(self, *args):
        """Met à jour l'affichage de la mesure"""
        is_active = self.flag_affiche_frame.get()
        etat = "normal" if is_active else "disabled"
        if hasattr(self, "title_label") and self.title_label:
            self.title_label.config(state=etat)
            self.check_affichage.config(state=etat)
            self.radio_saisir.config(
                state="normal"
            )  # Toujours actif pour cibler l'ajout
            self.lbl_val.config(state=etat)

            # Styles dynamiques
            dash_bg = "#34495E" if is_active else "#2C3E50"
            val_style = "Value.TLabel" if is_active else "DisabledValue.TLabel"
            unit_style = "Unit.TLabel" if is_active else "DisabledUnit.TLabel"
            pastille_co = self.color if is_active else "#7F8C8D"

            self.dash.config(bg=dash_bg)
            self.lbl_val.config(style=val_style)
            self.lbl_unit.config(style=unit_style)
            self.pastille.config(bg=pastille_co)

    def add_pt(self, event):
        """Ajoute un point à la mesure"""
        orig = self.app.img.coord_origine.get()
        zoom = self.app.zoom_factor.get()
        # Conversion coordonnées Canvas -> Image source (pixel réel)
        x_img = (event.x - orig["x"]) / zoom
        y_img = (event.y - orig["y"]) / zoom
        for pt in self.pts.values():
            if not pt.created:
                pt.coord_pt_img = {"x": x_img, "y": y_img}
                pt.created = True
                break
        if self.pts["pt1"].created and self.pts["pt2"].created:
            self.created = True
            self.longueur.set(str(self.calcul_distance()))

    def supprimer_pts(self):
        """Supprime les points de la mesure"""
        for pt in self.pts.values():
            pt.supprimer_pt()

    def maj_pos_pts(self):
        """Met à jour la position des points"""
        orig = self.app.img.coord_origine.get()
        zoom = self.app.zoom_factor.get()
        for pt in self.pts.values():
            if pt.created:
                pt.coord_pt_canvas["x"] = (pt.coord_pt_img["x"] * zoom) + orig["x"]
                pt.coord_pt_canvas["y"] = (pt.coord_pt_img["y"] * zoom) + orig["y"]

    def deplacer_pts(self, key_pt, event, deb_deplc_pt):
        """Déplace un point de la mesure"""
        zoom = self.app.zoom_factor.get()
        dx_img = (event.x - deb_deplc_pt[0]) / zoom
        dy_img = (event.y - deb_deplc_pt[1]) / zoom
        self.pts[key_pt].coord_pt_img["x"] += dx_img
        self.pts[key_pt].coord_pt_img["y"] += dy_img
        if self.pts["pt1"].created and self.pts["pt2"].created:
            self.longueur.set(str(self.calcul_distance()))

    def calcul_distance(self):
        """Calcule la distance entre les deux points"""
        if not (self.pts["pt1"].created and self.pts["pt2"].created):
            return 0.00
        p1, p2 = self.pts["pt1"].coord_pt_img, self.pts["pt2"].coord_pt_img
        # Distance euclidienne pure sur l'image
        dist_px = np.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)
        # Application du facteur de conversion (mm/pixel)
        dist_reelle = dist_px * self.app.facteur_conversion.get()
        return round(dist_reelle, 2)


class MesureSupp:
    """Classe pour gérer les mesures supplémentaires"""
    def __init__(self, app):
        self.app = app
        self.mesures_supp_frame = None
        self.mes_mesures_supp = {
            "Mesure_supp_1": UneMesure ("Mesure N°1", "green", 1, self.app),
            "Mesure_supp_2": UneMesure ("Mesure N°2", "blue", 2, self.app),
            "Mesure_supp_3": UneMesure ("Mesure N°3", "yellow", 3, self.app),
        }
        self.app.flag_mesures_supp_affiche.trace_add("write", self.display_state)

    def mesures_supp_gui(self):
        """Construit l'interface graphique des mesures supplémentaires"""
        if self.mesures_supp_frame is not None:
            self.btn_ajouter = ttk.Button(
                self.mesures_supp_frame,
                text="Ajouter",
                command=self._ajouter_mesure,
                style="TButton",
            )
            self.btn_supprimer = ttk.Button(
                self.mesures_supp_frame,
                text="Supprimer",
                command=self._supprimer_mesure,
                style="Secondary.TButton",
            )
            self.btn_ajouter.grid(row=0, column=0, sticky="we", padx=2, pady=(0, 10))
            self.btn_supprimer.grid(row=0, column=1, sticky="we", padx=2, pady=(0, 10))
            for i, (cle, mesure) in enumerate(self.mes_mesures_supp.items(), start=1):
                mesure.mesure_gui()
                mesure.mesure_frame.grid(
                    row=i, column=0, columnspan=2, sticky="nsew", padx=2, pady=2
                )
            self.mesures_supp_frame.columnconfigure(0, weight=1)
            self.mesures_supp_frame.columnconfigure(1, weight=1)

    def display_state(self, *args):
        """Met à jour l'affichage des mesures supplémentaires"""
        etat = "normal" if self.app.flag_mesures_supp_affiche.get() else "disabled"
        self.btn_ajouter.config(state=etat)
        self.btn_supprimer.config(state=etat)

    def _ajouter_mesure(self):
        """Ajoute une mesure supplémentaire"""
        num = self.app.choix_mesure.get()
        key = f"Mesure_supp_{num}"
        if num > 0 and key in self.mes_mesures_supp:
            self.mes_mesures_supp[key].longueur.set("0.00")
            self.mes_mesures_supp[key].flag_affiche_frame.set(True)
            self.mes_mesures_supp[key].created = True

    def _supprimer_mesure(self):
        """Supprime une mesure supplémentaire"""
        num = self.app.choix_mesure.get()
        key = f"Mesure_supp_{num}"
        if num > 0 and key in self.mes_mesures_supp:
            m = self.mes_mesures_supp[key]
            # Désactivation
            m.longueur.set("- - -")
            m.flag_affiche_frame.set(False)
            m.created = False
            m.supprimer_pts()  # Nettoie les coordonnées
            current = self.app.modif_canvas.get()
            self.app.modif_canvas.set(not current)
