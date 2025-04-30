from robodk.robolink import *
import threading
from time import *
from FuncionesBase import *
from FuncionesRobot import *
from CallPrograms import *
from FuncionesQyB import *
from Reset import *
from FuncionesMovimientos import *

reset()
print(f"Todo Reseteado, Empezamos")

def secuencia_inicio():
    preQueso = getItem(getLastQueso(), ITEM_TYPE_OBJECT)
    preBandeja = getItem(getLastBandeja(), ITEM_TYPE_OBJECT)
    frame = getFrame("Objeto_CintaQueso1")
    while True:
        queso = addQueso()
        bandeja = addBandeja()
        setParent(frame, preQueso)
        setParent(frame, preBandeja)
        setVisibility(True, preQueso)
        setVisibility(True, preBandeja)
        setVisibility(False, queso)
        setVisibility(False, bandeja)
        preQueso = queso
        preBandeja = bandeja
        time.sleep(14)


hilos = []
t = threading.Thread(target=cintaInicio)
t.start()
hilos.append(t)

t = threading.Thread(target=curvaInicio)
t.start()
hilos.append(t)

t = threading.Thread(target=separaBandejas)
t.start()
hilos.append(t)

sensores = ["SensorQueso5", "SensorQueso6", "SensorQueso7", "SensorQueso8",
            "SensorQueso9", "SensorQueso10", "SensorBandeja1", "SensorBandeja2",
            "SensorBandeja3", "SensorBandeja4", "SensorBandeja5", "SensorBandeja6",
            "SensorBandeja7", "SensorBandeja8", "SensorBandeja9", "SensorBandeja10",
            "SensorBandeja11", "SensorBandeja12", "SensorBandeja13", "SensorBandeja14"]

for sensor in sensores:
    t = threading.Thread(target=cintas, args=(sensor,))
    t.start()
    hilos.append(t)

t = threading.Thread(target=giraQuesos)
t.start()
hilos.append(t)

t = threading.Thread(target=Guia)
t.start()
hilos.append(t)

t = threading.Thread(target=recogeBandejas)
t.start()
hilos.append(t)

t = threading.Thread(target=paletizador)
t.start()
hilos.append(t)

t = threading.Thread(target=secuencia_inicio)
t.start()
hilos.append(t)

for hilo in hilos:
    hilo.join()