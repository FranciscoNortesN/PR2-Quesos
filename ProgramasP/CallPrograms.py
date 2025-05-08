from FuncionesBase import *

SHOW_ERROR = True               # True para mostrar errores, False para no mostrar errores

def callProgram(nombre, tipo=ITEM_TYPE_PROGRAM_PYTHON):
    rdk = getRDK()
    prog = rdk.Item(nombre, tipo)
    if not prog.Valid():
        print(f"Warning: Programa {nombre} no encontrado. Creando placeholder.", SHOW_ERROR)
        prog = rdk.AddProgram(nombre)
    prog.RunProgram()

def callProgramP(nombre):
    callProgram(nombre, ITEM_TYPE_PROGRAM_PYTHON)

def callProgramR(nombre):
    callProgram(nombre, ITEM_TYPE_PROGRAM)