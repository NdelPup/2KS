import time
import sys
import stomp
from ledscript import led
import socket
import logging

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
        print "connected"
        syncronize()

def syncronize():
    #funzione che invia al server la richiesta di sincronizzazione
    conn.send(body="SYNC", destination='/queue/server', headers = { "sender" : "0002"})

def messageParser(connection):
    #funzine che riceve l'input della telecamera e chiama la funzione che lo legge
    BUFFER_SIZE = 128  
    while True:
        data = connection.recv(BUFFER_SIZE)
        if not data: break
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

    if tickArena == arena and tickEvent == event and tickGate == gate:
        conn.send(body=ticket, destination='/queue/server', headers = { "sender" : "0002", "gate" : gate})
    else:
        ledController.led_rosso()

def ledStart():
    #funzione che illumina i led all'avvio
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

def main():
    #funzione main col ciclo di vita dello script
    ledStart()
    stompConnection()        
    lifeCycle()
    conn.disconnect()
    ledController.led_bianco_off()

if __name__ == '__main__':
    main()