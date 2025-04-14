import socket
import threading

def receive_messages(sock, username):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg.startswith(f"{username}:"):
                print(f"\n🟢 {msg}")
            else:
                print(f"\n🔴 {msg}")
        except:
            break

def send_messages(sock):
    while True:
        msg = input()
        sock.sendall(msg.encode())
        print(f"\n🟢 {username}: {msg}")  # Mostra il tuo messaggio con pallino verde

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

username = input("Inserisci il tuo username: ")
client.sendall(username.encode())  # invia username al server

print("Connesso al server! Scrivi i tuoi messaggi:")

threading.Thread(target=receive_messages, args=(client, username), daemon=True).start()
send_messages(client)
