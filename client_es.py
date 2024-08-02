import socket  # Importa el módulo de sockets para la comunicación en red
import threading  # Importa el módulo threading para manejar múltiples tareas simultáneamente
import time  # Importa el módulo time para manejar tiempos de espera

nombre_usuario = input("Ingrese su nombre de usuario: ")  # Solicita al usuario que ingrese su nombre de usuario

host = '127.0.0.1'  # Define la dirección IP del servidor (localhost)
puerto = 55566  # Define el puerto en el que el servidor escucha

# Crea un objeto socket para el cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Función para conectar al servidor
def conectar_al_servidor():
    try:
        cliente.connect((host, puerto))  # Intenta conectar al servidor
        #print("Conectado al servidor.")  # Imprime un mensaje indicando que la conexión fue exitosa
    except ConnectionRefusedError:
        print("Conexión rechazada, por favor asegúrese de que el servidor está en funcionamiento.")  # Imprime un mensaje si la conexión es rechazada
        exit()  # Sale del programa

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')  # Recibe un mensaje del servidor
            if mensaje == "@username":
                cliente.send(nombre_usuario.encode("utf-8"))  # Envía el nombre de usuario al servidor si se solicita
            else:
                print(mensaje)  # Imprime el mensaje recibido
        except ConnectionResetError:
            print("Conexión perdida, reconectando...")  # Imprime un mensaje si se pierde la conexión
            reconectar_al_servidor()  # Intenta reconectar al servidor
            break
        except Exception as e:
            print(f"Ocurrió un error: {e}")  # Imprime un mensaje de error si ocurre una excepción
            cliente.close()  # Cierra la conexión
            break

# Función para enviar mensajes al servidor
def escribir_mensajes():
    while True:
        try:
            mensaje = f"{nombre_usuario}: {input('')}"  # Prepara el mensaje con el nombre de usuario
            cliente.send(mensaje.encode('utf-8'))  # Envía el mensaje al servidor
        except Exception as e:
            print(f"Ocurrió un error al enviar el mensaje: {e}")  # Imprime un mensaje de error si ocurre una excepción
            cliente.close()  # Cierra la conexión
            break

# Función para reconectar al servidor en caso de pérdida de conexión
def reconectar_al_servidor():
    while True:
        try:
            time.sleep(5)  # Espera 5 segundos antes de intentar reconectar
            conectar_al_servidor()  # Intenta conectar al servidor
            # Vuelve a iniciar los hilos de recepción y envío de mensajes
            hilo_recibir = threading.Thread(target=recibir_mensajes)
            hilo_recibir.start()

            hilo_escribir = threading.Thread(target=escribir_mensajes)
            hilo_escribir.start()
            break
        except Exception as e:
            print(f"Intento de reconexión fallido: {e}")  # Imprime un mensaje si la reconexión falla
            continue

conectar_al_servidor()  # Conecta al servidor

# Inicia el hilo para recibir mensajes del servidor
hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

# Inicia el hilo para enviar mensajes al servidor
hilo_escribir = threading.Thread(target=escribir_mensajes)
hilo_escribir.start()
