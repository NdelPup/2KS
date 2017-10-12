#encoding=utf-8
import time
import sys
import stomp
from ledscript import led
import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG)
#connessione al broker
conn = stomp.Connection([('192.168.1.2', 61613)])
#istanza classe led
ledController = led()
#socket localhost per comunicare con lo script che legge i qrcode 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 55555))
sock.listen(1)
#dati da salvare per il controllo dei biglietti
gate = ""
arena = ""
event = ""
#variabile "spia" che riflette lo stato del tornello aperto/chiuso
isOpen = False

class MyListener(stomp.ConnectionListener):

    #classe listener prevista dalla documentazione di stomppy
    
    def on_error(self, headers, message):
        #funzione chiamata in caso di messaggio di errore dal broker (errore DEL broker)
        ledController.led_giallo_on()
        time.sleep(0.5)
        ledController.led_giallo_off()

    def on_message(self, headers, message):
        #funzione chiamata quando arriva un messaggio dal broker
        if message == "true":
            #led verde
            ledController.led_verde()
            open()
        elif message == "SYNC":
            global gate
            global arena
            global event
            gate = headers.get("gate")
            arena = headers.get("arena")
            event = headers.get("event")
        else:
            #led rosso
            ledController.led_rosso()

    def on_connected(self, headers, body):
        #funzione chiamata alla connessione col broker
        syncronize()

def syncronize():
    #funzione che invia al server la richiesta di sincronizzazione
    conn.send(body="SYNC", destination='/queue/server', headers = { "sender" : "0002"})

def messageParser(connection):
    #funzine che riceve l'input dal socket e decide cosa fare
    global isOpen
    BUFFER_SIZE = 128  
    while True:
        data = connection.recv(BUFFER_SIZE)
        if not data: break
        #se l'input è dal sensore
        if str(data) == "SENSOR":
            if isOpen:
                #se il tornello è aperto lo chiude, serve per chiudere il tornello
                #in sicurezza quando qualcuno entra
                close()
            else:
                #se è chiuso lo apre, aspetta e poi lo chiude
                #abbiamo utilizzato sleep anziché aspettare che il cliente entri (come sopra)
                #perché abbiamo solo un sensore a disposizione per il modello
                #avendo due sensori (uno prima ed uno dopo il braccio) avremmo fatto come sopra
                #in questo modo riusciamo anche a distinguere se si tratta di un'entrata o di un'uscita
                #visto che la fotcellula è sollecitata senza che il tornello sia aperto
                open()
                time.sleep(2)
                close()
                conn.send(body="EXIT", destination='/queue/server', headers = { "sender" : "0002", "gate" : gate})
        else:
            checkTicket(data[:(len(data)-1)])

def lifeCycle():
    #funzione che resta in ascolto per input dallo script che legge i qr code
    global sock
    while True:
        connection, addr = sock.accept()
        messageParser(connection)
        connection.close()
        
def stompConnection():
    #funzione di connessione al broker
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect('user1', 'user1', wait=True)
    conn.subscribe(destination='/queue/lettore0002', id=0, ack='auto')

def checkTicket(ticket):
    #funzione controllo ticket
    global gate
    global arena
    global event
    tickEvent = ticket[0:9]
    tickArena = ticket.split("-")[2]
    tickGate = ticket.split("-")[3]
    #controllo gate, arena ed evento siano giusti prima di inviare richiesta al server
    if tickArena == arena and tickEvent == event and tickGate == gate:
        conn.send(body=ticket, destination='/queue/server', headers = { "sender" : "0002", "gate" : gate})
    else:
        ledController.led_rosso()

def ledStart():
    #funzione che illumina i led all'avvio
    #serve a vedere che il led funzionano
    ledController.led_verde_on()
    time.sleep(0.03)
    ledController.led_rosso_on()
    time.sleep(0.03)
    ledController.led_giallo_on()
    time.sleep(0.03)
    ledController.led_bianco_on()
    time.sleep(0.03)
    ledController.led_verde_off()
    ledController.led_rosso_off()
    ledController.led_giallo_off()

def open():
    #metodo che apre il tornello
    global isOpen
    print "open"
    isOpen = True

def close():
    #metodo che chiude il tornello
    global isOpen
    print "close"
    isOpen = False

def main():
    #funzione main col ciclo di vita dello script
    ledStart()
    stompConnection()        
    lifeCycle()
    conn.disconnect()
    ledController.led_bianco_off()

if __name__ == '__main__':
    main()