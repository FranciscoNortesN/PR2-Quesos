import networkx as nx
import matplotlib.pyplot as plt

from FuncionesBase import *
from FuncionesMovimientos import *
from FuncionesRobot import *
from CallPrograms import *
from FuncionesQyB import *
from Reset import *
from Grafo import *

nodosEstacion = []
nodosPasillo = []

def conectarNodos(grafo, nodos):
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            if nodos[i] != nodos[j]:
                grafo.conect(nodos[i], nodos[j])

def initGrafo():
    grafo = Grafo()

    nodosEstacion = [
        grafo.nodo("baseCarga", [-110, 2890]),
        grafo.nodo("Central1", [-490, -660]),
        grafo.nodo("Central2", [-490, -145]),
        grafo.nodo("Central3", [-490, 340]),
    ]

    nodosPasilloGeneral = [
        grafo.nodo("fueraAlmacen1", [-1220, -5030]),
        grafo.nodo("fueraAlmacen2", [-1220, -430]),
        grafo.nodo("fueraAlmacen3", [-1220, 4270]),
        grafo.nodo("salirCentral1", [-1220, -660]),
        grafo.nodo("salirCentral2", [-1220, -145]),
        grafo.nodo("salirCentral3", [-1220, 340]),
        grafo.nodo("salirCarga", [-1220, 2890])
    ]

    conectarNodos(grafo, nodosPasilloGeneral)
    grafo.conect("baseCarga", "salirCarga")
    grafo.conect("Central1", "salirCentral1")
    grafo.conect("Central2", "salirCentral2")
    grafo.conect("Central3", "salirCentral3")

    def crearAlmacen(grafo, numAlmacen, posy):
        posyfila1 = posy + 110
        posyfila2 = posy + 1840
        
        def crearFila(grafo, numAlmacen, numFila, posy):
            estanteriasA = []
            pasillo = []
            estanteriasB = []
            pasillo.append(grafo.nodo(f"filaEntrada{numAlmacen}{numFila}", [-2660, posy]))
            for j in range(4):
                x = -3320 - j * 500
                estanteriasA.append(grafo.nodo(f"estanteriaA{numAlmacen}{numFila}{j}", [x, posy -585]))
                pasillo.append(grafo.nodo(f"pasillo{numAlmacen}{numFila}{j}", [x, posy]))
                estanteriasB.append(grafo.nodo(f"estanteriaB{numAlmacen}{numFila}{j}", [x, posy + 585]))
                grafo.conect(f"pasillo{numAlmacen}{numFila}{j}", f"estanteriaA{numAlmacen}{numFila}{j}")
                grafo.conect(f"pasillo{numAlmacen}{numFila}{j}", f"estanteriaB{numAlmacen}{numFila}{j}")
            conectarNodos(grafo, pasillo)
            fila = []
            fila.append(estanteriasA)
            fila.append(pasillo)
            fila.append(estanteriasB)

            return fila
        
        fila1 = crearFila(grafo, numAlmacen, 1, posyfila1)
        fila2 = crearFila(grafo, numAlmacen, 2, posyfila2)
        grafo.conect(fila1[1][0], fila2[1][0])

        grafo.nodo(f"entradaAlmacen{numAlmacen}", [-2660, posy])
        grafo.conect(f"entradaAlmacen{numAlmacen}", fila1[1][0])
        grafo.conect(f"entradaAlmacen{numAlmacen}", fila2[1][0])
        grafo.conect(f"entradaAlmacen{numAlmacen}", f"fueraAlmacen{numAlmacen}")

    crearAlmacen(grafo, 1, -5030)
    crearAlmacen(grafo, 2, -430)
    crearAlmacen(grafo, 3, 4270)

    return grafo

def visualizarGrafo(grafo, max_line_length=5, posiciones_destacadas=None):
    import textwrap

    G = nx.Graph()

    if posiciones_destacadas is None:
        posiciones_destacadas = []

    # Añadir nodos con posición
    for nombre, pos in grafo.nodos.items():
        G.add_node(nombre, pos=pos)

    # Añadir aristas evitando duplicados
    for nodo, vecinos in grafo.vecinos.items():
        for vecino in vecinos:
            if not G.has_edge(nodo, vecino):
                G.add_edge(nodo, vecino)

    pos = nx.get_node_attributes(G, 'pos')

    # Crear etiquetas con saltos de línea si son largas
    etiquetas = {
        nodo: "\n".join(textwrap.wrap(nodo, max_line_length)) for nodo in G.nodes
    }

    # Colorear nodos según posición
    colores = []
    for nodo in G.nodes:
        posicion = grafo.nodos[nodo]
        if posicion in posiciones_destacadas:
            colores.append("orange")  # Color para nodos destacados
        else:
            colores.append("skyblue")  # Color por defecto

    # Dibujar
    plt.figure(figsize=(12, 10))
    nx.draw(
        G, pos,
        with_labels=True,
        labels=etiquetas,
        node_size=800,
        node_color=colores,
        font_size=8
    )
    plt.title("Visualización del Grafo del Almacén")
    plt.axis('equal')
    plt.grid(True)
    plt.show()




# Ejecutar
grafo = initGrafo()
camino = grafo.camino("estanteriaA123", "estanteriaA311")
camino
visualizarGrafo(grafo, posiciones_destacadas=camino)


""" 
    3 almacenes
    cada almacen tiene 2 filas
    cada fila tiene estanterías a los lados
    cada fila tiene 4 estanterías

    hay un pasillo que conecta los 3 almacenes,
    los lugares de carga y descarga y la base de carga

    si hablamos de nodos, el pasillo posee un nodo por el lugar
    de carga, otro por el lugar de descarga y otro por la base de carga
    además de 3 nodos por cada entrada a los almacenes.

    si hablamos de los almacenes, cada uno tiene un nodo al entrar
    y uno en la entrada de cada fila

    si hablamos de cada fila, cada una tiene un nodo por cada pareja de estanterías
    y ese nodo se conecta con los nodos de las estanterías que se encuentran a los lados

    si hablamos de los lugares de carga y descarga y la base de carga, 
    cada uno tiene un nodo

    cada uno de estos nodos tiene 4 nodos orientados, de los cuales
    se conectan aquellos que se encuentran en la misma dirección con los demás nodos
    cada nodo orientado se conecta con los demás nodos orientados del mismo nodo



    tipo:almacen / carga / descarga
    almacen:
    fila:
    estantería
"""