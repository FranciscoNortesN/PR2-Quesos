from robodk.robolink import *  # Importamos la API de RoboDK
from robodk.robomath import *  # Importamos las herramientas matemáticas de RoboDK

# Conectarse al servidor de RoboDK
RDK = Robolink()

# Obtener los programas
programa_giraquesos = RDK.Item('ResetGiraQuesos', ITEM_TYPE_PROGRAM)
programa_pletinas = RDK.Item('ResetPletinas', ITEM_TYPE_PROGRAM)
programa_entrada = RDK.Item('ResetGiraQuesosEntrada', ITEM_TYPE_PROGRAM)

# Verificar si existen los programas
if not programa_giraquesos.Valid():
    RDK.ShowMessage("Error: No se encontró el programa 'ResetGiraQuesos'.")
    exit()
if not programa_pletinas.Valid():
    RDK.ShowMessage("Error: No se encontró el programa 'ResetPletinas'.")
    exit()
if not programa_entrada.Valid():
    RDK.ShowMessage("Error: No se encontró el programa 'ResetGiraQuesosEntrada'.")
    exit()

# Ejecutar los programas en secuencia
programa_giraquesos.RunProgram()
while programa_giraquesos.Busy():
    pass

programa_pletinas.RunProgram()
while programa_pletinas.Busy():
    pass

programa_entrada.RunProgram()
while programa_entrada.Busy():
    pass

RDK.ShowMessage("Todos los programas se ejecutaron correctamente.")
