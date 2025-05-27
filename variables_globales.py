from cubo import *

COLORES = ["B", "V", "N", "R", "AZ", "AM"]
cube_state = {cara: [[cara for _ in range(3)] for _ in range(3)] for cara in COLORES}

from PyQt6.QtGui import QColor
import random
# 1) Defino COLORES y COLORES_CAMBIABLES
COLORES = ["B", "V", "N", "R", "AZ", "AM"]
COLORES_CAMBIABLES = ["B", "V", "N", "R", "AZ"]

# 2) Defino PALETTES "fijas"
PALETTES = {
    "Default": {
        "B": QColor("white"),
        "V": QColor("green"),
        "N": QColor("orange"),
        "R": QColor("red"),
        "AZ": QColor("blue"),
        "AM": QColor("yellow"),
    },
    "Pastel": {
        "B": QColor(255, 210, 180),  
        "V": QColor(160, 220, 180),  
        "N": QColor(255, 180, 200),  
        "R": QColor(255, 160, 160),  
        "AZ": QColor(180, 200, 255), 
        "AM": QColor(255, 240, 180), 
    },
    "Oscuro": {
        "B": QColor(100, 100),
        "V": QColor(30, 80, 30),
        "N": QColor(80, 40, 10),
        "R": QColor(80, 20, 20),
        "AZ": QColor(20, 20, 80),
        "AM": QColor(80, 80, 20),
    },
    "Brillante": {
        "B": QColor(255, 255, 255),
        "V": QColor(0, 255, 0),
        "N": QColor(255, 165, 0),
        "R": QColor(255, 0, 0),
        "AZ": QColor(0, 0, 255),
        "AM": QColor(255, 255, 0),
    },
    "Colores random": {
        "B": QColor.fromRgbF(random.random(), random.random(), random.random()),
        "V": QColor.fromRgbF(random.random(), random.random(), random.random()),
        "N": QColor.fromRgbF(random.random(), random.random(), random.random()),
        "R": QColor.fromRgbF(random.random(), random.random(), random.random()),
        "AZ": QColor.fromRgbF(random.random(), random.random(), random.random()),
        "AM": QColor.fromRgbF(random.random(), random.random(), random.random()),
    },
}

ROTATION_INDEX = 0
# 4) (Opcional) inicializo el mapa de color activo
COLORES_MAPA = PALETTES["Default"]