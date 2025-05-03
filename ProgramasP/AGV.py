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

def calcularAngulo(origen, destino):
    dx = destino[0] - origen[0]
    dy = destino[1] - origen[1]
    anguloRad = math.atan2(dy, dx)
    anguloDeg = math.degrees(anguloRad)
    anguloDeg = anguloDeg - 90
    return anguloDeg

def generarCamino3D(camino2D):
    if len(camino2D) < 2:
        return [[x, y, 0, 0] for x, y in camino2D]  # Si solo hay un punto

    camino3D = []
    orientacionActual = calcularAngulo(camino2D[0], camino2D[1])
    camino3D.append([camino2D[0][0], camino2D[0][1], 0, orientacionActual])

    for i in range(1, len(camino2D)):
        puntoAnterior = camino2D[i - 1]
        puntoActual = camino2D[i]
        nuevaOrientacion = calcularAngulo(puntoAnterior, puntoActual)

        if not math.isclose(nuevaOrientacion, orientacionActual, abs_tol=1e-5):
            camino3D.append([puntoAnterior[0], puntoAnterior[1], 0, nuevaOrientacion])
            orientacionActual = nuevaOrientacion

        camino3D.append([puntoActual[0], puntoActual[1], 0, orientacionActual])

    return camino3D


agv = getRobot("AGV")

# Ejecutar
grafo = initGrafo()
camino = grafo.camino("estanteriaB222", "Central1")
camino3d = generarCamino3D(camino)
if camino3d is None:
    print("No se encontró un camino.")
else:
    for i in range(len(camino3d)):
        print(f"Posición {i}: {camino3d[i]}")
    for i in range(len(camino3d)):
        moveTo(agv, camino3d[i])
visualizarGrafo(grafo, posiciones_destacadas=camino)
