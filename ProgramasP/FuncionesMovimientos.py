from robodk.robolink import *
import threading
from time import *
from FuncionesBase import *
from FuncionesRobot import *
from CallPrograms import *
from FuncionesQyB import *
from Reset import *
from Grafo import *
from AGV import *

work = threading.Event()
espera = threading.Event()

def killThreads():
    work.set()
    espera.set()
    for thread in threading.enumerate():
        if thread is not threading.current_thread():
            thread.join()
    print("Todos los hilos han terminado.", False)

def reviveThreads():
    work.clear()
    print("Todos los hilos han revivido.", False)

configuracionesGeneral = {
    "SensorQueso5":("MecanismoCintaQueso5","Objeto_CintaQueso6",[1000]),
    "SensorQueso6":("MecanismoCintaQueso6","Objeto_CurvaQueso7",[1230]),
    "SensorQueso7":("MecanismoCurvaQueso7","Objeto_CintaQueso8",[3]),
    "SensorQueso8":("MecanismoCintaQueso8","Objeto_CurvaQueso9",[1230]),
    "SensorQueso9":("MecanismoCurvaQueso9","Objeto_Gira",[3]),
    "SensorQueso10":("MecanismoCintaQueso10","Objeto_Final",[1290]),
    "SensorBandeja1":("MecanismoCurvaBandeja1","Objeto_CintaBandeja2",[3]),
    "SensorBandeja2":("MecanismoCintaBandeja2","Objeto_CintaBandeja3",[1000]),
    "SensorBandeja3":("MecanismoCintaBandeja3","Objeto_CintaBandeja4",[1000]),
    "SensorBandeja4":("MecanismoCintaBandeja4","Objeto_CurvaBandeja5",[1030]),
    "SensorBandeja5":("MecanismoCurvaBandeja5","Objeto_CintaBandeja6",[3]),
    "SensorBandeja6":("MecanismoCintaBandeja6","Objeto_CintaBandeja7",[1000]),
    "SensorBandeja7":("MecanismoCintaBandeja7","Objeto_CintaBandeja8",[1000]),
    "SensorBandeja8":("MecanismoCintaBandeja8","Objeto_CintaBandeja9",[1000]),
    "SensorBandeja9":("MecanismoCintaBandeja9","Objeto_CurvaBandeja10",[1220]),
    "SensorBandeja10":("MecanismoCurvaBandeja10","Objeto_CintaBandeja11",[3]),
    "SensorBandeja11":("MecanismoCintaBandeja11","Objeto_CintaBandeja12",[1000]),
    "SensorBandeja12":("MecanismoCintaBandeja12","Objeto_CintaBandeja13",[1000]),
    "SensorBandeja13":("MecanismoCintaBandeja13","Objeto_CurvaBandeja14",[1030]),
    "SensorBandeja14":("MecanismoCurvaBandeja14","Objeto_Guia1",[3]),
}

