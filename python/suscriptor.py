import paho.mqtt.client as mqtt
import json

# Configuración del broker
broker = "localhost"
port = 1883
topic = "test/topic"

# Función callback cuando se recibe un mensaje
def on_message(client, userdata, message):
    try:
        # Convertir el payload a un diccionario
        data = json.loads(message.payload.decode())
        print(f"Mensaje recibido en {message.topic}: {data}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")

# Crear una instancia del cliente
client = mqtt.Client()

try:
    # Asignar la función callback
    client.on_message = on_message
    # Conectarse al broker
    client.connect(broker, port, 60)
    # Suscribirse al tema
    client.subscribe(topic)
    # Mantenerse en escucha
    client.loop_forever()
except Exception as e:
    print(f"Error al conectar o suscribir: {e}")