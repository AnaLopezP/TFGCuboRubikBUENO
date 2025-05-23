import csv
from tqdm import tqdm
from collections import deque

csv.field_size_limit(1000000000)

class LeyGrupo():
    def __init__(self, movimiento, nombre):
        self.movimiento = movimiento
        self.nombre = nombre
    
    def generar_movimiento(self):
        ciclo_alpha = self.crear_ciclo()
        pos_a = self.crear_posicion_arista()
        ciclo_beta = self.crear_ciclo()
        pos_b = self.crear_posicion_verice()
        self.movimiento = [ciclo_alpha, pos_a, ciclo_beta, pos_b]
        self.nombre = input("Ingrese el nombre (los giros) del movimiento: ")
        if not self.comprobar_restricciones(self.movimiento):
            print("Error: No se cumplieron las restricciones.")
            return None
        return self.movimiento
    '''Esta funcion genera un movimiento a partir de dos ciclos y dos posiciones'''
    
    def crear_ciclo(self):
        #ciclo = []
        uno = int(input("¿A qué posición va la posición 1? "))
        dos = int(input("¿A qué posición va la posición 2? "))
        tres = int(input("¿A qué posición va la posición 3? "))
        cuatro = int(input("¿A qué posición va la posición 4? "))
        ciclo = {1: uno, 2: dos, 3: tres, 4: cuatro}
        return ciclo
    
    def crear_posicion_arista(self):
        pos = []
        for i in range(4):
            color = int(input("Ingrese 0 o 1: "))
            if color != 0 and color != 1:
                print("Error: Ingrese 0 o 1")
                return None
            pos.append(color)
            i += 1
        return pos
    '''Esta funcion indica si el color de la arista está en su lugar (0) o no (1)'''

    def crear_posicion_verice(self):
        pos = []
        for i in range(4):
            color = int(input("Ingrese 0, 1 o 2: "))
            if color != 0 and color != 1 and color != 2:
                print("Error: Ingrese 0, 1, o 2")
                break
            pos.append(color)
            i += 1
        return pos
    '''Esta funcion indica si el color del vertice está en su lugar (0), si está girado 1/3 a la izquierda (1) o 2/3 a la izquierda (2), mirándolo desde la esquina'''
    
    def guardar_en_csv(self, archivo_csv):
        """Guarda el movimiento actual en un archivo CSV"""
        if self.movimiento and self.nombre:
            with open(archivo_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.nombre, self.movimiento])
            print(f"Movimiento {self.nombre} guardado en {archivo_csv}")
        else:
            print("No hay movimiento generado para guardar.")


    def __str__(self):
        return f"El movimiento {self.nombre} es: {self.movimiento}"
    
    def componer_movimientos(self, m1, m2):
        nuevo_mov = []
        nuevo_mov.append(self.componer_ciclos(m1[0], m2[0]))
        nuevo_mov.append(self.componer_posiciones_mod2(m1[1], m2[1], m2[0]))
        nuevo_mov.append(self.componer_ciclos(m1[2], m2[2]))
        nuevo_mov.append(self.componer_posiciones_mod3(m1[3], m2[3], m2[2]))
        return nuevo_mov
        
    def componer_ciclos(self, c1, c2):
        nuevo_ciclo = {}
        for i in range(len(c1)):
            valor = c1[i+1]
            valor2 = c2[valor]
            nuevo_ciclo[i+1] = valor2
        return nuevo_ciclo
    
    def calcular_ciclo_inverso(self, c2):
        ciclo_inverso = {j: i for i, j in c2.items()}  # Generar inversa
        return dict(sorted(ciclo_inverso.items()))  # Ordenarlo
    
    def componer_posiciones_mod2(self, p1, p2, c2):
        ciclo_inverso = self.calcular_ciclo_inverso(c2)

        pos = [0] * 4
        for k in range(4):
            x = ciclo_inverso[k+1]
            pos[k] = p1[x-1]

        nueva_pos = [(pos[i] + p2[i]) % 2 for i in range(4)]
        return nueva_pos

    def componer_posiciones_mod3(self, p1, p2, c2):
        ciclo_inverso = self.calcular_ciclo_inverso(c2)

        pos = [0] * 4
        for k in range(4):
            x = ciclo_inverso[k+1]
            pos[k] = p1[x-1]

        nueva_pos = [(pos[i] + p2[i]) % 3 for i in range(4)]
        return nueva_pos
    
    def comprobar_restricciones(self, m1):
        # primero comprobamos que el sumatorio de las posiciones de las aristas sea cero
        if sum(m1[1]) % 2 != 0:
            return False
        # luego comprobamos que el sumatorio de las posiciones de los vertices sea cero
        if sum(m1[3]) % 3 != 0:
            return False
        
    def comparar_movimientos(self, m1, m2):
        if m1 == m2:
            return True
        else:
            return False


