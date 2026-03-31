""" 
 Module de gestion de l'état de l'application. 
 Contient les classes ImageModel, PointModel, et AppState qui centralisent les données et
 l'état de l'application pour une gestion plus propre et réactive."""

import tkinter as tk
from core.custom_vars import JSONVar

class ImageModel:
    def __init__(self):
        self.id_img = None
        self.tk_img = None
        self.coord_origine = JSONVar(value={"x": 0, "y": 0})
        self.Image_img = None
        self.img_path = tk.StringVar(value="")
    
    def reboot(self):
        self.id_img = None 
        self.tk_img = None 
        self.coord_origine.set({"x": 0, "y": 0})
        self.Image_img = None

class PointModel:
    def __init__(self, color):
        self.color = color
        self.coord_pt_img = {"x": 0, 'y': 0}
        self.coord_pt_canvas = {"x": 0, 'y': 0} 
        self.taille = 5
        self.id = None
        self.created = False  

    def supprimer_pt(self):
        self.coord_pt_img = {"x": 0, 'y': 0}
        self.coord_pt_canvas = {"x": 0, 'y': 0} 
        self.id = None
        self.created = False

class AppState:
    def __init__(self):
        from ui.measurements import une_mesure, mesures_supp # Import local pour éviter 
        self.img = ImageModel()
        self.zoom_factor = tk.DoubleVar(value=1.0)
        self.facteur_conversion = tk.DoubleVar(value=1.0)
        self.distance_saisie = tk.StringVar(value='0.00')
        self.choix_mesure = tk.IntVar(value=0)
        self.flag_mesures_supp_affiche = tk.BooleanVar(value=True)
        self.flage_changer_echelle_affiche = tk.BooleanVar(value=False)
        self.flag_echelle_frame = tk.BooleanVar(value=False)
        self.flag_save_btn_affiche = tk.BooleanVar(value=False)
        self.modif_canvas = tk.BooleanVar(value=True)
        self.mesure_echelle = une_mesure(title="Mesure Echelle", color='red', num=0, app=self)
        self.mesures_supp = mesures_supp(app=self)
        self.list_mesures = [
            self.mesure_echelle, 
            self.mesures_supp.mes_mesures_supp["Mesure_supp_1"],
            self.mesures_supp.mes_mesures_supp["Mesure_supp_2"], 
            self.mesures_supp.mes_mesures_supp["Mesure_supp_3"]
        ]
        


    