from FuncionesBase import *

SHOW_ERROR = True               # True para mostrar errores, False para no mostrar errores

""" Función para modificarle la velocidad a un robot. 
    La función comprueba que el robot existe.
    
    Recibe el nombre del robot, la velocidad lineal, la aceleración lineal, 
    la velocidad angular y la aceleración angular.
    
    Devuelve True si ha funcionado y False si no existe el robot."""
def setSpeed(robot, velLineal, accelLineal, velAngular, accelAngular):
    if robot:
        robot.setSpeed(velLineal, velAngular, accelLineal, accelAngular)
        return True
    else:
        return False

def moveTo(robot, obj, tipoMov = "MoveJ"):
    if robot and obj:
        if tipoMov == "MoveJ":
            robot.MoveJ(obj)
        elif tipoMov == "MoveL":
            robot.MoveL(obj)
        return True
    else:
        return None

def setPose(robot, pose):
    if robot:
        robot.setJoints(pose)
        return True
    else:
        return None
