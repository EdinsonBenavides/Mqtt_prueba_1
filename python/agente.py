import paho.mqtt.client as mqtt
import json
import threading
import time
import signal

# Configuración del broker
broker = "localhost"
port = 1883
topic_public = "test/topic"
topic_suscrib = "agente1"

# Datos que queremos enviar como mensaje JSON
data = {
    "sensor": "temperature",
    "value": 23.5
}

# Bandera para controlar el bucle de publicación
publish_flag = True

def signal_handler(sig, frame):
    global publish_flag
    print("Deteniendo el publicador...")
    publish_flag = False

# Configurar la señal para capturar SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Función de publicación
def publish():
    global publish_flag
    # Convertir el diccionario a una cadena JSON
    message_str = json.dumps(data)

    # Crear una instancia del cliente
    client = mqtt.Client()

    try:
        # Conectarse al broker
        client.connect(broker, port, 60)
        if publish_flag:
            # Publicar el mensaje
            client.publish(topic_public, message_str)
            print(f"Mensaje JSON publicado en {topic_public}: {message_str}")
            time.sleep(5)  # Esperar 5 segundos antes de publicar nuevamente
    except Exception as e:
        print(f"Error al conectar o publicar: {e}")
    finally:
        # Desconectarse del broker
        client.disconnect()
        print("Cliente MQTT desconectado")

# Función de suscripción
def subscribe():
    # Función callback cuando se recibe un mensaje
    def on_message(client, userdata, message):
        try:
            # Convertir el payload a un diccionario
            data = json.loads(message.payload.decode())
            print(f"Mensaje recibido en {message.topic}: {type(data)}")

            # Escribir el mensaje recibido en un archivo JSON
            with open('received_messages.json', 'w') as file:
                json.dump(data, file)
                file.write('\n')  # Escribir nueva línea para separar los mensajes

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
        client.subscribe(topic_suscrib)
        # Mantenerse en escucha
        client.loop_forever()
    except Exception as e:
        print(f"Error al conectar o suscribir: {e}")

# Crear hilos para publicar y suscribir
publish_thread = threading.Thread(target=publish)
subscribe_thread = threading.Thread(target=subscribe)

# Iniciar hilos
publish_thread.start()
subscribe_thread.start()

# Esperar a que los hilos terminen
publish_thread.join()
subscribe_thread.join()