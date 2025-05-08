from robodk.robolink import *
from robodk import mbox

ACTIVAR_MQTT = 'MQTT'

RDK = Robolink()

prevalorMQTT = RDK.getParam(ACTIVAR_MQTT)
valorMQTT = mbox('¿Quiere activar MQTT? (opciones: Si,No)', entry=prevalorMQTT)
if valorMQTT:
    RDK.setParam(ACTIVAR_MQTT, valorMQTT)
else:
    quit()