import threading
import queue
import time
# Crear una cola
q = queue.Queue()

def producer():
    for i in range(10):
        q.put({str(i):i+2})
        
        print(f'Producido: {i}')
        time.sleep(1)

def consumer():
    while True:
        item = q.get()
        print(f'Consumido: {item}')
    

# Crear los hilos
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Iniciar los hilos
producer_thread.start()
consumer_thread.start()

# Esperar a que el productor termine
producer_thread.join()

# Enviar una señal de parada al consumidor


# Esperar a que el consumidor termine
consumer_thread.join()