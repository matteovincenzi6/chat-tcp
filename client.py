import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, master): # costruttore della classe, master è la finestra proncipale di tkinter
        self.master = master
        self.master.title("Chat Client")
        self.master.configure(bg="#2b2b2b")

        self.chat_box = scrolledtext.ScrolledText( # crea un widget di testo scrolabile
            master, state='disabled', bg="#1e1e1e", fg="#dcdcdc",
            font=("Segoe UI", 10), wrap=tk.WORD, relief=tk.FLAT
        )
        self.chat_box.pack(padx=12, pady=12, fill=tk.BOTH, expand=True)

        self.chat_box.tag_config('self', foreground="#4fc3f7")   # Messaggi propri (blu chiaro)
        self.chat_box.tag_config('other', foreground="#ffffff")  # Messaggi altrui (bianco)
        self.chat_box.tag_config('error', foreground="#ff5252")  # Messaggi di errore (rosso)

        self.bottom_frame = tk.Frame(master, bg="#2b2b2b")
        self.bottom_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.msg_entry = tk.Entry(
            self.bottom_frame, bg="#333333", fg="#ffffff",
            font=("Segoe UI", 10), relief=tk.FLAT
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.bottom_frame, text="Invia", command=self.send_message,
            bg="#007acc", fg="#ffffff", font=("Segoe UI", 10, "bold"),
            activebackground="#005f99", activeforeground="#ffffff",
            relief=tk.FLAT, padx=10, pady=2
        )
        self.send_button.pack(side=tk.RIGHT)






        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea un socket 
        self.sock.connect(('127.0.0.1', 12345)) # si connette al server in ascolto sulla porta 1234 (127.0.0.1 è il local host)

        self.username = simpledialog.askstring("Username", "Inserisci il tuo username:", parent=self.master)
        self.sock.sendall(self.username.encode()) # invia l'username appena chiesto al server

        threading.Thread(target=self.receive_messages, daemon=True).start() # avvia un thread separato per poter ricevere i messaffi dal server senza bloiccare la GUI

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.sock.sendall(msg.encode())
                self.display_message(f"🟢 {self.username}: {msg}", sender='self')
                self.msg_entry.delete(0, tk.END)
                self.master.after(10, lambda: self.msg_entry.focus())
            except Exception as e:
                self.display_message(f"Errore nell'invio: {e}", sender='error')

    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if msg:
                    if msg.startswith(f"{self.username}:"):
                        self.display_message(f"🟢 {msg}", sender='self')
                    else:
                        self.display_message(f"🔴 {msg}", sender='other')
            except:
                break

    def display_message(self, msg, sender='other'):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, f"{msg}\n", sender)
        self.chat_box.yview(tk.END)
        self.chat_box.config(state='disabled')

# Avvio finestra Tkinter
root = tk.Tk()
client = ChatClient(root)
root.mainloop()
