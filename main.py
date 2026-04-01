"""
Page d'entrée de l'application de calibrage de caméra. 
lle lance l'interface graphique principale."""

from ui.main_window import ApplicationCalibrage

if __name__ == "__main__":
    app = ApplicationCalibrage()
    app.mainloop()
