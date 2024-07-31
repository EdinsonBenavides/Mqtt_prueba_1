import paho.mqtt.client as mqtt
import json

# Configuración del broker
broker = "localhost"
port = 1883
topic = "agente1"

# Datos que queremos escribir en el archivo JSON
data = {
    "publicador": "admin",
    "state_optimizacion": True,
    "potencia_demandada":1150,
    "numero_de_agentes":6
}

# Escribir el archivo JSON
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

# Leer el archivo JSON
with open('data.json', 'r') as file:
    message = json.load(file)

# Convertir el diccionario a una cadena JSON
message_str = json.dumps(message)

# Crear una instancia del cliente
client = mqtt.Client()

try:
    # Conectarse al broker
    client.connect(broker, port, 60)
    # Publicar el mensaje
    client.publish(topic, message_str)
    print(f"Mensaje JSON publicado en {topic}: {message_str}")
except Exception as e:
    print(f"Error al conectar o publicar: {e}")
finally:
    # Desconectarse del broker
    client.disconnect()