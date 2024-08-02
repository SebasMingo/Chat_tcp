import socket  # Importa el módulo de sockets para la comunicación en red
import threading  # Importa el módulo threading para manejar múltiples conexiones simultáneamente

host = '127.0.0.1'  # Define la dirección IP del servidor (localhost)
puerto = 55566  # Define el puerto en el que el servidor escuchará

# Crea un objeto socket para el servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, puerto))  # Asocia el socket con la dirección y puerto definidos
servidor.listen()  # Pone el servidor en modo escucha
print(f"Servidor ejecutándose en {host}:{puerto}")  # Imprime un mensaje indicando que el servidor está en funcionamiento

clientes = []  # Lista para almacenar los sockets de los clientes conectados
nombres_de_usuarios = []  # Lista para almacenar los nombres de usuario de los clientes conectados

# Función para transmitir mensajes a todos los clientes conectados excepto el remitente
def transmitir(mensaje, _cliente=None):
    for cliente in clientes:  # Itera sobre todos los clientes conectados
        if cliente != _cliente:  # Si el cliente no es el remitente
            try:
                cliente.send(mensaje)  # Envía el mensaje al cliente
            except:
                eliminar_cliente(cliente)  # Si hay un error, elimina al cliente

# Función para eliminar un cliente de las listas y cerrar su conexión
def eliminar_cliente(cliente):
    if cliente in clientes:
        indice = clientes.index(cliente)  # Obtiene el índice del cliente en la lista
        clientes.remove(cliente)  # Elimina al cliente de la lista de clientes
        nombre_usuario = nombres_de_usuarios[indice]  # Obtiene el nombre de usuario del cliente
        nombres_de_usuarios.remove(nombre_usuario)  # Elimina el nombre de usuario de la lista
        print(f"{nombre_usuario} se ha desconectado.")  # Imprime un mensaje indicando que el cliente se ha desconectado
        transmitir(f"ChatBot: {nombre_usuario} ha dejado el chat.".encode('utf-8'))  # Notifica a los demás clientes que el usuario ha salido del chat
        cliente.close()  # Cierra la conexión del cliente

# Función para manejar mensajes recibidos de los clientes
def manejar_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)  # Recibe un mensaje del cliente
            if mensaje:
                transmitir(mensaje, cliente)  # Transmite el mensaje a los demás clientes
            else:
                eliminar_cliente(cliente)  # Si no se recibe mensaje, elimina al cliente
                break
        except:
            eliminar_cliente(cliente)  # Si hay un error, elimina al cliente
            break

# Función para aceptar y gestionar nuevas conexiones de clientes
def recibir_conexiones():
    while True:
        try:
            cliente, direccion = servidor.accept()  # Acepta una nueva conexión
            print(f"Conexión desde {direccion}")  # Imprime un mensaje indicando que se ha conectado un nuevo cliente

            cliente.send("@username".encode("utf-8"))  # Solicita el nombre de usuario del cliente
            nombre_usuario = cliente.recv(1024).decode('utf-8')  # Recibe el nombre de usuario del cliente
            clientes.append(cliente)  # Añade el socket del cliente a la lista de clientes
            nombres_de_usuarios.append(nombre_usuario)  # Añade el nombre de usuario a la lista de nombres

            print(f"{nombre_usuario} está ahora conectado con {direccion}")  # Imprime un mensaje indicando que el usuario se ha conectado
            transmitir(f"ChatBot: {nombre_usuario} se ha unido al chat.".encode("utf-8"), cliente)  # Notifica a los demás clientes que un nuevo usuario se ha unido al chat
            cliente.send("Conectado al servidor".encode("utf-8"))  # Envía un mensaje de confirmación al cliente

            hilo = threading.Thread(target=manejar_mensajes, args=(cliente,))  # Crea un nuevo hilo para manejar los mensajes del cliente
            hilo.start()  # Inicia el hilo

        except Exception as e:
            print(f"Error al aceptar una nueva conexión: {e}")  # Imprime un mensaje de error si falla la conexión

recibir_conexiones()  # Inicia la función para recibir conexiones
