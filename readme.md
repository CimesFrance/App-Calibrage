# App Calibrage

**Calibration Suite** est une application de métrologie assistée par ordinateur développée en Python. Elle permet de transformer n'importe quelle photographie en un plan de mesure précis grâce à un système d'étalonnage intuitif.

---

## Fonctionnalités

* **Moteur de Zoom Intelligent :** Zoom centré sur le curseur de la souris pour une précision chirurgicale lors du placement des points.
* **Système d'Étalonnage :** Définition d'une échelle réelle (en mm) pour convertir les pixels de l'image en unités de mesure physiques.
* **Mesures Multiples :** Gestion de plusieurs couches de mesures (Echelle + 3 mesures de contrôle) avec codes couleurs distincts.
* **Manipulation Fluide :** Déplacement de l'image (Pan) par clic droit et ajustement des points par "Drag & Drop".

## Details techniques
L'application utilise une conversion de coordonnées entre l'espace Canevas (affichage) et l'espace Image (pixels réels) pour garantir que les mesures restent exactes, quel que soit le niveau de zoom choisi.

Calcul de la distance :
```Distance Réelle = sqrt((x2 - x1)² + (y2 - y1)²) * Facteur de Conversion```

Le système repose sur la persistance des coordonnées dans le référentiel de l'image source, tandis que l'affichage est recalculé dynamiquement lors de chaque rafraîchissement du Canvas pour correspondre au facteur de zoom et au décalage de l'origine.

---

## Installation

### Prérequis
Assurez-vous d'avoir Python 3.x installé. Le projet utilise les bibliothèques suivantes :
* **Pillow (PIL) :** Pour le traitement d'image.
* **NumPy :** Pour les calculs de distances euclidiennes.
* **Pandas :** Pour la gestion des données optionnelles (imports CSV).

### Commandes
```bash
git clone https://github.com/CimesFrance/App-Calibrage.git
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```