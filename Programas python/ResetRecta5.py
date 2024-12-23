from robodk.robolink import *  # Importamos la API de RoboDK
from robodk.robomath import *  # Importamos las herramientas matemáticas de RoboDK

# Conectarse al servidor de RoboDK
RDK = Robolink()

# Obtener el mecanismo de la cinta transportadora
cinta = RDK.Item('MecanismoRecta5', ITEM_TYPE_ROBOT)

if not cinta.Valid():
    RDK.ShowMessage("Error: No se encontró un mecanismo llamado 'MecanismoRecta5'.")
    exit()

# Definir las juntas iniciales (reset a 0)
juntas_iniciales = [0]  # Suponemos que la cinta tiene una sola articulación

# Establecer las juntas directamente sin movimiento
cinta.setJoints(juntas_iniciales)
