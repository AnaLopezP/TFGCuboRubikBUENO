# TFGCuboRubikBUENO

## Introducción
Este repositorio almacena todos los archivos necesarios para crear la aplicación 'Cubo Rubik Solver'. Dicho ejecutable no se incluye ya que es un archivo bastante grande y supera el límite de GitHub. 
A continuación se explica la estructura del codigo de manera general

## Grafo
Este archivo contiene toda la lógica relacionada con la creación de la ley de grupo (leer, guardar y operar los movimientos), y la creación del grafo, además de la búsqueda de la identidad en el mismo. 

## App Buena
Aquí se implementó toda la lógica de la aplicación (interfaces, botones, etc.), tanto en el cubo 2D como en el 3D. Para conectar la aplicación con la lógica de resolución, se crearon los archivos siguientes.

## Cubo
En este archivo se creó la estructura de datos que reconoce a cada combinación de colores como una casilla del cubo, y se implementaron traductores para pasar del cubo como mezcla de colores a un movimiento matemático y viceversa.

## Variables globales 
Aquí se almacenan las variables globales, como el estado del cubo general o la paleta de colores.

## Traducciones
En este archivo se encuentra un diccionario con todos los textos y botones que se utilizan a lo largo del flujo de la aplicación y su traducción a varios idiomas. 

## Órbitas
En este archivo se encuenta la lógica para encontrar movimientos válidos en caso de piezas descolocadas, intercambio de casillas y flip de esquinas y aristas. 
