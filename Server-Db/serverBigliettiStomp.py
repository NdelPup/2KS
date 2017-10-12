#coding:utf-8
import time
import sys
import stomp
from DbMicrosoftLocale import DatabaseConnection
import logging
from threading import *
import json

logging.basicConfig(level=logging.DEBUG)
#connessione al database
dbCheck = DatabaseConnection()
#semaforo
dbLock = Semaphore(1)
#connessione al broker
conn = stomp.Connection([('127.0.0.1', 61613)])
event = ""
arena = ""

class MyListener(stomp.ConnectionListener):
        
    def on_message(self, headers, message):
        #metodo che gestisce l'arrivo dei messaggi dai lettori
        global event
        global arena
        if message == "SYNC":
            t = Thread(target=syncDev, args=(headers.get("sender"),))
            t.start()
            #gate = syncDev(headers.get("sender"))
            #conn.send(body="SYNC", headers={"gate" : gate, "event" : event, "arena" : arena}, \
            #destination='/queue/lettore' + headers.get("sender"))
        if message == "EXIT":
            t = Thread(target=registerExit, args=(headers))
            t.start()
        else:
            t = Thread(target=checkTicket, args=(headers, message))
            t.start()
            #checkTicket(headers, message)
        
def checkTicket(headers, message):
    #metodo che controlla i ticket ricevuti dai lettori
    sender = headers.get("sender")
    gate = headers.get("gate")

    dbLock.acquire()
    check = dbCheck.checkTicket(message, sender, gate)
    dbLock.release()
    
    if check.get("Result") == True:
        conn.send(body="true", destination='/queue/lettore' + sender)
    elif check.get("Error") == 3:
        conn.send(body="false", headers={"error" : "3", "gate" : check.get("Gate")}, destination='/queue/lettore' + sender)
    elif check.get("Error") == 2:
        conn.send(body="false", headers={"error" : "2"}, destination='/queue/lettore' + sender)
    else:
        conn.send(body="false", headers={"error" : "1"}, destination='/queue/lettore' + sender)

def registerExit(headers):
    print "exit registered in DB uscita: " +headers.get("gate")+", tornello: "+headers.get("tornello")

def syncServer():
    #funzione che sincronizza il server
    global event
    global arena
    event, arena = dbCheck.syncQuery()

def syncDev(dev):
    #funzione che risponde alla richiesta di sincronizzazione del dev
    with open ("config.json") as config:
        data = json.load(config)
        gate = data.get(dev)
        #return gate
        conn.send(body="SYNC", headers={"gate" : gate, "event" : event, "arena" : arena}, \
            destination='/queue/lettore' + dev)

def main():
    #ciclo vita dello script
    syncServer()
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect('user1', 'user1', wait=True)
    conn.subscribe(destination='/queue/server', id=1, ack='auto')

    while True:
        time.sleep(2)

if __name__ == '__main__':
    main()