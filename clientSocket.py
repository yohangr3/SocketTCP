import socket
import threading

host = '127.0.0.1'
port = 5555
username = input("Nombre de usuario: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive_message():
    while True:

        try:
            message = client.recv(1024).decode('utf-8')

            if message == "username":
                client.send(username.encode('utf-8'))
            else:
                print(message)    
        except:
            print("Error!!")
            client.close()
            break

def write_message():
    while True:
        message = f"{username}: {input('')}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()