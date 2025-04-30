from robodk.robolink import *   # API para comunicarse con RoboDK
from robodk.robomath import *   # Funciones matemáticas para manipular posiciones y orientaciones
import builtins                 # Para imprimir en consola
import threading

PRINT_CONSOLE = True          # True para imprimir en consola, False para imprimir en la ventana de RoboDK
SHOW_ERROR = True               # True para mostrar errores, False para no mostrar errores

def getRDK():
    return Robolink()

""" Permite decidir si se quiere imprimir en la consola o en la ventana de RoboDK.
    
    Recibe el mensaje a imprimir y un booleano que indica si se quiere mostrar el 
    mensaje en una ventana emergente o no.
    
    La librería tiene una variable global PRINT_CONSOLE que indica 
    si se quiere imprimir en la consola o no."""
def print(mensaje, popup = True):
    if PRINT_CONSOLE:
        builtins.print(mensaje)
    else:
        getRDK().ShowMessage(mensaje, popup)

""" Función para obtener un robot de RoboDK. La función comprueba que el robot existe.
    
    Recibe el nombre del robot como parámetro y devuelve el objeto robot.
    Devuelve None si no existe el robot."""
def getRobot(nombre):
    rdk = getRDK()
    robot = rdk.Item(nombre, ITEM_TYPE_ROBOT)
    if not robot.Valid():
        print(f"Error: Robot {nombre} no encontrado.", SHOW_ERROR)
        return None
    return robot

def getFrame(nombre):
    rdk = getRDK()
    frame = rdk.Item(nombre, ITEM_TYPE_FRAME)
    if not frame.Valid():
        print(f"Error: Sistema de referencia {frame} no encontrado.", SHOW_ERROR)
        return None
    return frame

""" Función para obtener un objeto de RoboDK. 
    La función comprueba que el objeto existe.
    
    Recibe el nombre del objeto como parámetro y el tipo del objeto (opcional) 
    y devuelve el objeto. Devuelve None si no existe el objeto. """
def getItem(nombre, tipo=None):
    rdk = getRDK()
    item = rdk.Item(nombre, tipo) if tipo else rdk.Item(nombre)
    if not item.Valid():
        print(f"Error: Objeto {nombre} no encontrado.", SHOW_ERROR)
        return None
    return item