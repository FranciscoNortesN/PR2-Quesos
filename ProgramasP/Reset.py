from FuncionesBase import *
from FuncionesRobot import *
from FuncionesQyB import *

def resetMecanismo(nombreMecanismo):
    posReset = {
        "MecanismoSeparaBandejas2":[0,-80],
        "UR20":[107.70, -68.18, -127.88, -163.27, -161.66, -178.64],
        "MecanismoCurvaQueso3":[0],
        "Curva":[-90],
        "Bandeja2":[-30],
        "Bandeja6":[-30],
        "Guia1":[2.5],
        "MecanismoFinal":[0,280],
        "MecanismoTopeBandejaSalida":[-40],
        "Mecanismo":[0,0,0,0,0,0],
        "AGV":[-110, 2890,0,0],
    }
    for clave in posReset:
        if clave in nombreMecanismo:
            robot=getRobot(nombreMecanismo)
            setPose(robot, posReset[clave])
            return True
    return None

def reset():
    rdk = getRDK()
    items = rdk.ItemList(ITEM_TYPE_OBJECT)

    for item in items:
        name = item.Name()
        if name.startswith("Queso") and name != "Queso1" and name != "Queso0":
            item.Delete()
        elif name.startswith("Bandeja") and name != "Bandeja1" and name != "Bandeja0":
            item.Delete()

    delQuesos()
    delBandejas()

    queso = getItem("Queso1", ITEM_TYPE_OBJECT)
    bandeja = getItem("Bandeja1", ITEM_TYPE_OBJECT)
    setVisibility(False,queso)
    setVisibility(False,bandeja)
    queso0 = getItem("Queso0", ITEM_TYPE_OBJECT)
    bandeja0 = getItem("Bandeja0", ITEM_TYPE_OBJECT)
    setVisibility(False,queso0)
    setVisibility(False,bandeja0)
    frameQ=getFrame("QuesosInicio")
    setParent(frameQ,queso)
    setParent(frameQ,bandeja)
    setParent(frameQ,queso0)
    setParent(frameQ,bandeja0)

    items = rdk.ItemList(ITEM_TYPE_ROBOT)
    for item in items:
        resetMecanismo(item.Name())
