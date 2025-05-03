from FuncionesBase import *
from Grafo import *

import math


def caminoConRotaciones(camino):
    resultado = ([])

    for i in range(len(camino) - 1):
        x1, y1 = camino([i])
        x2, y2 = camino([i + 1])

        dx = x2 - x1
        dy = y2 - y1

        # Calcular ángulo en grados
        anguloRad = math.atan2(dy, dx)
        anguloDeg = math.degrees(anguloRad)
        if anguloDeg < 0:
            anguloDeg += 360

        resultado.append(([x1, y1, 0, anguloDeg]))

    # Añadir el último punto
    if len(camino) >= 2:
        resultado.append(([camino([-1])([0]), camino([-1])([1]), 0, anguloDeg]))
    elif len(camino) == 1:
        resultado.append(([camino([0])([0]), camino([0])([1]), 0, 0]))

    return resultado

g = Grafo()
g.nodo("A", [0, 0])
g.nodo("B", [1, 0])
g.nodo("C", [2, 0])
g.nodo("D", [0, 1])
g.nodo("E", [1, 1])
g.nodo("F", [2, 1])
g.nodo("G", [0, 2])

g.conect("A", "B")
g.conect("B", "C")
g.conect("A", "D")
g.conect("B", "E")
g.conect("C", "F")
g.conect("D", "G")

subgrafo = [["A", "B", "C"], ["D", "E"], ["F"]]

g.printGrafo()



grafo = Grafo()

a = grafo.nodo("a",[0, 0])
b = grafo.nodo("b",[1, 0])
c = grafo.nodo("c",[1, 1])
d = grafo.nodo("d",[0, 1])
e = grafo.nodo("e",[0, 0])

grafo.conect(a, b)
grafo.conect(b, c)
grafo.conect(c, d)
grafo.conect(d, a)
grafo.conect(c, e)

camino = grafo.camino(a, e)
if camino is None:
    print("No se encontró un camino.")
else:
    for i in range(len(camino)):
        print(f"Posición {i}: {camino[i]}")
print("Camino encontrado:", camino)
grafo.printGrafo()

from mqtt_modular import *

def callback(topic, payload):
    print(f"Mensaje recibido en {topic}: {payload}")

set_prefix("PR2/A9/")
setup_mqtt()
publish("test", "Hello, world!")
register_callback("test", callback)
while True:
    pass