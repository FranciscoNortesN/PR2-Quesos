from robodk.robolink import *  # Importamos la API de RoboDK
from robodk.robomath import *  # Importamos las herramientas matemáticas de RoboDK

# Conectarse al servidor de RoboDK
RDK = Robolink()

# Obtener el mecanismo de la cinta transportadora
pletina1 = RDK.Item('MecanismoPletina1', ITEM_TYPE_ROBOT)
pletina2 = RDK.Item('MecanismoPletina2', ITEM_TYPE_ROBOT)

if not pletina1.Valid():
    RDK.ShowMessage("Error: No se encontró un mecanismo llamado 'MecanismoPletina1'.")
    exit()
if not pletina2.Valid():
    RDK.ShowMessage("Error: No se encontró un mecanismo llamado 'MecanismoPletina2'.")
    exit()


# Definir las juntas iniciales (reset a 0)
juntas_iniciales_pletina_1 = [-90]  # Suponemos que la cinta tiene una sola articulación
juntas_iniciales_pletina_2 = [90]

# Establecer las juntas directamente sin movimiento
pletina1.setJoints(juntas_iniciales_pletina_1)
pletina2.setJoints(juntas_iniciales_pletina_2)
