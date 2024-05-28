import socket
import threading

host = '127.0.0.1'  #Creación variable con nuestro localhost
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # definiendo un socket   TCP
server.bind((host,port)) # Pasando datos de conexión al servidor 
server.listen() #servidor escuchando peticiones
print(f"Servidor encendido {host}:{port}")

clients = [] # lista para almacenar clientes
usernames = [] # lista para almacenar usuarios

#
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024) # maximo de caracteres a recibir en el mensaje
            broadcast(message,client)
        except:
            index = clients.index(client) 
            username = usernames[index]
            message = f"Chat :{username} desconectado".encode('utf-8') # utilizamos el formato utf-8 de codificación para el mensaje
            broadcast(message,client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def receive_connection():
    while True:
        client, address = server.accept() # guaradaremos en estas variables quien se conecto y su ip 

        client.send("username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        clients.append(client) #guardamos clientes
        usernames.append(username)# guardamos usernames

        print(f"{username} esta conectado con {str(address)}") #utilizamos la función str para que nos pueda imprimir la dirección 

        message = f"Chat: {username} esperando mensaje ".encode('utf-8')

        broadcast(message,client)
        client.send("Conectado al servidor".encode('utf-8'))

        thread = threading.Thread(target=handle_messages, args=(client,)) 
        thread.start()

receive_connection() 