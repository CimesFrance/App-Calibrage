"""
 Module pour la fenêtre d'affichage de l'image et
la gestion des interactions directes (déplacement, zoom, manipulation des points)"""

import tkinter as tk
from PIL import Image, ImageTk
from utils.point_manager import bool_pt_appuye


class FenetreImage(tk.Canvas):
    """Classe pour afficher l'image et les mesures. """
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.app.img.img_path.trace_add("write", self._maj_fenetre)
        self.app.modif_canvas.trace_add("write", self._maj_fenetre)
        self.deb_deplc_img = []
        self.deb_deplc_pt = []
        self.pt_appuye = False
        self.key_pt = None
        self.config(cursor="crosshair")  # Curseur par défaut en croix de précision
        self.bind("<ButtonPress-3>", self._deplacement_start)
        self.bind("<B3-Motion>", self._deplacement_move)
        self.bind("<ButtonRelease-3>", self._deplacement_stop)
        self.bind("<MouseWheel>", self._zoom)
        self.bind("<ButtonPress-1>", self._handl_pt_start)
        self.bind("<B1-Motion>", self._handl_pt_move)

    def _maj_fenetre(self, *args):
        path = self.app.img.img_path.get()
        if not path:
            return
        try:
            self.app.img.ImportImg = Image.open(path)
            img_orig = self.app.img.ImportImg
            zoom = self.app.zoom_factor.get()
            new_w, new_h = int(img_orig.width * zoom), int(img_orig.height * zoom)
            img_resized = img_orig.resize((new_w, new_h), Image.LANCZOS)
            self.image_ref = ImageTk.PhotoImage(img_resized)  # Stockage local
            self.app.img.tk_image = self.image_ref  # Stockage dans l'état global
            self.delete("all")
            orig = self.app.img.coord_origine.get()
            # On dessine l'image d'abord
            self.create_image(orig["x"], orig["y"], anchor="nw", image=self.image_ref)
            # Puis on dessine les mesures par-dessus
            for mesure in self.app.list_mesures:
                if mesure.flag_affiche_ptligne.get():
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
                self.create_oval(
                    cx - 5, cy - 5, cx + 5, cy + 5, fill=pt.color, outline="white"
                )
                pts_canvas.append((cx, cy))
        if len(pts_canvas) == 2:
            self.create_line(
                pts_canvas[0][0],
                pts_canvas[0][1],
                pts_canvas[1][0],
                pts_canvas[1][1],
                fill=mesure.color,
                width=2,
            )

    def _deplacement_start(self, event):
        self.config(cursor="fleur")  # Change le curseur pendant le déplacement
        self.deb_deplc_img = [event.x, event.y]

    def _deplacement_stop(self, event):
        self.config(cursor="crosshair")  # Rétablit le curseur de précision


    def _deplacement_move(self, event):
        img_orig = self.app.img.ImportImg
        if not img_orig: return
        dx, dy = event.x - self.deb_deplc_img[0], event.y - self.deb_deplc_img[1]
        orig = self.app.img.coord_origine.get()
        # Calculer la taille de l'image redimensionnée et du canevas
        zoom = self.app.zoom_factor.get()
        new_w = img_orig.width * zoom
        new_h = img_orig.height * zoom
        canvas_w = self.winfo_width()
        canvas_h = self.winfo_height()
        # Marge de sécurité (px) pour garantir qu'un bout de l'image reste toujours visible
        margin = 100 
        min_x = -new_w + margin
        max_x = canvas_w - margin
        min_y = -new_h + margin
        max_y = canvas_h - margin
        # Clamp (Borner) les nouvelles valeurs
        new_x = max(min_x, min(max_x, orig["x"] + dx))
        new_y = max(min_y, min(max_y, orig["y"] + dy))
        self.app.img.coord_origine.set({"x": new_x, "y": new_y})
        self.deb_deplc_img = [event.x, event.y]
        self._maj_fenetre()

    def _zoom(self, event):
        old_zoom = self.app.zoom_factor.get()
        step = 1.1 if event.delta > 0 else 0.9
        new_zoom = old_zoom * step
        
        # Limite minimale (10%) et maximale (200%) du zoom
        if new_zoom < 0.1:
            new_zoom = 0.1
            step = new_zoom / old_zoom
        elif new_zoom > 2.0:
            new_zoom = 2.0
            step = new_zoom / old_zoom
        self.app.zoom_factor.set(new_zoom)
        orig = self.app.img.coord_origine.get()
        new_x = event.x - (event.x - orig["x"]) * step
        new_y = event.y - (event.y - orig["y"]) * step
        self.app.img.coord_origine.set({"x": new_x, "y": new_y})
        self._maj_fenetre()
        return "break"

    def _handl_pt_start(self, event):
        if not self.app.img.ImportImg:
            return
        idx = self.app.choix_mesure.get()
        mesure_active = self.app.list_mesures[idx]
        if mesure_active.created == False:
            return
        # idx = self.app.choix_mesure.get()
        # mesure_active = self.app.list_mesures[idx]
        self.key_pt, self.pt_appuye = bool_pt_appuye(mesure_active, event)
        if self.pt_appuye:
            self.deb_deplc_pt = [event.x, event.y]
        else:
            mesure_active.add_pt(event)
        self._maj_fenetre()

    def _handl_pt_move(self, event):
        if self.pt_appuye:
            idx = self.app.choix_mesure.get()
            self.app.list_mesures[idx].deplacer_pts(
                self.key_pt, event, self.deb_deplc_pt
            )
            self.deb_deplc_pt = [event.x, event.y]
            self._maj_fenetre()
