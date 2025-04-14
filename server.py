import socket
import threading

clients = []  # lista di socket
usernames = {}  # mappa socket -> username

# 🔹 Funzione per salvare i messaggi in un file
def salva_messaggio_log(msg):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# 🔹 Funzione per inviare un messaggio a tutti i client tranne il mittente
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except:
                pass  # Evita crash se un client si disconnette inaspettatamente

# 🔹 Gestione client
def handle_client(client_socket, address):
    print(f"Connesso: {address}")

    try:
        # Ricevi username
        username = client_socket.recv(1024).decode()
        usernames[client_socket] = username
        clients.append(client_socket)

        # 🔸 Invia cronologia della chat
        try:
            with open("chat_log.txt", "r", encoding="utf-8") as f:
                cronologia = f.read()
                if cronologia.strip():
                    client_socket.sendall(f"--- Cronologia chat ---\n{cronologia}".encode())
        except FileNotFoundError:
            pass  # Nessuna chat salvata ancora

        # 🔸 Notifica di ingresso
        welcome_msg = f"{username} si è unito alla chat!"
        broadcast(welcome_msg, client_socket)
        salva_messaggio_log(welcome_msg)

        # 🔸 Loop ricezione messaggi
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            formatted_message = f"{username}: {message.decode()}"
            broadcast(formatted_message, client_socket)
            salva_messaggio_log(formatted_message)

    except:
        pass

    print(f"Disconnesso: {address}")
    clients.remove(client_socket)
    broadcast(f"{usernames.get(client_socket, 'Un utente')} ha lasciato la chat.", client_socket)
    salva_messaggio_log(f"{usernames.get(client_socket, 'Un utente')} ha lasciato la chat.")
    usernames.pop(client_socket, None)
    client_socket.close()

# 🔸 Avvio server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen()

print("Server in ascolto su porta 12345...")

while True:
    client_socket, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
