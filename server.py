import socket
import threading

clients = []  # lista di socket
usernames = {}  # mappa che associa username ai socket


def salva_messaggio_log(msg):
    with open("chat_log.txt", "a", encoding="utf-8") as f: # "a" significa aggiungi alla fine del file (append), con codifica utf
        f.write(msg + "\n")


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except:
                pass  # serve ad evitare crash se un client si disconnette inaspettatamente

# Gestione client
def handle_client(client_socket, address):
    print(f"Connesso: {address}")

    try:
        # Ricevi username
        username = client_socket.recv(1024).decode() #legge i dati inviati dal client (nome di massimo 1024byte) e converte i dati in una stringa
        usernames[client_socket] = username 
        clients.append(client_socket)

        # Invia cronologia della chat
        try:
            with open("chat_log.txt", "r", encoding="utf-8") as f: # "r" sta per read
                cronologia = f.read()
                if cronologia.strip():
                    client_socket.sendall(f"--- Cronologia chat ---\n{cronologia}".encode())
        except FileNotFoundError:
            pass  # Ignora l'errore per evitare che crashi tutto

        # Notifica di ingresso
        welcome_msg = f"{username} si è unito alla chat!"
        broadcast(welcome_msg, client_socket)
        salva_messaggio_log(welcome_msg)

        # Loop ricezione messaggi
        while True: #Continua a ricevere i messaggi finchè il client non si disconnette
            message = client_socket.recv(1024)
            if not message:
                break # Se si disconnette il client esce dal loop
            formatted_message = f"{username}: {message.decode()}"
            broadcast(formatted_message, client_socket)
            salva_messaggio_log(formatted_message)

    except:
        pass # In caso di errore non fa nulla

    print(f"Disconnesso: {address}")
    clients.remove(client_socket)
    broadcast(f"{usernames.get(client_socket, 'Un utente')} ha lasciato la chat.", client_socket)
    salva_messaggio_log(f"{usernames.get(client_socket, 'Un utente')} ha lasciato la chat.")
    usernames.pop(client_socket, None) # pop rimuove il nome utente dal client
    client_socket.close() 

# Avvio server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crea un nuovo soket tcp
server.bind(('0.0.0.0', 12345)) # 0.0.0.0 significa che il server accetta connessioni da qualsiasi IP
server.listen()

print("Server in ascolto su porta 12345...")

while True:
    client_socket, addr = server.accept() #Accetta òla connessione in i ngresso
    thread = threading.Thread(target=handle_client, args=(client_socket, addr)) # Crea un nuovo thread per il client in modo che il server puo continuare a ricevere nuove connessioni
    thread.start() # Avvia il thread
