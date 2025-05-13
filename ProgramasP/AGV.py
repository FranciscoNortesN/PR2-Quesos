import networkx as nx
import matplotlib.pyplot as plt

from FuncionesBase import *
from FuncionesRobot import *
from FuncionesQyB import *
from Reset import *
from Grafo import *
from mqtt_modular import*
import json

estanteria_destino = None

def conectarNodos(grafo, nodos):
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            if nodos[i] != nodos[j]:
                grafo.conect(nodos[i], nodos[j])

def initGrafo():
    grafo = Grafo()

    almacen1 = -5030
    almacen2 = -480
    almacen3 = 4090
    baseCarga = 2890
    Central1 = -660
    Central2 = -145
    Central3 = 340

    nodosEstacion = [
        grafo.nodo("baseCarga", [-110, baseCarga]),
        grafo.nodo("Central1", [-490, Central1]),
        grafo.nodo("Central2", [-490, Central2]),
        grafo.nodo("Central3", [-490, Central3]),
    ]

    grafo.nodoActual = "baseCarga"

    nodosPasilloGeneral = [
        grafo.nodo("fueraAlmacen1", [-1220, almacen1]),
        grafo.nodo("fueraAlmacen2", [-1220, almacen2]),
        grafo.nodo("fueraAlmacen3", [-1220, almacen3]),
        grafo.nodo("salirCentral1", [-1220, Central1]),
        grafo.nodo("salirCentral2", [-1220, Central2]),
        grafo.nodo("salirCentral3", [-1220, Central3]),
        grafo.nodo("salirCarga", [-1220, baseCarga]),
    ]

    conectarNodos(grafo, nodosPasilloGeneral)
    grafo.conect("baseCarga", "salirCarga")
    grafo.conect("Central1", "salirCentral1")
    grafo.conect("Central2", "salirCentral2")
    grafo.conect("Central3", "salirCentral3")

    def crearAlmacen(grafo, numAlmacen, posy):
        posyfila1 = posy + 110
        posyfila2 = posy + 2000
        
        def crearFila(grafo, numAlmacen, numFila, posy):
            estanteriasA = []
            pasillo = []
            estanteriasB = []
            pasillo.append(grafo.nodo(f"filaEntrada{numAlmacen}{numFila}", [-2660, posy]))
            for j in range(4):
                x = -3230 - j * 500
                estanteriasA.append(grafo.nodo(f"estanteriaA{numAlmacen}{numFila}{j}", [x, posy -545]))
                pasillo.append(grafo.nodo(f"pasillo{numAlmacen}{numFila}{j}", [x, posy]))
                estanteriasB.append(grafo.nodo(f"estanteriaB{numAlmacen}{numFila}{j}", [x, posy + 545]))
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

    crearAlmacen(grafo, 1, almacen1)
    crearAlmacen(grafo, 2, almacen2)
    crearAlmacen(grafo, 3, almacen3)

    return grafo

def calcularAngulo(origen, destino):
    dx = destino[0] - origen[0]
    dy = destino[1] - origen[1]
    anguloRad = math.atan2(dy, dx)
    anguloDeg = math.degrees(anguloRad)
    anguloDeg = anguloDeg - 90
    return anguloDeg

def generarCamino3D(camino2D, salidaMarchaAtras=False, anguloInicial=0):
    if len(camino2D) < 2:
        return [[x, y, 0, 0] for x, y in camino2D]  # Solo un punto

    camino3D = []
    puntoInicial = camino2D[0]
    puntoSiguiente = camino2D[1]

    # Calcular orientación inicial
    orientacion = calcularAngulo(puntoInicial, puntoSiguiente)
    if salidaMarchaAtras:
        orientacion = anguloInicial

    camino3D.append([puntoInicial[0], puntoInicial[1], 0, orientacion])
    camino3D.append([puntoSiguiente[0], puntoSiguiente[1], 0, orientacion])


    for i in range(2, len(camino2D)):
        puntoAnterior = camino2D[i - 1]
        puntoActual = camino2D[i]
        nuevaOrientacion = calcularAngulo(puntoAnterior, puntoActual)

        if not math.isclose(nuevaOrientacion, orientacion, abs_tol=1e-5):
            camino3D.append([puntoAnterior[0], puntoAnterior[1], 0, nuevaOrientacion])
            orientacion = nuevaOrientacion

        camino3D.append([puntoActual[0], puntoActual[1], 0, orientacion])

    return camino3D

