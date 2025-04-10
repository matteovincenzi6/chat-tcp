import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print("\n" + msg)
        except:
            break

def send_messages(sock):
    while True:
        msg = input()
        sock.sendall(msg.encode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

print("Connesso al server! Scrivi i tuoi messaggi:")

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
send_messages(client)
