import heapq
import math

class Grafo:
    def __init__(self):
        self.nodos = {}  # id -> posición [x, y]
        self.vecinos = {}  # id -> lista de ids vecinos

    def nodo(self, id, posicion):
        self.nodos[id] = posicion
        self.vecinos[id] = []
        return id

    def conect(self, id1, id2):
        if id2 not in self.vecinos[id1]:
            self.vecinos[id1].append(id2)
        if id1 not in self.vecinos[id2]:
            self.vecinos[id2].append(id1)

    def distancia(self, id1, id2):
        p1 = self.nodos[id1]
        p2 = self.nodos[id2]
        return math.dist(p1, p2)

    def camino(self, id_inicio, id_fin):
        cola = [(0, id_inicio, [])]
        visitados = set()

        while cola:
            costo, actual, camino = heapq.heappop(cola)
            if actual in visitados:
                continue
            nuevo_camino = camino + [self.nodos[actual]]
            if actual == id_fin:
                return nuevo_camino
            visitados.add(actual)
            for vecino in self.vecinos[actual]:
                if vecino not in visitados:
                    nuevo_costo = costo + self.distancia(actual, vecino)
                    heapq.heappush(cola, (nuevo_costo, vecino, nuevo_camino))
        return None

    def printGrafo(self):
        print("GRAFO DE POSICIONES DEL AGV")
        for id, pos in self.nodos.items():
            vecinos = self.vecinos.get(id, [])
            if vecinos:
                vecinos_str = ', '.join(str(v) for v in vecinos)
            else:
                vecinos_str = "SIN CONEXIONES"
            print(f"Nodo '{id}': Posición {pos} -> Vecinos: {vecinos_str}")
