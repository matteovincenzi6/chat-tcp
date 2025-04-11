import socket
import threading

clients = []  # lista di socket
usernames = {}  # mappa socket -> username

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.sendall(message.encode())

def handle_client(client_socket, address):
    print(f"Connesso: {address}")

    try:
        # ricevi l'username appena connesso
        username = client_socket.recv(1024).decode()
        usernames[client_socket] = username
        welcome_msg = f"{username} si è unito alla chat!"
        broadcast(welcome_msg, client_socket)

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            formatted_message = f"{usernames[client_socket]}: {message.decode()}"
            broadcast(formatted_message, client_socket)

    except:
        pass

    print(f"Disconnesso: {address}")
    clients.remove(client_socket)
    broadcast(f"{usernames.get(client_socket, 'Un utente')} ha lasciato la chat.", client_socket)
    usernames.pop(client_socket, None)
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen()

print("Server in ascolto su porta 12345...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
