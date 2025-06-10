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
            print("Restricción de mod2 no cumplida")
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
        if sum(self.orientaciones_mod3) % 3 != 0:
            # no está en la órbita debido a una esquina
            print("Restricción de mod3 no cumplida")
            return False
        else:
            return True

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
        valores = [perm[k] for k in perm]
        num_transposiciones = 0
        n = len(valores)
        for i in range(n):
            for j in range(i + 1, n):
                if valores[i] > valores[j]:
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
        # Intercambio los colores blancos entre ellos y los colores que no son blancos entre ellos
        pieza1 = self.buscar_posicion_por_color_arista(cubo, colores1)
        pieza2 = self.buscar_posicion_por_color_arista(cubo, colores2)
        if not (pieza1 and pieza2):
            print("No se han encontrado las aristas a intercambiar")
            return None
        stiker1_pieza1 = pieza1.color
        stiker2_pieza1 = pieza1.adyacente.color
        stiker1_pieza2 = pieza2.color
        stiker2_pieza2 = pieza2.adyacente.color
        # Identifico que pieza es la blanca y que pieza es la de otro color
        if stiker1_pieza1 == "B":
            color_blanco1 = 'color'
            color_noblanco1 = 'adyacente'
            valor_blanco1 = stiker1_pieza1
            valor_noblanco1 = stiker2_pieza1
        elif stiker2_pieza1 == "B":
            color_blanco1 = 'adyacente'
            color_noblanco1 = 'color'
            valor_blanco1 = stiker2_pieza1
            valor_noblanco1 = stiker1_pieza1
        
        # Hacemos lo mismo en la otra pieza 
        if stiker1_pieza2 == "B":
            color_blanco2 = 'color'
            color_noblanco2 = 'adyacente'
            valor_blanco2 = stiker1_pieza2
            valor_noblanco2 = stiker2_pieza2
        elif stiker2_pieza2 == "B":
            color_blanco2 = 'adyacente'
            color_noblanco2 = 'color'
            valor_blanco2 = stiker2_pieza2
            valor_noblanco2 = stiker1_pieza2
            
        # Intercambiamos los colores blancos
        if color_blanco1 and color_blanco2:
            # guardo temporalmente el stiker blanco de la primera pieza
            temp_blanco = valor_blanco1
            if color_blanco1 == 'color':
                pieza1.color = valor_blanco2
            else:
                pieza1.adyacente.color = valor_blanco2
                
            if color_blanco2 == 'color':
                pieza2.color = temp_blanco
            else:
                pieza2.adyacente.color = temp_blanco
                
        # intercambiamos los colores que no son blancos
        if color_noblanco1 and color_noblanco2:
            # guardo temporalmente el stiker no blanco de la primera pieza
            temp_noblanco = valor_noblanco1
            if color_noblanco1 == 'color':
                pieza1.color = valor_noblanco2
            else:
                pieza1.adyacente.color = valor_noblanco2
                
            if color_noblanco2 == 'color':
                pieza2.color = temp_noblanco
            else:
                pieza2.adyacente.color = temp_noblanco
        return cubo
    
    def intercambiar_esquinas(self, cubo, colores1, colores2):
        """
        Intercambia dos esquinas en el modelo molecular,
        emparejando cada color de colores1 con el correspondiente de colores2.
        """
        pieza1 = self.buscar_posicion_por_color_esquina(cubo, colores1)
        pieza2 = self.buscar_posicion_por_color_esquina(cubo, colores2)
        
        if not (pieza1 and pieza2):
            print("No se han encontrado las esquinas a intercambiar")
            return None

        # stickers: (objeto, atributo) de los 3 stickers de cada esquina
        stickers1 = [
            (pieza1, 'color'),
            (pieza1.precedente, 'color'),
            (pieza1.adyacente, 'color'),
        ]
        stickers2 = [
            (pieza2, 'color'),
            (pieza2.adyacente, 'color'),
            (pieza2.precedente, 'color'),
        ]

        # Para k = 0,1,2: empareja colores1[k] ↔ colores2[k]
        for k in range(3):
            c1_t = colores1[k]
            c2_t = colores2[k]

            # Busca sticker en esquina1 con c1_t
            for obj, attr in stickers1:
                if getattr(obj, attr) == c1_t:
                    s1_obj, s1_attr = obj, attr
                    break

            # Busca sticker en esquina2 con c2_t
            for obj, attr in stickers2:
                if getattr(obj, attr) == c2_t:
                    s2_obj, s2_attr = obj, attr
                    break

            # Intercambia
            tmp = getattr(s1_obj, s1_attr)
            setattr(s1_obj, s1_attr, getattr(s2_obj, s2_attr))
            setattr(s2_obj, s2_attr, tmp)

        return cubo
        
    def cambiar_paridad(self, eleccion):
        # Cambia la paridad intercambiando los valores 1 y 2 en el diccionario seleccionado
        if eleccion == 0:
            nueva = self.perm1.copy()
        elif eleccion == 2:
            nueva = self.perm2.copy()
        else:
            print("Elección no válida. Debe ser 0 o 2.")
            return None

        # Buscar claves con valor 1 y 2
        claves_valor_1 = [k for k, v in nueva.items() if v == 1]
        claves_valor_2 = [k for k, v in nueva.items() if v == 2]

        if claves_valor_1 and claves_valor_2:
            # Tomamos la primera de cada una
            k1 = claves_valor_1[0]
            k2 = claves_valor_2[0]
            # Intercambiamos los valores
            nueva[k1], nueva[k2] = nueva[k2], nueva[k1]
        else:
            print("No se encontraron ambos valores 1 y 2 para intercambiar.")

        return nueva
                
    def buscar_casillas_intercambiadas(self, permutacion_nueva, cubo, eleccion):
        """
        Busca las aristas o esquinas que han sido intercambiadas en la nueva permutación.
        Devuelve una lista de colores de las piezas que han cambiado.
        """
        if eleccion == 0:
            # Buscar las claves que tenían valor 1 y 2 en perm1
            original_k1 = next((k for k, v in self.perm1.items() if v == 1), None)
            original_k2 = next((k for k, v in self.perm1.items() if v == 2), None)

            # Buscar las claves que ahora tienen valor 1 y 2 en permutacion_nueva
            nueva_k1 = next((k for k, v in permutacion_nueva.items() if v == 1), None)
            nueva_k2 = next((k for k, v in permutacion_nueva.items() if v == 2), None)

            if original_k1 != nueva_k1 or original_k2 != nueva_k2:
                return [[cubo[0][1].color, cubo[0][1].adyacente.color],
                        [cubo[1][0].color, cubo[1][0].adyacente.color]]
            else:
                print("No se han intercambiado las aristas con valores 1 y 2")
                return None

        elif eleccion == 2:
            original_k1 = next((k for k, v in self.perm2.items() if v == 1), None)
            original_k2 = next((k for k, v in self.perm2.items() if v == 2), None)

            nueva_k1 = next((k for k, v in permutacion_nueva.items() if v == 1), None)
            nueva_k2 = next((k for k, v in permutacion_nueva.items() if v == 2), None)

            if original_k1 != nueva_k1 or original_k2 != nueva_k2:
                return [[cubo[0][0].color, cubo[0][0].adyacente.color, cubo[0][0].precedente.color],
                        [cubo[2][0].color, cubo[2][0].adyacente.color, cubo[2][0].precedente.color]]
            else:
                print("No se han intercambiado las esquinas con valores 1 y 2")
                return None

        return None