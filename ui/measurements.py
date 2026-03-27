"""
Module de gestion des differentes mesures supplémentaires (distance entre 2 points)
Chaque mesure est représentée par une instance de la classe "une_mesure", qui gère :
- Les points de mesure (pt1 et pt2) avec leurs coordonnées en image et en canvas
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from core.state import PointModel


class une_mesure:
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
        self.flag_affiche_ptLigne = tk.BooleanVar(value=True)
        self.flag_affiche_frame = tk.BooleanVar(value=False)
        self.num = num
        self.longueur = tk.StringVar(value="0.00")
        self.mesure_frame = None
        self.app = app
        self.pts = {"pt1": PointModel(color), "pt2": PointModel(color)}
        self.created = False
        self.flag_affiche_frame.trace_add("write", self.display_state)

    def mesure_GUI(self):
        if self.mesure_frame:
            self.mesure_frame.configure(bg="#FFFFFF", pady=5)
            # Header : Nom + Pastille
            top = tk.Frame(self.mesure_frame, bg="#FFFFFF")
            top.pack(fill="x")
            self.title_label = tk.Label(
                top,
                text=self.title,
                font=("Segoe UI", 9, "bold"),
                bg="#FFFFFF",
                fg="#212529",
            )
            self.title_label.pack(side="left")
            pastille = tk.Frame(top, bg=self.color, width=10, height=10)
            pastille.pack(side="right", padx=5)
            # Dashboard : Valeur en gros
            dash = tk.Frame(self.mesure_frame, bg="#F8F9FA", pady=10)
            dash.pack(fill="x", pady=5)
            self.lbl_val = tk.Label(
                dash,
                textvariable=self.longueur,
                font=("Consolas", 14, "bold"),
                bg="#F8F9FA",
                fg="#0056B3",
            )
            self.lbl_val.pack(side="left", padx=10)
            tk.Label(
                dash, text="mm", font=("Segoe UI", 8), bg="#F8F9FA", fg="#ADB5BD"
            ).pack(side="right", padx=10)
            # Contrôles discrets
            btm = tk.Frame(self.mesure_frame, bg="#FFFFFF")
            btm.pack(fill="x")
            tk.Checkbutton(
                btm,
                text="Afficher",
                variable=self.flag_affiche_ptLigne,
                bg="#FFFFFF",
                font=("Segoe UI", 8),
            ).pack(side="left")
            tk.Radiobutton(
                btm,
                text="Saisir",
                value=self.num,
                variable=self.app.choix_mesure,
                bg="#FFFFFF",
                font=("Segoe UI", 8),
            ).pack(side="right")

    def _affiche_mesure(self):
        self.app.modif_canvas.set(True)

    def display_state(self, *args):
        etat = "normal" if self.flag_affiche_frame.get() else "disabled"
        self.title_label.config(state=etat)
        self.check_affichage.config(state=etat)
        self.label_afficheur_longueure.config(state=etat)
        self.afficheur_longueure.config(state=etat)

    def add_pt(self, event):
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
        for pt in self.pts.values():
            pt.supprimer_pt()

    def maj_pos_pts(self):
        orig = self.app.img.coord_origine.get()
        zoom = self.app.zoom_factor.get()
        for pt in self.pts.values():
            if pt.created:
                pt.coord_pt_canvas["x"] = (pt.coord_pt_img["x"] * zoom) + orig["x"]
                pt.coord_pt_canvas["y"] = (pt.coord_pt_img["y"] * zoom) + orig["y"]

    def deplacer_pts(self, key_pt, event, deb_deplc_pt):
        zoom = self.app.zoom_factor.get()
        dx_img = (event.x - deb_deplc_pt[0]) / zoom
        dy_img = (event.y - deb_deplc_pt[1]) / zoom
        self.pts[key_pt].coord_pt_img["x"] += dx_img
        self.pts[key_pt].coord_pt_img["y"] += dy_img
        if self.pts["pt1"].created and self.pts["pt2"].created:
            self.longueur.set(str(self.calcul_distance()))

    def calcul_distance(self):
        if not (self.pts["pt1"].created and self.pts["pt2"].created):
            return 0.00
        p1, p2 = self.pts["pt1"].coord_pt_img, self.pts["pt2"].coord_pt_img
        # Distance euclidienne pure sur l'image
        dist_px = np.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)
        # Application du facteur de conversion (mm/pixel)
        dist_reelle = dist_px * self.app.facteur_conversion.get()
        return round(dist_reelle, 2)


class mesures_supp:
    def __init__(self, app):
        self.app = app
        self.mesures_supp_frame = None
        self.mes_mesures_supp = {
            "Mesure_supp_1": une_mesure("Mesure N°1", "green", 1, self.app),
            "Mesure_supp_2": une_mesure("Mesure N°2", "blue", 2, self.app),
            "Mesure_supp_3": une_mesure("Mesure N°3", "yellow", 3, self.app),
        }
        self.app.flag_mesures_supp_affiche.trace_add("write", self.display_state)

    def mesures_supp_GUI(self):
        if self.mesures_supp_frame is not None:
            title = tk.Label(
                self.mesures_supp_frame, text="Mesures", font=("Arial", 14, "bold")
            )
            separator = tk.Frame(self.mesures_supp_frame, bg="black", height=2)
            self.btn_ajouter = ttk.Button(
                self.mesures_supp_frame, text="Ajouter", command=self._ajouter_mesure
            )
            self.btn_supprimer = ttk.Button(
                self.mesures_supp_frame,
                text="Supprimer",
                command=self._supprimer_mesure,
            )
            title.grid(row=0, column=0, columnspan=2, sticky="we", padx=2, pady=2)
            separator.grid(row=1, column=0, columnspan=2, sticky="we", padx=2, pady=2)
            self.btn_ajouter.grid(row=2, column=0, sticky="we", padx=2, pady=2)
            self.btn_supprimer.grid(row=2, column=1, sticky="we", padx=2, pady=2)
            for i, (cle, mesure) in enumerate(self.mes_mesures_supp.items(), start=3):
                mesure.mesure_GUI()
                mesure.mesure_frame.grid(
                    row=i, column=0, columnspan=2, sticky="nsew", padx=2, pady=2
                )
            self.mesures_supp_frame.columnconfigure(0, weight=1)
            self.mesures_supp_frame.columnconfigure(1, weight=1)

    def display_state(self, *args):
        etat = "normal" if self.app.flag_mesures_supp_affiche.get() else "disabled"
        self.btn_ajouter.config(state=etat)
        self.btn_supprimer.config(state=etat)

    def _ajouter_mesure(self):
        num = self.app.choix_mesure.get()
        key = f"Mesure_supp_{num}"
        if num > 0 and key in self.mes_mesures_supp:
            self.mes_mesures_supp[key].flag_affiche_frame.set(True)
            self.mes_mesures_supp[key].created = True

    def _supprimer_mesure(self):
        num = self.app.choix_mesure.get()
        key = f"Mesure_supp_{num}"
        if num > 0 and key in self.mes_mesures_supp:
            m = self.mes_mesures_supp[key]
            # Désactivation
            m.flag_affiche_frame.set(False)
            m.created = False
            m.supprimer_pts()  # Nettoie les coordonnées
            m.longueur.set("0.00")
            # Si modif_canvas était déjà à True, le remettre à True ne ferait rien sur certains systèmes
            current = self.app.modif_canvas.get()
            self.app.modif_canvas.set(not current)
