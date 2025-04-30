from FuncionesBase import *
import threading

SHOW_ERROR = True               # True para mostrar errores, False para no mostrar errores

# Listas reales protegidas (solo para escritura)
_totalQ = ["Queso1"]
_totalB = ["Bandeja1"]

# Copias inmutables para lectura sin bloqueo
totalQ = tuple(_totalQ)
totalB = tuple(_totalB)

# Locks de escritura
lockQ = threading.Lock()
lockB = threading.Lock()


def setParent(frame, objetos):
    if not frame or not objetos:
        return None

    def assign_parent(item):
        item.setParent(frame)

    if isinstance(objetos, list):
        for obj in objetos:
            assign_parent(obj)
    else:
        assign_parent(objetos)

    return True


def sensor(sensor_obj, objetos):
    if not sensor_obj or not objetos:
        return None

    def detect_collision(obj):
        return obj and sensor_obj.Collision(obj)

    if isinstance(objetos, list):
        for obj in objetos:
            if detect_collision(obj):
                return obj
        return None
    else:
        return objetos if detect_collision(objetos) else -1

def dupItem(prefix, itemName, nombreLista, tipo=None, dupChildren=True):
    global _totalQ, _totalB, totalQ, totalB

    rdk = getRDK()
    item = getItem(itemName, tipo)
    if not item:
        return None

    item.Copy(dupChildren)

    if nombreLista == "Quesos":
        with lockQ:
            nuevoNombre = f"{prefix}{len(_totalQ)+1}"
            _totalQ.append(nuevoNombre)
            nuevoItem = rdk.Paste()
            nuevoItem.setName(nuevoNombre)
            totalQ = tuple(_totalQ)
    elif nombreLista == "Bandejas":
        with lockB:
            nuevoNombre = f"{prefix}{len(_totalB)+1}"
            _totalB.append(nuevoNombre)
            nuevoItem = rdk.Paste()
            nuevoItem.setName(nuevoNombre)
            totalB = tuple(_totalB)
    else:
        return None


    return nuevoItem

def addQueso():
    return dupItem("Queso", "Queso1", "Quesos", ITEM_TYPE_OBJECT)

def addBandeja():
    return dupItem("Bandeja", "Bandeja1", "Bandejas", ITEM_TYPE_OBJECT)

def delCopies(Lista):
    global _totalQ, _totalB, totalQ, totalB
    if Lista == "Quesos":
        with lockQ:
            for nombre in _totalQ[1:]:
                item = getItem(nombre, ITEM_TYPE_OBJECT)
                if item:
                    item.Delete()
            _totalQ[:] = ["Queso1"]
            totalQ = tuple(_totalQ)
    elif Lista == "Bandejas":
        with lockB:
            for nombre in _totalB[1:]:
                item = getItem(nombre, ITEM_TYPE_OBJECT)
                if item:
                    item.Delete()
            _totalB[:] = ["Bandeja1"]
            totalB = tuple(_totalB)
    else:
        return -1
    return True

def delQuesos():
    return delCopies("Quesos")

def delBandejas():
    return delCopies("Bandejas")

def getLastQueso():
    return totalQ[-1]

def getLastBandeja():
    return totalB[-1]

def getAllQuesos():
    return totalQ

def getAllBandejas():
    return totalB

def setVisibility(visible, objetos):
    """Asigna un nuevo sistema de referencia (frame) a uno o varios objetos."""

    def changeVisibility(item):
        if item:
            item.setVisible(visible)
        else:
            return None

    if isinstance(objetos, list):
        for obj in objetos:
            changeVisibility(obj)
    else:
        changeVisibility(objetos)

    return True