# creamos un csv con los movimientos base de datos (son 34) solo si no existe
# Este codigo solo se ejecuta una vez, para crear el csv
def crear_csv():
    while True:
        print("-------------------- GENERANDO MOVIMIENTO --------------------")
        mov = LeyGrupo([], "")
        mov.generar_movimiento()
        mov.guardar_en_csv("movimientos.csv")
        
        continuar = input("¿Desea continuar? (s/n): ").strip().lower()
        if continuar != "s":
            break
        

# creamos una clase Nodo para almacenar los movimientos
class Nodo():
    def __init__(self, numero, nombre, movimiento):
        self.numero = numero
        self.nombre = nombre
        self.movimiento = movimiento
        self.adyacentes = []
    
    def agregar_adyacente(self, nodo, posicion):
        # Asegurarse de que no se agregue el propio nodo ni duplicados. ponemos el nodo adyacente en la posicion del movimiento aplicado para llegar a él
        if nodo != self and nodo not in self.adyacentes:
            self.adyacentes.insert(posicion, nodo)
            
    def __str__(self):
        return f"El movimiento es: {self.movimiento}"    

# creamos un grafo con los movimientos del csv
class Grafo():
    def __init__(self):
        self.nodos = {} # diccionario {numero del nodo: nodo}
        self.ley = LeyGrupo([], "")
    
    def agregar_nodo(self, numero, nombre, movimiento):
        if numero not in self.nodos:
            self.nodos[numero] = Nodo(numero, nombre, movimiento)
        else:
            print("Ya existe un nodo con ese número.")
    
    def agregar_arista(self, nodo1, nodo2, posicion):
        # añadir una arista que vaya del nodo 1 al nodo 2 en la posicion del movimiento aplicado para llegar al nodo2
        # evitamos crear una arista con el mismo nodo
        if nodo1 != nodo2:
            if nodo1 in self.nodos and nodo2 in self.nodos:
                self.nodos[nodo1].agregar_adyacente(self.nodos[nodo2], posicion)            
    
    def mostrar_grafo(self):
        for num, nodo in self.nodos.items():
            print(f"Nodo {num} ({nodo.movimiento}): {[n.numero for n in nodo.adyacentes]}")           
   
    def combinar_grafo(self, nodos_fuente, nodos_destino, grafo_destino):
        """
        Combina los movimientos de dos grupos de nodos y guarda los nuevos en dos grafos, uno con toda la informacion y otro solo con la nueva
        """
        lg = LeyGrupo([], "")
        iteraciones = 0

        print(f"Combinando {len(nodos_fuente)} con {len(nodos_destino)} en un grafo aparte")
        
        # ponemos los nodos destino en el grafo destino
        for nodo in nodos_destino:
            grafo_destino.agregar_nodo(nodo.numero, nodo.nombre, nodo.movimiento)

        with tqdm(total=len(nodos_fuente) * len(nodos_destino), desc="Combinando", unit="iter") as pbar:
            for nodo1 in nodos_fuente:
                for nodo2 in nodos_destino:
                    nuevo_mov = lg.componer_movimientos(nodo1.movimiento, nodo2.movimiento)

                    # Verificar si ya existe en el grafo destino
                    nodo_existente = next(
                        (n for n in grafo_destino.nodos.values() if lg.comparar_movimientos(nuevo_mov, n.movimiento)), 
                        None
                    )

                    if nodo_existente is None:
                        # Si no existe, crear un nuevo nodo en el grafo destino
                        nuevo_num = max(grafo_destino.nodos.keys(), default=-1) + 1
                        grafo_destino.agregar_nodo(nuevo_num, f"Nodo {nuevo_num}", nuevo_mov)
                        
                        # Conectar con el nodo de origen (nodo2) en el grafo destino
                        grafo_destino.agregar_arista(nodo1.numero, nuevo_num, nodo2.numero)
                    else:
                        # Si ya existe, solo añadir aristas
                        grafo_destino.agregar_arista(nodo1.numero, nodo_existente.numero, nodo2.numero)

                    iteraciones += 1
                    pbar.update(1)

        print(f"{len(grafo_destino.nodos)} movimientos almacenados en el grafo auxiliar")

    
    def guardar_grafo_csv(self, archivo_csv):
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Numero', 'Nombre', 'Movimiento', 'Adyacentes'])
            
            for nodo in self.nodos.values():
                writer.writerow([nodo.numero, nodo.nombre, nodo.movimiento, [n.numero for n in nodo.adyacentes]])
            print(f"Grafo guardado en {archivo_csv}")


