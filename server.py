import socket
import threading

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.sendall(message)

def handle_client(client_socket, address):
    print(f"Connesso: {address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break
    clients.remove(client_socket)
    client_socket.close()
    print(f"Disconnesso: {address}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # ascolta su tutte le interfacce di rete
server.listen()

print("Server in ascolto su porta 12345...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
