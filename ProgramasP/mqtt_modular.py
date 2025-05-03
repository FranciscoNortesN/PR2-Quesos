import paho.mqtt.client as mqtt
from paho.mqtt.client import topic_matches_sub
import threading
import uuid

_callbacks = []
_client = None
_lock = threading.Lock()
_topic_prefix = ""

BROKER="100.93.177.37"

def set_prefix(prefix):
    """Define un prefijo global para los topics, como 'RoboDK/'."""
    global _topic_prefix
    _topic_prefix = prefix.strip("/")
    if _topic_prefix:
        _topic_prefix += "/"

def _apply_prefix(topic):
    """Aplica el prefijo configurado al topic."""
    return _topic_prefix + topic.strip("/")

def register_callback(sub_topic, callback):
    """Registra una función callback asociada a un subtopic."""
    with _lock:
        full_topic = _apply_prefix(sub_topic)
        _callbacks.append((full_topic, callback))

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    with _lock:
        for sub_topic, callback in _callbacks:
            if topic_matches_sub(sub_topic, topic):
                threading.Thread(target=callback, args=(topic, payload), daemon=True).start()

def setup_mqtt(client_id=None, broker=BROKER, port=1883):
    """Inicia el cliente MQTT, se suscribe automáticamente a {prefix}#."""
    if client_id is None:
        client_id = str(uuid.uuid4())
    global _client
    _client = mqtt.Client(client_id=client_id)
    _client.on_message = on_message
    _client.connect(broker, port)
    _client.loop_start()

    # Suscripción general a todos los topics bajo el prefijo
    if _topic_prefix:
        _client.subscribe(_topic_prefix + "#")

    print(f"Conectado a {broker}:{port} con ID {client_id}. Suscrito a {_topic_prefix}#")


def publish(topic, message, qos=0, retain=False):
    """Publica un mensaje en un topic con el prefijo aplicado."""
    if _client:
        _client.publish(_apply_prefix(topic), message, qos, retain)
    else:
        raise RuntimeError("MQTT no está inicializado. Llama a setup_mqtt primero.")
