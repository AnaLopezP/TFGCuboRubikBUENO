'''if self.piezas_transmutadas is not None:
                print("Piezas transmutadas:", self.piezas_transmutadas)
                if len(self.piezas_transmutadas[0]) == 2:
                    # busco que colores están en la posicion (0, 1) y (1, 0)
                    colores1 = [cube_state["B"][0][1], cube_state["R"][2][1]]
                    colores2 = [cube_state["B"][1][0], cube_state["AZ"][1][2]]
                    
                    # intercambio esos colores
                    cube_state["B"][0][1], cube_state["R"][2][1] = colores2
                    cube_state["B"][1][0], cube_state["AZ"][1][2] = colores1
                    
                    # Actualizar la matriz del cubo
                    asignar_color_deuna(self.cubo)
                
                elif len(self.piezas_transmutadas[0]) == 3:
                    # busco que colores están en la posicion (0, 0) y (2, 0)
                    colores1 = [cube_state["B"][0][0], cube_state["R"][2][0], cube_state["AZ"][0][2]]
                    colores2 = [cube_state["B"][2][0], cube_state["AZ"][2][2], cube_state["N"][0][0]]
                    
                    # intercambio esos colores
                    cube_state["B"][0][0], cube_state["R"][2][0], cube_state["AZ"][0][2] = colores2
                    cube_state["B"][2][0], cube_state["AZ"][2][2], cube_state["N"][0][0] = colores1
                    
                    # Actualizar la matriz del cubo
                    asignar_color_deuna(self.cubo)
                    
                piezas_transmutadas = [colores1, colores2]
                print("Colores transmutados:", piezas_transmutadas)'''
        
        
'''def aplicar_errores(self):
        asignar_color_deuna(self.cubo)
        orb = Orbitas(self.movimiento_origen)
        # --- Flip de la pieza cambiada ---
        if self.piecita_cambiada is not None:
            print("Piezas flippeadas:", self.piecita_cambiada)
            for casilla in range(len(self.piecita_cambiada)):
                colores = self.piecita_cambiada[casilla]
                if len(colores) == 2:
                    # Arista
                    pieza = orb.buscar_posicion_por_color_arista(self.cubo, colores)
                    if pieza:
                        i, j = pieza.fila, pieza.columna
                        ia, ja = pieza.adyacente.fila, pieza.adyacente.columna
                        cara0, cara1 = pieza.cara, pieza.adyacente.cara
                        c0 = cube_state[cara0][i][j]
                        c1 = cube_state[cara1][ia][ja]
                        cube_state[cara0][i][j] = c1
                        cube_state[cara1][ia][ja] = c0
                        orb.flippear_arista(self.cubo, (i, j))
                else:
                    # Esquina
                    pieza = orb.buscar_posicion_por_color_esquina(self.cubo, colores)
                    if pieza:
                        i, j = pieza.fila, pieza.columna
                        ia, ja = pieza.adyacente.fila, pieza.adyacente.columna
                        ip, jp = pieza.precedente.fila, pieza.precedente.columna
                        cara0, cara1, cara2 = pieza.cara, pieza.adyacente.cara, pieza.precedente.cara
                        c0 = cube_state[cara0][i][j]
                        c1 = cube_state[cara1][ia][ja]
                        c2 = cube_state[cara2][ip][jp]
                        if self.sentido == 1:
                            cube_state[cara0][i][j] = c2
                            cube_state[cara1][ia][ja] = c0
                            cube_state[cara2][ip][jp] = c1
                            
                        elif self.sentido == 2:
                            cube_state[cara0][i][j] = c1
                            cube_state[cara1][ia][ja] = c2
                            cube_state[cara2][ip][jp] = c0
                            
        # --- Transmutación de piezas ---
        if self.piezas_transmutadas is not None:
                print("Piezas transmutadas:", self.piezas_transmutadas)
                if len(self.piezas_transmutadas[0]) == 2:
                    # Desempaqueta directamente las dos listas de colores
                    colores1, colores2 = self.piezas_transmutadas

                    # Busca las dos piezas en la Molecula
                    pieza1 = orb.buscar_posicion_por_color_arista(self.cubo, colores1)
                    pieza2 = orb.buscar_posicion_por_color_arista(self.cubo, colores2)
                    if not (pieza1 and pieza2):
                        print("No encontradas las aristas a swapear")
                    else:
                        # Saca sus coordenadas y caras
                        f1, i1, j1 = pieza1.cara, pieza1.fila, pieza1.columna
                        f2, i2, j2 = pieza2.cara, pieza2.fila, pieza2.columna

                        # **Swap clásico** en cube_state
                        tmp = cube_state[f1][i1][j1]
                        cube_state[f1][i1][j1] = cube_state[f2][i2][j2]
                        cube_state[f2][i2][j2] = tmp
                
                elif len(self.piezas_transmutadas[0]) == 3:
                    # se han intercambiado dos esquinas
                    # cambiamos la matriz cubo
                    # cambiamos cube_state
                    colores1, colores2 = self.piezas_transmutadas
                    # Busca las tres piezas en la Molecula
                    pieza1 = orb.buscar_posicion_por_color_esquina(self.cubo, colores1)
                    pieza2 = orb.buscar_posicion_por_color_esquina(self.cubo, colores2)
                    if not (pieza1 and pieza2):
                        print("No encontradas las esquinas a swapear")
                    else:
                        # Saca sus coordenadas y caras
                        f1, i1, j1 = pieza1.cara, pieza1.fila, pieza1.columna
                        f2, i2, j2 = pieza2.cara, pieza2.fila, pieza2.columna

                        # **Swap clásico** en cube_state
                        tmp = cube_state[f1][i1][j1]
                        cube_state[f1][i1][j1] = cube_state[f2][i2][j2]
                        cube_state[f2][i2][j2] = tmp
        # Actualizar la vista 3D
        asignar_color_deuna(self.cubo)
        '''