def cargar_grafo_de_csv(archivo_csv):
    grafo = Grafo()
    conexiones = {} # guardamos las conexiones temporalmente para añadirlas después
    
    with open(archivo_csv, newline='', mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)
        # Se salta la cabecera
        next(reader)

        # Crear los nodos
        for row in reader:
            numero = int(row[0])
            nombre = row[1]
            movimiento = eval(row[2])  # Convertimos la cadena a su estructura original 
            adyacentes = eval(row[3])  # Esto es una lista de números de los nodos adyacentes
            
            grafo.agregar_nodo(numero, nombre, movimiento)
            conexiones[numero] = adyacentes # Guardamos las conexiones para después

        # crear las aristas
        for numero, adyacentes in conexiones.items():
            for i, adyacente in enumerate(adyacentes):
                grafo.agregar_arista(numero, adyacente, i)                
    
    return grafo


def cargar_movimientos_iniciales(archivo_csv):
    '''
    Cargamos los movimientos iniciales del archivo csv y los devolvemos en un diccionario.
    '''
    movimientos = {}
    with open(archivo_csv, newline='', mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            movimientos[i] = row[0]
    return movimientos

import sys, os

def resource_path(relative_path):
    """ Devuelve la ruta absoluta dentro del bundle de PyInstaller
        o la de tu carpeta normal si estás en desarrollo. """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# cargamos los movimientos iniciales
movimientos_iniciales = cargar_movimientos_iniciales(resource_path("movimientos.csv"))
# cargamos el grafo
grafo= cargar_grafo_de_csv(resource_path("grafo_final.csv"))

def buscar_nodo(movimiento):
    """
    Busca un nodo en el grafo que tenga el mismo movimiento que el proporcionado.
    """
    for nodo in grafo.nodos.values():
        if nodo.movimiento == movimiento:
            return nodo.numero
    return None
        
# ------------- CODIGO PARA CREAR EL GRAFO FINAL------------------
# Este código se ejecuta una vez para crear el grafo final
#cargo los movimientos del csv
'''grafo = Grafo()

# cargamos los movimientos iniciales del archivo csv en forma de grafo
with open("movimientos.csv",newline= "", mode='r', encoding="utf-8") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        nombre = row[0]
        movimiento = eval(row[1])
        grafo.agregar_nodo(i, nombre, movimiento)
        

grafo_combinado1 = Grafo()
grafo_combinado1.combinar_grafo(grafo.nodos.values(), grafo.nodos.values(), grafo_combinado1)
#grafo.mostrar_grafo()
#grafo_combinado1.mostrar_grafo()
grafo_combinado1.guardar_grafo_csv("grafo_combinado1.csv")
grafo.guardar_grafo_csv("grafo.csv")


#opero los nuevos nodos con los nodos del grafo primero
grafo_combinado2 = Grafo()
grafo_combinado2.combinar_grafo(grafo_combinado1.nodos.values(), grafo.nodos.values(), grafo_combinado2)
grafo_combinado2.guardar_grafo_csv("grafo_combinado2.csv")
#grafo_combinado2.mostrar_grafo()

#grafo_combinado3 = cargar_grafo_de_csv("grafo_combinado3.csv")

grafo_combinado3 = Grafo()
grafo_combinado3.combinar_grafo( grafo_combinado2.nodos.values(), grafo.nodos.values(), grafo_combinado3)
grafo_combinado3.guardar_grafo_csv("grafo_combinado3.csv")
grafo_combinado3.mostrar_grafo()

grafo_combinado4 = Grafo()
grafo_combinado4.combinar_grafo(grafo_combinado3.nodos.values(), grafo.nodos.values(), grafo_combinado4)
grafo_combinado4.guardar_grafo_csv("grafo_combinado4.csv")

grafo_final = Grafo()
grafo_final.combinar_grafo(grafo_combinado4.nodos.values(), grafo.nodos.values(), grafo_final)
grafo_final.guardar_grafo_csv("grafo_final.csv")'''


# Algoritmo de búsqueda en anchura para encontrar el camino más corto a la identidad

def buscar_identidad(nodo_inicial):
    ''' 
    Para cada nodo del grafo:
    - Si tiene conexión con la identidad (nodo 51), se añade a la lista de movimientos
    - Si no tiene conexión, elige el nodo con el numero más pequeño
    - Devuelve la lista de movimientos hasta llegar a la identidad
    '''
    movimiento_identidad = 51
    cola = deque()
    visitados = set()
    
    secuencia_movimientos = [] # guardamos los movimientos
    historial = [] # micky herramienta que usaremos más adelante (guarda los nodos visitados)
    cola.append(nodo_inicial)
    
    while cola:
        nodo_actual = cola.popleft()
        
        # Si ya lo visitamos, lo saltamos
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        # Lista para guardar los nodos adyacentes válidos
        nodos_adyacentes = grafo.nodos[nodo_actual].adyacentes
        
        # Buscar si el nodo 51 está en los adyacentes
        if any(nodo.numero == movimiento_identidad for nodo in nodos_adyacentes):
            for indice, nodo in enumerate(nodos_adyacentes):
                if nodo.numero == movimiento_identidad:
                    secuencia_movimientos.append(movimientos_iniciales.get(indice, f"Movimiento_{indice}"))
                    historial.append(movimiento_identidad)
                    return secuencia_movimientos, historial  # Terminamos porque llegamos a 51
        
        # Si no encontramos el 51, buscamos el nodo con el número más pequeño
        nodo_mas_pequeno = min(nodos_adyacentes, key=lambda nodo: nodo.numero, default=None)
        
        if nodo_mas_pequeno:
            # Obtenemos el índice del movimiento que lleva a este nodo
            for indice, nodo in enumerate(nodos_adyacentes):
                if nodo.numero == nodo_mas_pequeno.numero:
                    secuencia_movimientos.append(movimientos_iniciales.get(indice, f"Movimiento_{indice}"))
                    historial.append(nodo_mas_pequeno.numero)
                    cola.append(nodo_mas_pequeno.numero)
                    break  # Solo agregamos el primer camino encontrado
    
    return secuencia_movimientos, historial
