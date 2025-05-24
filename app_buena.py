import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,  QPushButton, QStackedWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtWidgets import QTextEdit,QGridLayout, QHBoxLayout, QWidget, QVBoxLayout, QWidget, QPushButton, QLabel, QMessageBox, QInputDialog
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from cubo import *
from grafo import *
import random
from variables_globales import *
import traceback
from orbitas import *
import gettext
from traducciones import t

# para las traducciones
_ = gettext.gettext

# ---------------------------
# Estado global del cubo
# ---------------------------
# Lista de identificadores de caras (usada para el ciclo de colores)
COLORES = ["B", "V", "N", "R", "AZ", "AM"]
COLORES_CAMBIABLES = ["B", "V", "N", "R", "AZ"]  # Solo estas caras son cambiables
# Mapa de colores (PyQt) para cada cara
COLORES_MAPA = {
    "B": QColor("white"),   # Up (Blanco)
    "V": QColor("green"),   # Left (Verde)
    "N": QColor("orange"),  # Back (Naranja)
    "R": QColor("red"),     # Front (Rojo)
    "AZ": QColor("blue"),   # Right (Azul)
    "AM": QColor("yellow")   # Down (Amarillo)
}

# Definimos nombres para las casillas según su posición
NOMBRES_ARISTAS = {(0, 1): "a", (1, 0): "b", (2, 1): "c", (1, 2): "d"}
NOMBRES_VERTICES = {(0, 0): "e", (2, 0): "f", (2, 2): "g", (0, 2): "h"}

# Definimos los colores secundarios que compone cada casilla de la cara blanca según su posición
ARISTAS_LATERAL = {(0, 1): "R", (1, 0): "AZ", (2, 1): "N", (1, 2): "V"}
ESQUINAS_LATERAL = {(0, 0): ("R", "AZ"), (2, 0): ("AZ", "N"), (2, 2): ("N", "V"), (0, 2): ("V", "R")}

def colorFromLetter(letter):
    """Devuelve una tupla RGB normalizada a partir de la letra de la cara."""
    color = COLORES_MAPA[letter]
    return (color.redF(), color.greenF(), color.blueF())

POSICIONES_CARAS = {
    "R":  (3, 0),
    "AZ":  (0, 3),
    "B":  (3, 3),
    "V":  (6, 3),
    "AM": (9, 3),
    "N": (3, 6)
}
TILE_SIZE = 40

class CuboTile(QGraphicsRectItem):
    def __init__(self, x, y, size, cara, fila, columna, cube3d):
        super().__init__(x, y, size, size)
        self.cara = cara
        self.fila = fila
        self.columna = columna
        self.cube3d = cube3d
        self.color_actual = cube_state[cara][fila][columna]
        self.setBrush(QBrush(COLORES_MAPA[self.color_actual]))
        self.setPen(QPen(Qt.GlobalColor.black, 2))
       
        
    def mousePressEvent(self, event):
        # Lógica de cambio de color:
        # - Si es la cara blanca ("B") y la casilla no es la central, o
        # - Si es una cara contigua a la blanca (V, N, R, AZ) y es la fila 0.
        if self.cara == "B" and not (self.fila == 1 and self.columna == 1):
            self.cambiar_color()
        elif self.cara == "R" and self.fila == 2:
            self.cambiar_color()
        elif self.cara == "AZ" and self.columna == 2:
            self.cambiar_color()
        elif self.cara == "V" and self.columna == 0:
            self.cambiar_color()
        elif self.cara == "N" and self.fila == 0:
            self.cambiar_color()
        # Actualizamos el estado global
        cube_state[self.cara][self.fila][self.columna] = self.color_actual  
        # actualizamos la vista 3D
        self.cube3d.update()

    def cambiar_color(self):
        indice_actual = COLORES_CAMBIABLES.index(self.color_actual)
        nuevo_color = COLORES_CAMBIABLES[(indice_actual + 1) % len(COLORES_CAMBIABLES)]
        self.setBrush(QBrush(COLORES_MAPA[nuevo_color]))
        self.color_actual = nuevo_color

