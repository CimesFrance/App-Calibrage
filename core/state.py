"""
Module de gestion de l'état de l'application.
Contient les classes ImageModel, PointModel, et AppState qui centralisent les données et
l'état de l'application pour une gestion plus propre et réactive."""

import tkinter as tk
from core.custom_vars import JSONVar
import json
import os


class ImageModel:
    """Classe pour stocker les données de l'image. 
    """
    def __init__(self):
        self.id_img = None
        self.tk_img = None
        self.coord_origine = JSONVar(value={"x": 0, "y": 0})
        self.ImportImg = None
        self.img_path = tk.StringVar(value="")

    def reboot(self):
        """Réinitialise l'image."""
        self.id_img = None
        self.tk_img = None
        self.coord_origine.set({"x": 0, "y": 0})
        self.ImportImg = None


class PointModel:
    """Classe pour stocker les données d'un point. 
    """
    def __init__(self, color):
        self.color = color
        self.coord_pt_img = {"x": 0, "y": 0}
        self.coord_pt_canvas = {"x": 0, "y": 0}
        self.taille = 5
        self.id = None
        self.created = False

    def supprimer_pt(self):
        """Supprime le point."""
        self.coord_pt_img = {"x": 0, "y": 0}
        self.coord_pt_canvas = {"x": 0, "y": 0}
        self.id = None
        self.created = False


class AppState:
    """Classe pour stocker l'état de l'application. 
    """
    def __init__(self):
        from ui.measurements import UneMesure , MesureSupp  # Import local
        self.img = ImageModel()
        self.zoom_factor = tk.DoubleVar(value=1.0)
        self.facteur_conversion = tk.DoubleVar(value=1.0)
        self.distance_saisie = tk.StringVar(value="0.00")
        self.choix_mesure = tk.IntVar(value=0)
        self.flag_mesures_supp_affiche = tk.BooleanVar(value=True)
        self.flage_changer_echelle_affiche = tk.BooleanVar(value=False)
        self.flag_EchelleFrame = tk.BooleanVar(value=False)
        self.flag_save_btn_affiche = tk.BooleanVar(value=False)
        self.modif_canvas = tk.BooleanVar(value=True)
        self.mesure_echelle = UneMesure (
            title="Mesure Echelle", color="red", num=0, app=self
        )
        self._load_mesure_principale()
        self.MesureSupp = MesureSupp(app=self)
        self.list_mesures = [
            self.mesure_echelle,
            self.MesureSupp.mes_mesures_supp["Mesure_supp_1"],
            self.MesureSupp.mes_mesures_supp["Mesure_supp_2"],
            self.MesureSupp.mes_mesures_supp["Mesure_supp_3"],
        ]

    def _load_mesure_principale(self):
        if os.path.exists("mesure_config.json"):
            try:
                with open("mesure_config.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.facteur_conversion.set(data.get("facteur_conversion", 1.0))
                self.distance_saisie.set(data.get("distance_saisie", "0.00"))
                longueur = data.get("longueur", "0.00")
                self.mesure_echelle.longueur.set(longueur)
                
                created = data.get("created", False)
                self.mesure_echelle.created = created
                
                pt1_data = data.get("pt1", {"x": 0, "y": 0})
                self.mesure_echelle.pts["pt1"].coord_pt_img = pt1_data
                self.mesure_echelle.pts["pt1"].created = created
                
                pt2_data = data.get("pt2", {"x": 0, "y": 0})
                self.mesure_echelle.pts["pt2"].coord_pt_img = pt2_data
                self.mesure_echelle.pts["pt2"].created = created
                
                if created:
                    self.flag_EchelleFrame.set(True)
            except Exception as e:
                print("Erreur de chargement de la configuration:", e)