def cintaInicio(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector = getItem("SensorInicio", ITEM_TYPE_OBJECT)
    robot = getRobot("MecanismoCintaQueso1")
    frame = getFrame("Objeto_CurvaQueso3")
    detectaQ = []

    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            detectaQ.append(itemQ)

    detectaB = []
    # Añadimos las bandejas que ya existen al array detectaB, no está en una función para que así no hayan condiciones de carrrera
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            detectaB.append(itemB)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaQ = getAllQuesos()
        if len(listaQ) > len(detectaQ):
            nuevoQ = getLastQueso()
            itemQ = getItem(nuevoQ, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                detectaQ.append(itemQ)

        listaB = getAllBandejas()
        if len(listaB) > len(detectaB):
            nuevoB = getLastBandeja()
            itemB = getItem(nuevoB, ITEM_TYPE_OBJECT)
            if itemB is not None:
                detectaB.append(itemB)

        num = sensor(detector, detectaQ)
        if num is not None:
            bandeja = detectaB[detectaQ.index(num)]
            moveTo(robot, [2030])
            setParent(frame, num)
            setParent(frame, bandeja)
            resetMecanismo("MecanismoCintaQueso1")


def curvaInicio(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector=getItem("SensorQueso1",ITEM_TYPE_OBJECT)
    robot=getRobot("MecanismoCurvaQueso3")
    frame=getFrame("Objeto_SeparaBandejas1")
    detectaQ = []

    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            detectaQ.append(itemQ)

    detectaB = []
    # Añadimos las bandejas que ya existen al array detectaB, no está en una función para que así no hayan condiciones de carrrera
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            detectaB.append(itemB)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaQ = getAllQuesos()
        if len(listaQ) > len(detectaQ):
            nuevoQ = getLastQueso()
            itemQ = getItem(nuevoQ, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                detectaQ.append(itemQ)

        listaB = getAllBandejas()
        if len(listaB) > len(detectaB):
            nuevoB = getLastBandeja()
            itemB = getItem(nuevoB, ITEM_TYPE_OBJECT)
            if itemB is not None:
                detectaB.append(itemB)

        num = sensor(detector,detectaQ)
        if num is not None:
            bandeja = detectaB[detectaQ.index(num)]
            moveTo(robot, [-90])
            setParent(frame,num)
            setParent(frame,bandeja)
            resetMecanismo("MecanismoCurvaQueso3")

def separaBandejas(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector=getItem("SensorSeparaBandejas1",ITEM_TYPE_OBJECT)
    robot=getRobot("MecanismoSeparaBandejas1")
    robot2=getRobot("MecanismoSeparaBandejas2")
    frame=getFrame("Objeto_CurvaBandeja1")
    frame2=getFrame("Objeto_CintaQueso5")
    frame3=getFrame("Objeto_SeparaBandejas2")
    detectaB = []

    # Añadimos las bandejas que ya existen al array detectaB, no está en una función para que así no hayan condiciones de carrrera
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            detectaB.append(itemB)

    detectaQ = []
    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            detectaQ.append(itemQ)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaB = getAllBandejas()
        if len(listaB) > len(detectaB):
            nuevoB = getLastBandeja()
            itemB = getItem(nuevoB, ITEM_TYPE_OBJECT)
            if itemB is not None:
                detectaB.append(itemB)

        listaQ = getAllQuesos()
        if len(listaQ) > len(detectaQ):
            nuevoQ = getLastQueso()
            itemQ = getItem(nuevoQ, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                detectaQ.append(itemQ)

        num = sensor(detector,detectaB)
        if num is not None:
            moveTo(robot, [530])
            moveTo(robot2, [0,0])
            setParent(frame3,num)
            moveTo(robot2, [320, 0])
            setParent(frame,num)
            t = threading.Thread(target=moveTo, args=(robot2,[0,0]))
            t.start()
            moveTo(robot, [1030])
            queso = detectaQ[detectaB.index(num)]
            setParent(frame2,queso)
            t.join()
            resetMecanismo("MecanismoSeparaBandejas1")
            resetMecanismo("MecanismoSeparaBandejas2")

def cintas(nombreSensor, ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    if "Queso" in nombreSensor:
        objeto = []
        for queso in getAllQuesos():
            itemQ = getItem(queso, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                objeto.append(itemQ)
    elif "Bandeja" in nombreSensor:
        objeto = []
        for bandeja in getAllBandejas():
            itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
            if itemB is not None:
                objeto.append(itemB)
    else:
        return None
    mecanismo, objetivo, pos = configuracionesGeneral[nombreSensor]
    detector=getItem(nombreSensor,ITEM_TYPE_OBJECT)
    robot=getRobot(mecanismo)
    objetivo=getFrame(objetivo)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        # Comprobamos si hay un nuevo objeto en la lista de objetos
        lista = getAllQuesos() if "Queso" in nombreSensor else getAllBandejas()
        if len(lista) > len(objeto):
            nuevo = getLastQueso() if "Queso" in nombreSensor else getLastBandeja()
            item = getItem(nuevo, ITEM_TYPE_OBJECT)
            if item is not None:
                objeto.append(item)

        num = sensor(detector, objeto)
        if num is not None:
            moveTo(robot, pos)
            setParent(objetivo, num)
            resetMecanismo(mecanismo)

def giraQuesos(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector=getItem("SensorGiraQuesos",ITEM_TYPE_OBJECT)
    robot=getRobot("MecanismoEntrada")
    robot2=getRobot("MecanismoGiraQuesos")
    robot3=getRobot("MecanismoGravedad")
    frame=getFrame("Objeto_CintaQueso10")
    detectaQ = []
    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            detectaQ.append(itemQ)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaQ = getAllQuesos()
        if len(listaQ) > len(detectaQ):
            nuevoQ = getLastQueso()
            itemQ = getItem(nuevoQ, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                detectaQ.append(itemQ)

        num = sensor(detector,detectaQ)
        if num is not None:
            moveTo(robot, [400])
            moveTo(robot2, [180])
            moveTo(robot3, [60])
            moveTo(robot, [0])
            setParent(frame,num)
            resetMecanismo("MecanismoEntrada")
            resetMecanismo("MecanismoGiraQuesos")
            resetMecanismo("MecanismoGravedad")

def Guia(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector=getItem("SensorGuia1",ITEM_TYPE_OBJECT)
    robot=getRobot("MecanismoGuia1")
    robot2=getRobot("MecanismoGuia2")
    robot3=getRobot("MecanismoGuia3")
    frame=getFrame("Objeto_Guia2")
    frame2=getFrame("Objeto_Guia3")
    frame3=getFrame("Objeto_Final")
    detectaB = []

    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            detectaB.append(itemB)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaB = getAllBandejas()
        if len(listaB) > len(detectaB):
            nuevoB = getLastBandeja()
            itemB = getItem(nuevoB, ITEM_TYPE_OBJECT)
            if itemB is not None:
                detectaB.append(itemB)

        num = sensor(detector,detectaB)
        if num is not None:
            moveTo(robot, [250])
            setParent(frame,num)
            moveTo(robot2, [566])
            setParent(frame2,num)
            moveTo(robot3, [565])
            setParent(frame3,num)
            resetMecanismo("MecanismoGuia1")
            resetMecanismo("MecanismoGuia2")
            resetMecanismo("MecanismoGuia3")

def recogeBandejas(ready):
    #Definimos las variables antes del bucle infinito para que no se creen cada vez que se entra en el bucle
    detector=getItem("SensorQueso11",ITEM_TYPE_OBJECT)
    robot=getRobot("MecanismoFinal")
    frame=getFrame("ColocacionFinal")
    detectaQ = []

    # Añadimos los quesos que ya existen al array detectaQ, no está en una función para que así no hayan condiciones de carrrera
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            detectaQ.append(itemQ)

    detectaB = []
    # Añadimos las bandejas que ya existen al array detectaB, no está en una función para que así no hayan condiciones de carrrera
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            detectaB.append(itemB)

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaQ = getAllQuesos()
        if len(listaQ) > len(detectaQ):
            nuevoQ = getLastQueso()
            itemQ = getItem(nuevoQ, ITEM_TYPE_OBJECT)
            if itemQ is not None:
                detectaQ.append(itemQ)

        listaB = getAllBandejas()
        if len(listaB) > len(detectaB):
            nuevoB = getLastBandeja()
            itemB = getItem(nuevoB, ITEM_TYPE_OBJECT)
            if itemB is not None:
                detectaB.append(itemB)

        num = sensor(detector,detectaQ)
        if num is not None:
            bandeja = detectaB[detectaQ.index(num)]
            moveTo(robot, [-60, 980])
            setParent(frame,num)
            setParent(frame,bandeja)
            resetMecanismo("MecanismoFinal")

def paletizador(ready):
    robot = getRobot("UR20")
    frame = getFrame("Fork_Frame")
    detector = getItem("SensorPick", ITEM_TYPE_OBJECT)
    quesosPaletizados = []
    bandejasPaletizadas = []

    estantes = []
    for i in range(1, 10):
        estante = getItem(f"Target_Estante{i}", ITEM_TYPE_TARGET)
        if estante is not None:
            estantes.append(estante)

    estantesAproximacion = []
    for i in range(1, 10):
        estante = getItem(f"Target_AproximacionEstante{i}", ITEM_TYPE_TARGET)
        if estante is not None:
            estantesAproximacion.append(estante)

    framesEstantes = []
    for i in range(1, 10):
        estante = getFrame(f"Estante{i}")
        if estante is not None:
            framesEstantes.append(estante)

    quesos = []
    for queso in getAllQuesos():
        itemQ = getItem(queso, ITEM_TYPE_OBJECT)
        if itemQ is not None:
            quesos.append(itemQ)

    bandejas = []
    for bandeja in getAllBandejas():
        itemB = getItem(bandeja, ITEM_TYPE_OBJECT)
        if itemB is not None:
            bandejas.append(itemB)

    grafo = initGrafo()

    ready.set()

    while not work.is_set():
        espera.wait()
        if work.is_set():
            break
        listaQ = getAllQuesos()
        listaB = getAllBandejas()

        if len(listaQ) > len(quesos):
            itemQ = getItem(getLastQueso(), ITEM_TYPE_OBJECT)
            if itemQ is not None:
                quesos.append(itemQ)

        if len(listaB) > len(bandejas):
            itemB = getItem(getLastBandeja(), ITEM_TYPE_OBJECT)
            if itemB is not None:
                bandejas.append(itemB)

        queso = sensor(detector, quesos)
        if queso is not None:
            numero = (quesos.index(queso)) % 9 + 1
            bandeja = bandejas[quesos.index(queso)]

            moveTo(robot, [167.1, -107.92, -134.17, -120.95, -13.74, -176.83])
            moveTo(robot, [143.16, -119.23, -116.04, -125.92, -37.29, -178.83])
            moveTo(robot, [143.95, -119.05, -116.06, -126.10, -36.79, -178.81])

            setParent(frame, queso)
            setParent(frame, bandeja)

            moveTo(robot, [144.53, -98.95, -101.40, -160.87, -36.21, -178.79])
            moveTo(robot, [95.55, -68.08, -118.11, -171.86, -173.80, -177.34])

            if numero < 9:
                moveTo(robot, estantesAproximacion[numero-1], "MoveL")
                moveTo(robot, estantes[numero-1], "MoveL")
            elif numero == 9:
                moveTo(robot, [122.09, -82.27, -72.05, -26.25, -205.95, 0.19])
                moveTo(robot, [156.55, -93.02, -61.99, -25.33, -247.29, 0.53])

            setParent(framesEstantes[numero-1], queso)
            setParent(framesEstantes[numero-1], bandeja)

            quesosPaletizados.append(queso)
            bandejasPaletizadas.append(bandeja)

            if numero < 9:
                moveTo(robot, estantesAproximacion[numero-1], "MoveL")
                moveTo(robot, [107.70, -68.18, -127.88, -163.27, -161.66, -178.64])
            elif numero == 9:
                moveTo(robot, [122.09, -82.27, -72.05, -26.25, -205.95, 0.19])
                moveTo(robot, [95.55, -68.08, -118.11, -171.86, -173.80, -177.34])
                moveTo(robot, [107.70, -68.18, -127.88, -163.27, -161.66, -178.64])
                espera.clear()
                callAGV(espera, grafo, quesosPaletizados, bandejasPaletizadas)


