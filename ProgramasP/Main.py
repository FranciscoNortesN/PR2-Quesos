from robodk.robolink import *
import threading
from time import *
from FuncionesBase import *
from FuncionesRobot import *
from CallPrograms import *
from FuncionesQyB import *
from Reset import *
from FuncionesMovimientos import *
from mqtt_modular import *

print(f"Aviso, dependiendo de tu ordenador, el estado de la estación antes de ejecutar el programa y si se ha ejecutado el programa antes, puede tardar un poco en ejecutarse.")
reset()
print(f"Todo Reseteado, Inicializando el programa...",False)

readys = []


def secuencia_inicio():
    preQueso = getItem(getLastQueso(), ITEM_TYPE_OBJECT)
    preBandeja = getItem(getLastBandeja(), ITEM_TYPE_OBJECT)
    frame = getFrame("Objeto_CintaQueso1")
    for ready in readys:
        ready.wait()
    print("Programa inicializado, empezamos")
    espera.set()
    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
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



def placeQueso(preQueso, preBandeja, frame):
    queso = addQueso()
    bandeja = addBandeja()
    setParent(frame, preQueso)
    setParent(frame, preBandeja)
    setVisibility(False, queso)
    setVisibility(False, bandeja)
    setVisibility(True, preQueso)
    setVisibility(True, preBandeja)
    preQueso = queso
    preBandeja = bandeja
    return preQueso, preBandeja

def spawnQueso():
    flanco = False
    quesos = []
    preQueso = getItem(getLastQueso(), ITEM_TYPE_OBJECT)
    preBandeja = getItem(getLastBandeja(), ITEM_TYPE_OBJECT)
    quesos.append(preQueso)
    frame = getFrame("Objeto_CintaQueso1")
    for ready in readys:
        ready.wait()
    print("Programa inicializado, empezamos")
    espera.set()
    preQueso, preBandeja = placeQueso(preQueso, preBandeja, frame)
    quesos.append(preQueso)
    detector = getItem("SensorQueso7", ITEM_TYPE_OBJECT)
    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        queso1 = sensor(detector, quesos)
        if queso1 is not None:
            if not flanco:
                preQueso, preBandeja = placeQueso(preQueso, preBandeja, frame)
                quesos.append(preQueso)
            flanco = True
        else:
            flanco = False

# Inicializamos y nos conectamos al topic
set_prefix("PR2/A9/RoboDK/")
setup_mqtt()

hilos = []

ready = threading.Event()
t = threading.Thread(target=cintaInicio, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=curvaInicio, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=separaBandejas, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

sensores = ["SensorQueso5", "SensorQueso6", "SensorQueso7", "SensorQueso8",
            "SensorQueso9", "SensorQueso10", "SensorBandeja1", "SensorBandeja2",
            "SensorBandeja3", "SensorBandeja4", "SensorBandeja5", "SensorBandeja6",
            "SensorBandeja7", "SensorBandeja8", "SensorBandeja9", "SensorBandeja10",
            "SensorBandeja11", "SensorBandeja12", "SensorBandeja13", "SensorBandeja14"]

for sensors in sensores:
    ready = threading.Event()
    t = threading.Thread(target=cintas, args=(sensors, ready,))
    t.start()
    hilos.append(t)
    readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=giraQuesos, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=Guia, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=recogeBandejas, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

ready = threading.Event()
t = threading.Thread(target=paletizador, args=(ready,))
t.start()
hilos.append(t)
readys.append(ready)

t = threading.Thread(target=spawnQueso)
t.start()
hilos.append(t)

#time.sleep(180)
#killThreads()

for hilo in hilos:
    hilo.join()