estanteria_destino = None

import time

estanteria_destino = None  # Global para que el callback la modifique

def callAGV(espera, grafo, quesos, bandejas):
    global estanteria_destino
    estanteria_destino = None  # Resetear al inicio de la función

    def obtener_estanteria(topic, payload):
        global estanteria_destino
        estanteria = payload.strip()
        if estanteria:
            estanteria_destino = estanteria
            publish("AGV/logs", f"Destino actualizado a: {estanteria_destino}")

    register_callback("AGV", obtener_estanteria)

    baseAGV = getFrame("AGV")
    agv = getRobot("AGV")
    camino = grafo.camino(grafo.nodoActual, "Central3")
    camino3d = generarCamino3D(camino)
    if camino3d is None:
        print("No se encontró un camino a Central3.")
        return
    else:
        for i in range(len(camino3d)):
            print(f"Posición {i}: {camino3d[i]}")
            moveTo(agv, camino3d[i])
            grafo.nodoActual = grafo.getID(camino3d[i][0:2])

    TorreQuesosAGV = getItem("TorreQuesosAGV", ITEM_TYPE_OBJECT)
    setVisibility(True, TorreQuesosAGV)
    setVisibility(False, quesos)
    setVisibility(False, bandejas)
    Tool = getRobot("MecanismoAGVTool")
    moveTo(Tool, [40])

    # Espera indefinida hasta recibir estanteria_destino
    print("Esperando destino de estantería...")
    while estanteria_destino is None:
        time.sleep(0.1)

    camino = grafo.camino("Central3", estanteria_destino)
    camino3d = generarCamino3D(camino, salidaMarchaAtras=True, anguloInicial=camino3d[-1][3])
    if camino3d is None:
        print("No se encontró un camino hacia la estantería.")
        return
    else:
        for i in range(len(camino3d)):
            print(f"Posición {i}: {camino3d[i]}")
            moveTo(agv, camino3d[i])
            grafo.nodoActual = grafo.getID(camino3d[i][0:2])
    espera.set()
    moveTo(Tool, [10])

    carpeta = getItem("FramesAlmacenes", ITEM_TYPE_FOLDER)
    pos = camino3d[-1]
    pos.append(0)
    if "estanteriaA" in estanteria_destino:
        pos[0] = pos[0] - 370 + 30
        pos[1] = pos[1] + 150 - 60 + 120
    elif "estanteriaB" in estanteria_destino:
        pos[0] = pos[0] - 370 + 30 -20
        pos[1] = pos[1] - 150 - 60 + 120 + 180 + 400 -60
    for i in range(len(pos)):
        print(f"Posición {i}: {pos[i]}")
    nuevoFrame = addFrame(f"TorreQuesos_{estanteria_destino}", carpeta, pos)
    rdk = getRDK()
    item = getItem("TorreQuesos", ITEM_TYPE_OBJECT)
    if not item:
        return None
    item.Copy()
    nuevoItem = rdk.Paste()
    nuevoItem.setName(f"TorreQuesos_{estanteria_destino}")
    setParent(baseAGV, nuevoFrame)
    setParent(nuevoFrame, nuevoItem)
    setVisibility(True, nuevoItem)
    setVisibility(False, TorreQuesosAGV)

    camino = grafo.camino(estanteria_destino, "baseCarga")
    camino3d = generarCamino3D(camino, salidaMarchaAtras=True, anguloInicial=camino3d[-1][3])
    if camino3d is None:
        print("No se encontró un camino hacia baseCarga.")
    else:
        for i in range(len(camino3d)):
            print(f"Posición {i}: {camino3d[i]}")
            moveTo(agv, camino3d[i])
            grafo.nodoActual = grafo.getID(camino3d[i][0:2])


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
    
"""
agv = getRobot("AGV")

# Ejecutar
grafo = initGrafo()
camino = grafo.camino("baseCarga", "estanteriaB110")
camino3d = generarCamino3D(camino)
if camino3d is None:
    print("No se encontró un camino.")
else:
    for i in range(len(camino3d)):
        print(f"Posición {i}: {camino3d[i]}")
    for i in range(len(camino3d)):
        moveTo(agv, camino3d[i])
visualizarGrafo(grafo, posiciones_destacadas=camino)
"""