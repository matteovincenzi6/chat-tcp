# Introduzione ai Socket

I socket sono punti di connessione per le comunicazioni di rete che permettono a programmi di comunicare, sia sulla stessa macchina che tra computer distanti. Funzionano in modo simile ai file, con operazioni di apertura, lettura, scrittura e chiusura. Ogni socket comprende:

- **Indirizzo IP**: identifica un dispositivo nella rete  
- **Numero di Porta**: identifica uno specifico processo sulla macchina

---

## Il Modello Client-Server

In questo paradigma, un client invia richieste a un server che fornisce il servizio desiderato:

1. Il **server** crea un socket con `bind()` e si mette in ascolto con `listen()`
2. Il **client** crea un socket e si connette con `connect()`
3. Dopo lo scambio di dati, la connessione viene chiusa

---

## Protocolli UDP e TCP

| Caratteristica     | UDP                        | TCP                        |
|--------------------|----------------------------|----------------------------|
| Connessione        | Non orientato alla connessione | Orientato alla connessione |
| Affidabilità       | Inaffidabile               | Affidabile                 |
| Ordine             | Non garantito              | Garantito                  |
| Trasferimento      | Datagrammi                 | Flusso di byte             |
| Velocità           | Maggiore                   | Minore                     |
| Uso tipico         | Streaming, Giochi, DNS     | Web, Email, File           |


# Chat Client-Server in Python

Questa applicazione permette di creare una chat testuale multiclient, in cui più utenti possono scambiarsi messaggi in tempo reale. Il sistema è strutturato utilizzando un modello client-server, dove il server gestisce le connessioni tra i client e la comunicazione dei messaggi. La parte client include un'interfaccia grafica realizzata con Tkinter, mentre il server gestisce le connessioni multiple tramite threading.

## Funzionalità

- **Chat Multiclient**: Più utenti possono connettersi al server e scambiarsi messaggi in tempo reale. Il server gestisce tutte le connessioni in modo indipendente, permettendo a ciascun client di interagire con gli altri senza interruzioni.
  
- **Comunicazione in Tempo Reale**: I client inviano messaggi al server, che poi li distribuisce a tutti gli altri client connessi. I messaggi vengono visualizzati in tempo reale nell'interfaccia grafica di ogni client.

- **Gestione delle Connessioni**: Il server è in grado di gestire più connessioni contemporaneamente grazie all'uso del **threading**. Ogni client viene gestito da un thread separato, evitando blocchi o rallentamenti del server.

- **Persistenza dei Messaggi**: Ogni messaggio inviato viene salvato su un file di log (`chat_log.txt`). Questo permette di conservare la cronologia della chat e consente anche ai nuovi client di ricevere la cronologia dei messaggi quando si connettono al server.

- **Interfaccia Grafica**: Il client include una semplice interfaccia grafica (GUI) creata con Tkinter, che permette agli utenti di inviare e ricevere messaggi in modo intuitivo.

## Come Funziona

1. **Avvio del Server**: 
   Il server gestisce tutte le connessioni in entrata. Utilizza un **socket TCP** per ascoltare sulla porta `12345` e stabilire connessioni con i client. Ogni volta che un client si connette, viene creato un nuovo thread per gestirlo, permettendo al server di supportare più client simultaneamente.

2. **Avvio del Client**: 
   Ogni client, una volta avviato, si connette al server e invia un nome utente. Il client visualizza l'interfaccia grafica che permette di scrivere messaggi e riceverli in tempo reale. Ogni messaggio inviato viene poi propagato a tutti gli altri client connessi.

3. **Gestione dei Messaggi**: 
   Il server riceve i messaggi dai client e li invia a tutti gli altri client. Inoltre, i messaggi vengono salvati in un file di log (`chat_log.txt`), per garantire la persistenza della cronologia della chat.

## Struttura del Codice

- **Client** (`client.py`):
  - Il client utilizza **Tkinter** per creare un'interfaccia grafica che consente di inviare e ricevere messaggi.
  - Si connette al server tramite un **socket TCP**, inviando i messaggi e ricevendo quelli inviati dagli altri client.
  - I messaggi vengono visualizzati nell'interfaccia grafica con colori distintivi per i messaggi inviati dall'utente e quelli ricevuti.

- **Server** (`server.py`):
  - Il server utilizza un **socket TCP** per ascoltare le connessioni in entrata sulla porta `12345`.
  - Quando un client si connette, viene avviato un nuovo thread per gestire la comunicazione con quel client, permettendo al server di gestire più connessioni simultaneamente.
  - Ogni messaggio ricevuto viene trasmesso a tutti i client connessi e salvato nel file di log (`chat_log.txt`).


