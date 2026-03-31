"""
 Module pour la fenêtre d'affichage de l'image et 
la gestion des interactions directes (déplacement, zoom, manipulation des points) """

import tkinter as tk
from PIL import Image, ImageTk
from utils.point_manager import bool_pt_appuye

class FenetreImage(tk.Canvas):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.app.img.img_path.trace_add("write", self._maj_fenetre)
        self.app.modif_canvas.trace_add("write", self._maj_fenetre)
        self.deb_deplc_img = []
        self.deb_deplc_pt = []
        self.pt_appuye = False
        self.key_pt = None
        self.bind("<ButtonPress-3>", self._deplacement_start)
        self.bind("<B3-Motion>", self._deplacement_move) 
        self.bind("<MouseWheel>", self._zoom)
        self.bind("<ButtonPress-1>", self._handl_pt_start)
        self.bind("<B1-Motion>", self._handl_pt_move)

    def _maj_fenetre(self, *args):
        path = self.app.img.img_path.get()
        if not path: return
        try:
            self.app.img.Image_img = Image.open(path)
            img_orig = self.app.img.Image_img
            zoom = self.app.zoom_factor.get()
            new_w, new_h = int(img_orig.width * zoom), int(img_orig.height * zoom)
            img_resized = img_orig.resize((new_w, new_h), Image.LANCZOS)
            self.image_ref = ImageTk.PhotoImage(img_resized) # Stockage local
            self.app.img.tk_image = self.image_ref # Stockage dans l'état global
            self.delete('all')
            orig = self.app.img.coord_origine.get()
            # On dessine l'image d'abord
            self.create_image(orig["x"], orig["y"], anchor="nw", image=self.image_ref)
            # Puis on dessine les mesures par-dessus
            for mesure in self.app.list_mesures:
                if mesure.flag_affiche_ptLigne.get():
                    self._dessiner_mesure(mesure, zoom, orig)
        except Exception as e:
            print(f"Erreur de rendu : {e}")

    def _dessiner_mesure(self, mesure, zoom, orig):
        pts_canvas = []
        for pt in mesure.pts.values():
            if pt.created:
                # Calcul des coordonnées écran
                cx = (pt.coord_pt_img["x"] * zoom) + orig["x"]
                cy = (pt.coord_pt_img["y"] * zoom) + orig["y"]
                pt.coord_pt_canvas = {"x": cx, "y": cy}
                self.create_oval(cx-5, cy-5, cx+5, cy+5, fill=pt.color, outline="white")
                pts_canvas.append((cx, cy))
        if len(pts_canvas) == 2:
            self.create_line(pts_canvas[0][0], pts_canvas[0][1], 
                             pts_canvas[1][0], pts_canvas[1][1], 
                             fill=mesure.color, width=2)

    def _deplacement_start(self, event):
        self.deb_deplc_img = [event.x, event.y]

    def _deplacement_move(self, event):
        dx, dy = event.x - self.deb_deplc_img[0], event.y - self.deb_deplc_img[1]
        orig = self.app.img.coord_origine.get()
        self.app.img.coord_origine.set({"x": orig["x"] + dx, "y": orig["y"] + dy})
        self.deb_deplc_img = [event.x, event.y]
        self._maj_fenetre()

    def _zoom(self, event):
        old_zoom = self.app.zoom_factor.get()
        step = 1.1 if event.delta > 0 else 0.9
        new_zoom = old_zoom * step
        self.app.zoom_factor.set(new_zoom)
        orig = self.app.img.coord_origine.get()
        new_x = event.x - (event.x - orig["x"]) * step
        new_y = event.y - (event.y - orig["y"]) * step
        self.app.img.coord_origine.set({"x": new_x, "y": new_y})
        self._maj_fenetre()

    def _handl_pt_start(self, event):
        if not self.app.img.Image_img: return
        idx = self.app.choix_mesure.get()
        mesure_active = self.app.list_mesures[idx]
        self.key_pt, self.pt_appuye = bool_pt_appuye(mesure_active, event)
        if self.pt_appuye:
            self.deb_deplc_pt = [event.x, event.y]
        else:
            mesure_active.add_pt(event)
        self._maj_fenetre()

    def _handl_pt_move(self, event):
        if self.pt_appuye:
            idx = self.app.choix_mesure.get()
            self.app.list_mesures[idx].deplacer_pts(self.key_pt, event, self.deb_deplc_pt)
            self.deb_deplc_pt = [event.x, event.y]
            self._maj_fenetre()