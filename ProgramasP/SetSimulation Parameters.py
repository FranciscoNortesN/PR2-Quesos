from robodk.robolink import *   # RoboDK API
from robodk.robodialogs import *
RDK = Robolink()

data = InputDialog('Configuración MQTT:', {
    'Activar MQTT:': True,
    'Introduce el broker:': '100.93.177.37',
    'Introduce el puerto:': 1883,
})

# Extraer los valores
integer_value = data['Enter an integer:']
float_value = data['Enter a float:']
boolean_value = data['Set a boolean:']
text_value = data['Enter text:']

# Dropdown: índice seleccionado y lista de opciones
dropdown_index = data['Select from a dropdown:'][0]

print(f"Integer: {integer_value}")
print(f"Float: {float_value}")
print(f"Boolean: {boolean_value}")
print(f"Text: {text_value}")
print(f"Dropdown selected: {dropdown_index}")