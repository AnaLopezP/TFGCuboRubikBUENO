from cubo import Molecula, Vertice, Arista

class Orbitas:
    def __init__(self, movimiento):
        self.movimiento = movimiento
        self.orientaciones_mod2 = movimiento[1]
        self.orientaciones_mod3 = movimiento[3]
        self.perm1 = movimiento[0]
        self.perm2 = movimiento[2]

    def comprobar_restriccion_mod2(self):
        if sum(self.orientaciones_mod2) % 2 != 0:
            # no está en la órbita debido a una arista
            return False
        else:
            return True

    def opciones_mod2_correcto(self):
        if self.comprobar_restriccion_mod2() == False:
            # cambio un numero de la lista cada vez y devuelve las 4 opciones
            opciones = []
            for i in range(len(self.orientaciones_mod2)):
                if self.orientaciones_mod2[i] == 0:
                    nuevo = self.orientaciones_mod2.copy()
                    nuevo[i] = 1
                    opciones.append(nuevo)
                else:
                    nuevo = self.orientaciones_mod2.copy()
                    nuevo[i] = 0
                    opciones.append(nuevo)
            return opciones
        else:
            return False

    def movimientos_opciones(self):
        mov_opciones = []
        orientaciones = self.opciones_mod2_correcto()
        for i in range(len(orientaciones)):
            self.movimiento[1] = orientaciones[i]
            mov_opciones.append(self.movimiento.copy())            

        return mov_opciones
    
    def buscar_posicion_por_color_arista(self, cubo, colores):
        # buscamos un par de colores en el cubo
        if (cubo[0][1].color == colores[0] and cubo[0][1].adyacente.color == colores[1]) or (cubo[0][1].color == colores[1] and cubo[0][1].adyacente.color == colores[0]):
            return cubo[0][1]
        elif (cubo[1][0].color == colores[0] and cubo[1][0].adyacente.color == colores[1]) or (cubo[1][0].color == colores[1] and cubo[1][0].adyacente.color == colores[0]): 
            return cubo[1][0]
        elif (cubo[1][2].color == colores[0] and cubo[1][2].adyacente.color == colores[1]) or (cubo[1][2].color == colores[1] and cubo[1][2].adyacente.color == colores[0]):
            return cubo[1][2]
        elif (cubo[2][1].color == colores[0] and cubo[2][1].adyacente.color == colores[1]) or (cubo[2][1].color == colores[1] and cubo[2][1].adyacente.color == colores[0]):
            return cubo[2][1]
        else:
            print("No se ha encontrado la arista")
            return None
        
    def buscar_color_por_posicion_arista(self, orientacion_nueva, cubo):
        for i in range(len(self.orientaciones_mod2)):
            if self.orientaciones_mod2[i] != orientacion_nueva[i]:
                if i == 0:
                    return [cubo[0][1].color, cubo[0][1].adyacente.color]
                elif i == 1:
                    return [cubo[1][0].color, cubo[1][0].adyacente.color]
                elif i == 2:
                    return [cubo[1][2].color, cubo[1][2].adyacente.color]
                elif i == 3:
                    return [cubo[2][1].color, cubo[2][1].adyacente.color]
            else:
                print("No hay ninguna diferencia entre las orientaciones")
                
    def flippear_arista(self, cubo, posicion):
        """
        Dado el cubo (la matriz 3x3) y la posición (i,j) de la arista a voltear,
        intercambia los colores de la pieza y su adyacente.
        """
        i, j = posicion
        pieza = cubo[i][j]
        c1 = pieza.color
        c2 = pieza.adyacente.color
        pieza.color = c2
        pieza.adyacente.color = c1
        return cubo
    
    # Esquinas: comprobación suma mod-3
    def comprobar_restriccion_mod3(self):
        return sum(self.orientaciones_mod3) % 3 == 0

    # Generar las 4 opciones cambiando UNA esquina a cada valor distinto
    def opciones_mod3_correcto(self):
        opciones = []
        for i in range(len(self.orientaciones_mod3)):
            for nuevo in (0, 1, 2):
                if self.orientaciones_mod3[i] != nuevo:
                    candidata = self.orientaciones_mod3.copy()
                    candidata[i] = nuevo
                    # sólo la añadimos si la suma sigue siendo 0 mod 3
                    if sum(candidata) % 3 == 0:
                        opciones.append(candidata)
        return opciones

    def movimientos_opciones_esquinas(self):
        movs = []
        for ori_mod3 in self.opciones_mod3_correcto():
            mov = self.movimiento.copy()
            mov[3] = ori_mod3
            movs.append(mov)
        return movs

    # Busca vértice por colores
    def buscar_posicion_por_color_esquina(self, cubo, colores3):
        # recorre tus 4 vértices y devuelve el vertice cuya tupla de 3 colores
        # coincida, independiente del orden.
        for coords in [(0,0),(0,2),(2,2),(2,0)]:
            pieza = cubo[coords[0]][coords[1]]
            tri = [pieza.color,
                   pieza.adyacente.color,
                   pieza.precedente.color]
            if set(tri) == set(colores3):
                return pieza
        return None
    
    def buscar_color_por_posicion_esquina(self, orientacion_nueva, cubo):
        for i in range(len(self.orientaciones_mod3)):
            if self.orientaciones_mod3[i] != orientacion_nueva[i]:
                if i == 0:
                    return [cubo[0][0].color, cubo[0][0].adyacente.color, cubo[0][0].precedente.color]
                elif i == 1:
                    return [cubo[0][2].color, cubo[0][2].adyacente.color, cubo[0][2].precedente.color]
                elif i == 2:
                    return [cubo[2][2].color, cubo[2][2].adyacente.color, cubo[2][2].precedente.color]
                elif i == 3:
                    return [cubo[2][0].color, cubo[2][0].adyacente.color, cubo[2][0].precedente.color]
            else:
                print("No hay ninguna diferencia entre las orientaciones")

    def flippear_esquina(self, cubo, posicion, sentido):
        """
        Las esquinas se pueden girar en dos sentidos (1 o 2).
        """
        v = cubo[posicion[0]][posicion[1]]
        c0, c1, c2 = v.color, v.adyacente.color, v.precedente.color

        if sentido == 1:
            # rotación +1
            v.color, v.adyacente.color, v.precedente.color = c2, c0, c1
        elif sentido == 2:
            # rotación −1 (equivalente a dos rotaciones +1)
            v.color, v.adyacente.color, v.precedente.color = c1, c2, c0
        else:
            raise ValueError("sentido debe ser 1 o 2")
        return cubo

    def restaurar_esquina(self, cubo, posicion, sentido=1):
        """
        Devolvemos la esquina a su posicion original 
        giramos en el sentido contrario al que se giró
        """
        # sólo llamamos de nuevo a flippear con el sentido inverso
        inverso = 2 if sentido == 1 else 1
        return self.flippear_esquina(cubo, posicion, sentido=inverso)
    
    def transposiciones(self, perm):
        num_transposiciones = 0
        for i in range(len(perm)):
            if perm[i] > perm[i + 1]:
                print(f"Transposición entre {perm[i]} y {perm[i + 1]}")
                num_transposiciones += 1
        return num_transposiciones
    
    def comprobar_restriccion_perm(self):
        ''' Para que se cumple la restricción de permutación, ambas tienen que ser pares o impares.
            Una manera de comprobarlo es que, en los valores de cada diccionario, el número de números que estén descolocaos sea par o impar.
            Los números descolocados son aquellos que son más grandes que su siguiente valor
            Ejemplo, {1: 2, 2:4, 3:3, 4:1}, 2 es más grande que 1, 4 es más grande que 3 y 1, 3 es más grande que 1, eso suman 4 transposiciones, por lo tanto es par.'''
        
        transposiciones1 = self.transposiciones(self.perm1)
        transposiciones2 = self.transposiciones(self.perm2)
        signo = (transposiciones1 + transposiciones2) % 2
        if signo == 0:
            print("Restricción de permutación cumplida. Es par")
            return True
        else:
            return False
        
    def intercambiar_aristas(self, cubo, colores1, colores2):
        """
        Intercambia dos aristas en el cubo.
        Busca las aristas por colores y las intercambia.
        """
        posicion1 = self.buscar_posicion_por_color_arista(cubo, colores1)
        posicion2 = self.buscar_posicion_por_color_arista(cubo, colores2)
        
        if posicion1 and posicion2:
            # Intercambiamos los colores de las aristas
            c1 = posicion1.color
            c2 = posicion1.adyacente.color
            posicion1.color = posicion2.color
            posicion1.adyacente.color = posicion2.adyacente.color
            posicion2.color = c1
            posicion2.adyacente.color = c2
            return cubo
        else:
            print("No se han encontrado las aristas a intercambiar")
            return None
        
    def intercambiar_esquinas(self, cubo, colores1, colores2):
        """
        Intercambia dos esquinas en el cubo.
        Busca las esquinas por colores y las intercambia.
        """
        posicion1 = self.buscar_posicion_por_color_esquina(cubo, colores1)
        posicion2 = self.buscar_posicion_por_color_esquina(cubo, colores2)
        
        if posicion1 and posicion2:
            # Intercambiamos los colores de las esquinas
            c1 = posicion1.color
            c2 = posicion1.adyacente.color
            c3 = posicion1.precedente.color
            
            posicion1.color = posicion2.color
            posicion1.adyacente.color = posicion2.adyacente.color
            posicion1.precedente.color = posicion2.precedente.color
            
            posicion2.color = c1
            posicion2.adyacente.color = c2
            posicion2.precedente.color = c3
            
            return cubo
        else:
            print("No se han encontrado las esquinas a intercambiar")
            return None
        
    def cambiar_paridad(self, eleccion):
        # coje una de las permutaciones e intercambia dos valores de la permutación para cambiar la paridad
        if eleccion == 0:
            # intercambiamos los dos primeros valores de la permutación 1
            self.perm1[0], self.perm1[1] = self.perm1[1], self.perm1[0]
            return self.perm1
        elif eleccion == 2:
            # intercambiamos los dos primeros valores de la permutación 2
            self.perm2[0], self.perm2[1] = self.perm2[1], self.perm2[0]
            return self.perm2
        else:
            print("Elección no válida. Debe ser 1 o 2.")
        