class RubiksCubeNet(QGraphicsView):
    def __init__(self, parent=None, cube3d=None):
        super().__init__(parent)
        self.setFixedSize(1000, 800)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.cube3d = cube3d
        self.setBackgroundBrush(QColor(25, 25, 25))
        self.scene.setSceneRect(0, 0, 600, 500)
        self.tile = None
        self.drawNet()
        

    def drawNet(self):
        self.scene.clear()
        for cara, (grid_x, grid_y) in POSICIONES_CARAS.items():
            for fila in range(3):
                for col in range(3):
                    x = (grid_x + col) * TILE_SIZE
                    y = (grid_y + fila) * TILE_SIZE
                    self.tile = CuboTile(x, y, TILE_SIZE, cara, fila, col, self.cube3d)
                    self.scene.addItem(self.tile)

    
    def get_cubotile(self):
        return self.tile

class RubiksCube3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xRot = 0
        self.yRot = 0
        self.lastPos = QPoint()
        self.cubeSize = 2.0
        self.gap = 0.1


    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        glDisable(GL_LIGHTING) 

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h if h else 1, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -25)
        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        self.drawCube()
        

    def drawCube(self):
        totalSize = 3 * self.cubeSize + 2 * self.gap
        offset = totalSize/2 - self.cubeSize/2
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    glPushMatrix()
                    x = i * (self.cubeSize + self.gap) - offset
                    y = j * (self.cubeSize + self.gap) - offset
                    z = k * (self.cubeSize + self.gap) - offset
                    glTranslatef(x, y, z)
                    self.drawSmallCube(self.cubeSize, i, j, k)
                    glPopMatrix()
                    

    def drawSmallCube(self, size, i, j, k):
        hs = size / 2

        # --- Frente  ---
        glBegin(GL_QUADS)
        if k == 2:
            row = 2 - j
            col = i
            face_letter = cube_state["B"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(-hs, -hs, hs)
        glVertex3f(hs, -hs, hs)
        glVertex3f(hs, hs, hs)
        glVertex3f(-hs, hs, hs)
        glEnd()

        # --- Atrás ---
        glBegin(GL_QUADS)
        if k == 0:
            row = 2 - j
            col = 2 - i
            face_letter = cube_state["AM"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(-hs, -hs, -hs)
        glVertex3f(-hs, hs, -hs)
        glVertex3f(hs, hs, -hs)
        glVertex3f(hs, -hs, -hs)
        glEnd()

        # --- Izquierda ---
        glBegin(GL_QUADS)
        if i == 0:
            row = 2 - j
            col = k
            face_letter = cube_state["AZ"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(-hs, -hs, hs)
        glVertex3f(-hs, hs, hs)
        glVertex3f(-hs, hs, -hs)
        glVertex3f(-hs, -hs, -hs)
        glEnd()

        # --- Derecha ---
        glBegin(GL_QUADS)
        if i == 2:
            row = 2 - j
            col = 2 - k
            face_letter = cube_state["V"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(hs, -hs, hs)
        glVertex3f(hs, -hs, -hs)
        glVertex3f(hs, hs, -hs)
        glVertex3f(hs, hs, hs)
        glEnd()

        # --- Arriba ---
        glBegin(GL_QUADS)
        if j == 2:
            row = k
            col = i
            face_letter = cube_state["R"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(-hs, hs, hs)
        glVertex3f(hs, hs, hs)
        glVertex3f(hs, hs, -hs)
        glVertex3f(-hs, hs, -hs)
        glEnd()

        # --- Abajo ---
        glBegin(GL_QUADS)
        if j == 0:
            row = 2 - k
            col = i
            face_letter = cube_state["N"][row][col]
            glColor3f(*colorFromLetter(face_letter))
        else:
            glColor3f(0.2, 0.2, 0.2)
        glVertex3f(-hs, -hs, hs)
        glVertex3f(-hs, -hs, -hs)
        glVertex3f(hs, -hs, -hs)
        glVertex3f(hs, -hs, hs)
        glEnd()

    def mousePressEvent(self, event):
        self.lastPos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        dx = event.position().x() - self.lastPos.x()
        dy = event.position().y() - self.lastPos.y()
        self.xRot += dy
        self.yRot += dx
        self.lastPos = event.position().toPoint()
        self.update()


class SolutionWidget(QWidget):
    def __init__(
        self,
        secuencia_movimientos, historial,
        piecita_cambiada, sentido, cubo_modelo,
        movimiento_origen, lang,
        parent=None
    ):
        super().__init__(parent)
        self.lang = lang
        self.setWindowTitle(t('solution_complete', self.lang))

        # Estados de vista
        self.showingFullCube = False
        self.flip_shown = (piecita_cambiada is None)
        self.flip_end_shown = False
        self.current_step = 0

        # Datos del algoritmo
        self.cubo = cubo_modelo
        self.secuencia_movimientos = secuencia_movimientos
        self.historial = historial
        self.piecita_cambiada = piecita_cambiada
        self.sentido = sentido
        self.movimiento_origen = movimiento_origen

        # Layout principal
        self.mainLayout = QHBoxLayout(self)

        # Panel izquierdo
        self.leftPanel = QWidget()
        leftLayout = QVBoxLayout(self.leftPanel)

        self.comentario = QTextEdit()
        self.comentario.setReadOnly(True)
        leftLayout.addWidget(self.comentario, 1)

        self.instructionsText = QTextEdit()
        self.instructionsText.setReadOnly(True)
        leftLayout.addWidget(self.instructionsText, 1)

        self.nextStepBtn = QPushButton()
        self.nextStepBtn.clicked.connect(self.nextStep)
        leftLayout.addWidget(self.nextStepBtn)

        self.volverBtn = QPushButton()
        self.volverBtn.clicked.connect(self.volverMenu)
        leftLayout.addWidget(self.volverBtn)

        # Botón toggle central
        self.toggleViewBtn = QPushButton()
        self.toggleViewBtn.setFixedSize(40, 40)
        self.toggleViewBtn.setText("<<")
        self.toggleViewBtn.setStyleSheet("""
            QPushButton { border-radius: 20px; background-color: #B8F58E;
                         color: #55917F; font-weight: bold; font-size: 18px; }
            QPushButton:hover { background-color: #9bf15f; }
        """)
        self.toggleViewBtn.clicked.connect(self.toggleView)
        self.toggleViewBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        buttonContainer = QVBoxLayout()
        buttonContainer.addStretch()
        buttonContainer.addWidget(self.toggleViewBtn)
        buttonContainer.addStretch()
        self.middleWidget = QWidget()
        self.middleWidget.setLayout(buttonContainer)

        # Panel 3D derecho
        self.cube3DView = RubiksCube3D()

        # Montaje layout
        self.mainLayout.addWidget(self.leftPanel, 3)
        self.mainLayout.addWidget(self.middleWidget)
        self.mainLayout.addWidget(self.cube3DView, 3)

        # Inicializar textos y estado
        self.retranslate()
        self.updateStep()

    def retranslate(self):
        # Texto explicativo
        self.comentario.setText(t('coment', self.lang))
        # Botones
        self.nextStepBtn.setText(t('next_step', self.lang) )
        self.volverBtn.setText(t('goto_menu', self.lang) )
        # Toggle view button remains an icon or arrows

    def updateStep(self):
        total = len(self.secuencia_movimientos) + 2
        # --- Si no hay pieza desorientada (órbita canónica), vamos directo a movimientos canónicos ---
        if self.piecita_cambiada is None:
            total = len(self.secuencia_movimientos)
            # Muestra el primer movimiento canónico
            if self.current_step < len(self.secuencia_movimientos):
                mov = self.secuencia_movimientos[self.current_step]
                texto = t(f"{mov}", self.lang)
                self.instructionsText.setPlainText(
                    f"{t('step', self.lang)} {self.current_step+1}/{total}:\n{texto}"
                )
            else:
                self.instructionsText.setPlainText(t('solution_complete', self.lang))
                self.nextStepBtn.setEnabled(False)
            return

        # --- Paso 0: flip inicial ---
        if not self.flip_shown:
            self.instructionsText.setPlainText(
                f"{t('step', self.lang)} 0/{total}:\n{t('arista_flipped', self.lang)}"
            )
            return

        # --- Paso final: flip de vuelta ---
        if self.flip_shown and not self.flip_end_shown and self.current_step >= len(self.secuencia_movimientos):
            paso = len(self.secuencia_movimientos) + 1
            self.instructionsText.setPlainText(
                f"{t('step', self.lang)} {paso}/{total}:\n{t('arista_flipped', self.lang)}"
            )
            return

        # --- Pasos intermedios canónicos ---
        idx = self.current_step
        if idx < len(self.secuencia_movimientos):
            mov = self.secuencia_movimientos[idx]
            texto = t(f"{mov}", self.lang)
            self.instructionsText.setPlainText(
                f"{t('step', self.lang)} {idx+1}/{total}:\n{texto}"
            )
        else:
            self.instructionsText.setPlainText(t('solution_complete', self.lang))
            self.nextStepBtn.setEnabled(False)

            
    def nextStep(self):
        # --- Paso 0: flip inicial ---
        if not self.flip_shown:
            orb = Orbitas(self.movimiento_origen)

            if isinstance(self.piecita_cambiada, (list, tuple)) and len(self.piecita_cambiada) == 2:
                # es una arista
                pieza = orb.buscar_posicion_por_color_arista(self.cubo,
                                                            self.piecita_cambiada)
                i,j   = pieza.fila, pieza.columna
                ia,ja = pieza.adyacente.fila, pieza.adyacente.columna
                cara0, cara1 = pieza.cara, pieza.adyacente.cara
                c0 = cube_state[cara0][i][j]
                c1 = cube_state[cara1][ia][ja]
                    
                if self.sentido == None:
                    cube_state[cara0][i][j] = c1
                    cube_state[cara1][ia][ja] = c0
                    orb.flippear_arista(self.cubo, (i,j))
                    
            else:
                # es una esquina (longitud==3)
                pieza = orb.buscar_posicion_por_color_esquina(self.cubo,
                                                            self.piecita_cambiada)
                i,j   = pieza.fila, pieza.columna
                ia,ja = pieza.adyacente.fila, pieza.adyacente.columna
                ip,jp = pieza.precedente.fila, pieza.precedente.columna
                cara0, cara1, cara2 = pieza.cara, pieza.adyacente.cara, pieza.precedente.cara
                c0 = cube_state[cara0][i][j]
                c1 = cube_state[cara1][ia][ja]
                c2 = cube_state[cara2][ip][jp]
                    
                if self.sentido == 1: # ha girado a la izquierda
                    cube_state[cara0][i][j] = c2
                    cube_state[cara1][ia][ja] = c0
                    cube_state[cara2][ip][jp] = c1
                    orb.flippear_esquina(self.cubo, (i,j), self.sentido)
                    
                elif self.sentido == 2: # ha girado a la derecha
                    cube_state[cara0][i][j] = c1
                    cube_state[cara1][ia][ja] = c2
                    cube_state[cara2][ip][jp] = c0
                    orb.flippear_esquina(self.cubo, (i,j), self.sentido)

            if pieza:
                asignar_color_deuna(self.cubo)
                self.cube3DView.update()
                self.parent().parent().get_cubenet().drawNet()

            self.flip_shown = True
            self.updateStep()
            return

        # ------------------------------------------------
        # 1) Pasos canónicos: aplicar uno por uno
        # ------------------------------------------------
        if self.current_step < len(self.secuencia_movimientos):
            num_mov = self.historial[self.current_step]
            mov = grafo.nodos[num_mov].movimiento
            # 2.1) Aplica el giro al cube_state (estado canónico)
            traducir_a_cubo(mov, cube_state)
            # 2.2) Repinta el modelo molecular
            asignar_color_deuna(self.cubo)
            # 2.3) Actualiza vistas
            self.cube3DView.update()
            self.parent().parent().get_cubenet().drawNet()
            # 2.4) Avanza contador y refresca texto
            self.current_step += 1
            self.updateStep()
            return
        else:
            # Ya no hay más movimientos
            self.updateStep()
            
        # --- 3) Flip final (devuelve la pieza a la mala órbita) ---
        if self.flip_shown and not self.flip_end_shown and self.current_step >= len(self.secuencia_movimientos):
            orb = Orbitas(self.movimiento_origen)

            # Si es arista (2 colores)
            if isinstance(self.piecita_cambiada, (list, tuple)) and len(self.piecita_cambiada) == 2:
                pieza = orb.buscar_posicion_por_color_arista(self.cubo, self.piecita_cambiada)
                if pieza:
                    i,j = pieza.fila, pieza.columna
                    cs1 = cube_state[pieza.cara]
                    cs2 = cube_state[pieza.adyacente.cara]
                    ia,ja = pieza.adyacente.fila, pieza.adyacente.columna
                    cs1[i][j], cs2[ia][ja] = cs2[ia][ja], cs1[i][j]
                    orb.flippear_arista(self.cubo, (i,j))

            # Si es esquina (3 colores)
            else:
                pieza = orb.buscar_posicion_por_color_esquina(self.cubo, self.piecita_cambiada)
                if pieza:
                    i,j   = pieza.fila, pieza.columna
                    ia,ja = pieza.adyacente.fila, pieza.adyacente.columna
                    ip,jp = pieza.precedente.fila, pieza.precedente.columna
                    cara0, cara1, cara2 = pieza.cara, pieza.adyacente.cara, pieza.precedente.cara
                    c0 = cube_state[cara0][i][j]
                    c1 = cube_state[cara1][ia][ja]
                    c2 = cube_state[cara2][ip][jp]
                        
                    if self.sentido == 1: # ha girado a la izquierda, para volver tengo que girar a la derecha
                        cube_state[cara0][i][j] = c1
                        cube_state[cara1][ia][ja] = c2
                        cube_state[cara2][ip][jp] = c0
                        orb.restaurar_esquina(self.cubo, (i,j), self.sentido)
                        
                    elif self.sentido == 2: # ha girado a la derecha, para volver tengo que girar a la izquierda
                        cube_state[cara0][i][j] = c2
                        cube_state[cara1][ia][ja] = c0
                        cube_state[cara2][ip][jp] = c1
                        orb.restaurar_esquina(self.cubo, (i,j), self.sentido)
                        

            asignar_color_deuna(self.cubo)
            self.cube3DView.update()
            self.parent().parent().get_cubenet().drawNet()

            self.flip_end_shown = True
            self.updateStep()
            return

    def volverMenu(self):
        parent = self.parent()
        while parent is not None and not isinstance(parent, MainContainer):
            parent = parent.parent()
        if parent is not None:
            parent.stacked.setCurrentIndex(0)  

    def toggleView(self):
        if self.showingFullCube:
            # Volver a la vista dividida
            self.leftPanel.show()
            self.toggleViewBtn.setText("<<")
            self.mainLayout.insertWidget(0, self.leftPanel)
            self.mainLayout.insertWidget(1, self.middleWidget)
        else:
            # Ocultar panel izquierdo, mover botón al borde
            self.leftPanel.hide()
            self.toggleViewBtn.setText(">>")
            self.mainLayout.removeWidget(self.leftPanel)
            self.mainLayout.removeWidget(self.middleWidget)
            self.mainLayout.insertWidget(0, self.middleWidget)
        self.showingFullCube = not self.showingFullCube


# ---------------------------
# Integración en la interfaz
# ---------------------------
class MainWidget(QWidget):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.setWindowTitle(t('welcome', self.lang))  

        layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.cubo = iniciar()

        # Vistas 3D y Net
        self.cube3D  = RubiksCube3D()
        self.cubeNet = RubiksCubeNet(cube3d=self.cube3D)
        self.stacked.addWidget(self.cube3D)
        self.stacked.addWidget(self.cubeNet)
        layout.addWidget(self.stacked)

        # Label de mensajes temporales
        self.messageLabel = QLabel("")
        self.messageLabel.setStyleSheet(
            "background-color: #ff3333; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        self.messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.messageLabel)
        self.messageLabel.hide()

        # Botones inferiores
        btnLayout = QHBoxLayout()
        self.solucionarBtn = QPushButton()
        self.solucionarBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.solucionarBtn.clicked.connect(self.solucionar)

        self.toggleBtn = QPushButton()
        self.toggleBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.toggleBtn.clicked.connect(self.toggleView)

        self.reiniciarBtn = QPushButton()
        self.reiniciarBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.reiniciarBtn.clicked.connect(self.reiniciarCubo)

        self.shuffleBtn = QPushButton()
        self.shuffleBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.shuffleBtn.clicked.connect(self.mezclarCubo)

        for btn in (self.solucionarBtn, self.toggleBtn, self.reiniciarBtn, self.shuffleBtn):
            btnLayout.addWidget(btn)
        layout.addLayout(btnLayout)

        # finalmente, ponemos los textos
        self.retranslate()
        
    def retranslate(self):
        # Actualiza textos según el idioma actual
        self.setWindowTitle(t('welcome', self.lang))
        self.solucionarBtn.setText(t('solve_cube', self.lang))
        self.toggleBtn.setText(t('toggle_view', self.lang))
        self.reiniciarBtn.setText(t('reset_cube', self.lang))
        self.shuffleBtn.setText(t('shuffle_cube', self.lang))

    
    def get_cubenet(self):
        return self.cubeNet
    
    def mezclarCubo(self):
        """Selecciona un nodo aleatorio del grafo y aplica los movimientos al cubo."""
        try:
            # Obtener un nodo aleatorio del grafo
            numnodo_aleatorio = random.choice(list(grafo.nodos.values()))
            mov = numnodo_aleatorio.movimiento
            traducir_a_cubo(mov, cube_state)
            asignar_color_deuna(self.cubo)

            # Actualizar la vista net
            self.cubeNet.drawNet()
            self.mostrarMensaje(t('cube_shuffled', self.lang))
            
        except Exception as e:
            self.mostrarMensaje(t('not_found', self.lang))
            print("Error al mezclar el cubo:", e)
            
    def cubo_solucionado(self):
        # Recorremos cada cara y comprobamos que todas las casillas sean iguales a la letra de la cara.
        for cara, matriz in cube_state.items():
            for fila in matriz:
                for color in fila:
                    if color != cara:
                        return False
        return True
    
    def reiniciarCubo(self):
        
        if self.cubo_solucionado():
            self.mostrarMensaje(t('already_solved', self.lang))
            return cube_state, self.cubo
        
        current_index = self.stacked.currentIndex() 
        
        # Reiniciar el cubo a su estado inicial
        for cara in cube_state:
            for i in range(3):
                for j in range(3):
                    cube_state[cara][i][j] = cara
        
        self.cubo = iniciar()
        self.cubeNet.drawNet()
        self.cube3D.update()
        
        self.stacked.setCurrentIndex(current_index) 

        self.mostrarMensaje(t('cube_reset', self.lang))
        return cube_state, self.cubo

    def toggleView(self):
        current = self.stacked.currentIndex()
        self.stacked.setCurrentIndex(1 - current)
        self.cubeNet.drawNet()
        self.cube3D.update()
    
    def mostrarMensaje(self, texto):
        self.messageLabel.setText(texto)
        self.messageLabel.show()
        QTimer.singleShot(3000, self.messageLabel.hide)
        
    '''def openSolutionWindow(self, secuencia, historial, piecita_cambiada, movimiento_origen):
        """Crea una ventana independiente con un SolutionWidget."""
        sw = SolutionWidget(
            secuencia_movimientos=secuencia,
            historial=historial,
            piecita_cambiada=piecita_cambiada,
            cubo_modelo=self.cubo,
            movimiento_origen=movimiento_origen
        )
        win = QMainWindow(self)
        win.setWindowTitle("Solución alternativa")
        win.setCentralWidget(sw)
        win.resize(800, 600)
        win.show()'''

    def solucionar(self):
        # 1) Comprobamos que el cubo no está ya resuelto
        if self.cubo_solucionado():
            self.mostrarMensaje(t('already_solved', self.lang))
            return None

        try:
            # 2) Verificar que hay exactamente 9 casillas de cada color
            counts = {}
            for face in cube_state:
                for row in cube_state[face]:
                    for color in row:
                        counts[color] = counts.get(color, 0) + 1
            for color, count in counts.items():
                if count != 9:
                    raise ValueError(t('only_9', self.lang))

            # 3) Sincronizar colores al modelo molecular y traducimos a movimiento
            asignar_color_deuna(self.cubo)
            movimiento = traducir_a_mov(self.cubo)

            # 4) Comprobamos las restricciones del cubo
            orb = Orbitas(movimiento)
            restriccion_mod2 = orb.comprobar_restriccion_mod2()
            restriccion_mod3 = orb.comprobar_restriccion_mod3()
            restriccion_perm = orb.comprobar_restriccion_perm()
            if not restriccion_mod2 or not restriccion_mod3 or not restriccion_perm:
                
                # --- Caso “otra órbita” ---
                self.mostrarMensaje(t('not_found', self.lang))
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Icon.Warning)
                msgBox.setWindowTitle("Movimiento no encontrado")
                msgBox.setText(t('not_found', self.lang))
                msgBox.setInformativeText(t('question_orbit', self.lang))
                aceptar = msgBox.addButton(t('continue_orbit', self.lang), QMessageBox.ButtonRole.AcceptRole)
                corregir = msgBox.addButton(t('correct_cube', self.lang),    QMessageBox.ButtonRole.RejectRole)
                msgBox.setDefaultButton(corregir)
                msgBox.exec()
                
                if msgBox.clickedButton() == aceptar:
                    nuevo_movimiento = movimiento.copy()
                    piezas_cambiadas = []
                    piezas_transmutadas = []
                    sentido = None
                    
                    if not restriccion_mod2:
                        orient2_buenas = orb.opciones_mod2_correcto()
                        orient2_elegida = random.choice(orient2_buenas)
                        nuevo_movimiento[1] = orient2_elegida
                        
                        color2 = orb.buscar_color_por_posicion_arista(orient2_elegida, self.cubo)
                        piezas_cambiadas.append(color2)
                        
                    if not restriccion_mod3:
                        orient3_buenas = orb.opciones_mod3_correcto()
                        orient3_elegida = random.choice(orient3_buenas)
                        nuevo_movimiento[3] = orient3_elegida
                        
                        # definimos el sentido de giro
                        for i in range(len(orient3_elegida)):
                            if movimiento[3][i] != orient3_elegida[i]:
                                indice_distinto = i
                        orient_original = movimiento[3][indice_distinto]
                        orient_nueva = orient3_elegida[indice_distinto]
                        cuanto_gira = (orient_nueva - orient_original) % 3
                        if cuanto_gira == 1:
                            sentido = 1
                        elif cuanto_gira == 2:
                            sentido = 2
                        else:
                            sentido = None
                        
                        color3 = orb.buscar_color_por_posicion_esquina(orient3_elegida, self.cubo)
                        piezas_cambiadas.append(color3)
                              
                    if not restriccion_perm:
                        # elegimos si permutar dos aristas o dos esquinas
                        eleccion = random.choice([0, 2])
                        nueva_perm = orb.cambiar_paridad(eleccion)
                        nuevo_movimiento[eleccion] = nueva_perm
                        # CONTINUAR PR AQUI, HAY QUE DEFINIR EN LA MATRIZ CUBO QUE DOS PIEZAS SE INTERCAMBIAN
                        
                    
                    self.mostrarMensaje(t('random_solution', self.lang))
                    secuencia, historial = buscar_identidad(buscar_nodo(nuevo_movimiento))
                    self.solutionWidget = SolutionWidget(
                        secuencia_movimientos=secuencia,
                        historial=historial,
                        
                    
                    
                    
                        
                            
            
            
                
class MainMenuWidget(QWidget):
    def __init__(self, lang, main_container):
        super().__init__()
        self.lang = lang
        self.main_container = main_container
        self.buildUI()
        self.retranslate()
        
    def buildUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addStretch(2)

        self.titulo = QLabel()
        self.titulo.setObjectName("titleLabel")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setFixedHeight(60)
        layout.addWidget(self.titulo)
        layout.addStretch(1) 
        
        self.subtitulo = QLabel()
        self.subtitulo.setObjectName("subtitleLabel")
        self.subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitulo)
        
        layout.addStretch(1) # espacio bonito
        
        # Botones del menú
        self.startBtn = QPushButton()
        self.startBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.startBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.languageBtn = QPushButton()
        self.languageBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.languageBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.aboutBtn = QPushButton()
        self.aboutBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.aboutBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.exitBtn = QPushButton()
        self.exitBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.exitBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(2)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(15)
        grid.addWidget(self.startBtn,   0, 0)
        grid.addWidget(self.languageBtn,0, 1)
        grid.addWidget(self.aboutBtn,   1, 0)
        grid.addWidget(self.exitBtn,    1, 1)
        layout.addLayout(grid)

        layout.addStretch(3)
        
        # Conexiones
        self.languageBtn.clicked.connect(self.cambiar_idioma)
        self.aboutBtn.clicked.connect(self.acercaDe)
        self.exitBtn.clicked.connect(QApplication.instance().quit)

        
        # Definir un estilo global para el menú
        self.setStyleSheet("""
            QWidget {
                background-color: #C4D7F2;  
                border-radius: 15px;
                padding: 10px;
            }
            QLabel#titleLabel {
                background-color: #F48FB1;  
                color: white;
                font-size: 32px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                background-color: #B8F58E;
                color: #55917F;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border: none;
                border-radius: 10px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #9bf15f;
            }
            QInputDialog QComboBox {
                background-color: white;
            }
            QInputDialog QListView {
                background-color: white;
            }
        """)
    def retranslate(self):
        # Títulos
        self.titulo.setText(t('welcome', self.lang))
        self.subtitulo.setText(t('press_start', self.lang) )
        # Botones del menú
        self.startBtn.setText(t('start', self.lang) )
        self.languageBtn.setText(t('language', self.lang) )
        self.aboutBtn.setText(t('about', self.lang) )
        self.exitBtn.setText(t('exit', self.lang) )

        
    def cambiar_idioma(self):
        # Lista de opciones traducidas
        labels = [
            ("Español", "es"),
            ("English", "en"),
            ("Italiano", "it"),
            ("Deutsch", "de"),
            ("Français", "fr")
        ]
        display = [l[0] for l in labels]
        elegido, ok = QInputDialog.getItem(
            self,
            t('select_lenguage', self.lang),
            t('language',        self.lang),
            display, 0, False
        )
        if ok:
            new_lang = dict(labels)[elegido]
            self.main_container.changeLanguage(new_lang)
            self.retranslate()
            self.update()    
            QApplication.processEvents()

    def acercaDe(self):
        QMessageBox.about(
            self,
            t('about', self.lang),
            t('about_text', self.lang))


class MainContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stacked = QStackedWidget()
        self.lang = 'es'  # Idioma por defecto

        self.menuWidget = MainMenuWidget(self.lang, self)
        self.cubeWidget = MainWidget(self.lang)  # Creamos una primera instancia
        
        self.stacked.addWidget(self.menuWidget)
        self.stacked.addWidget(self.cubeWidget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked)

        # Conecta el botón de "Comenzar"
        self.menuWidget.startBtn.clicked.connect(self.startNewSession)

    def startNewSession(self):
        
        # Asegúrate de que el cubo esté en su estado inicial
        for cara in cube_state:
            for i in range(3):
                for j in range(3):
                    cube_state[cara][i][j] = cara
        
        new_cubo = MainWidget(self.lang)  
        self.stacked.addWidget(new_cubo)  
        self.stacked.setCurrentWidget(new_cubo)
        old = getattr(self, 'cubeWidget', None)
        self.cubeWidget = new_cubo  
    
    def changeLanguage(self, new_lang):
        self.lang = new_lang
        # retranslate en ambos widgets
        self.menuWidget.lang = new_lang
        self.menuWidget.retranslate()
        self.cubeWidget.lang = new_lang
        self.cubeWidget.retranslate()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainContainer = MainContainer()
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self.mainContainer)
    
    def get_mainwidget(self):
        return self.mainWidget
    
    def keyPressEvent(self, event):
        event.ignore()
        
def run_app():
    cubo = iniciar()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

