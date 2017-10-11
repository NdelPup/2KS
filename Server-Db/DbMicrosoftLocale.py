#coding:utf-8
import pyodbc
from time import strftime, localtime

cnxn = pyodbc.connect("Driver={SQL Server};SERVER=192.168.1.5;DATABASE=dbLocaleTornelli;UID=Tornello;PWD=Vmware1!")
cursor = cnxn.cursor()

class DatabaseConnection():

    def parseMessage(self, message):
        #funzione che legge il messaggio per ricavarne i dati per la query
        arr = message.split("-")
        ticket = str(arr[4]+"-"+arr[5])
        return ticket

    def checkTicket(self, message, tornello, gate):
        #funzione che controlla il biglietto
        #primo controllo di correttezza formale
        if len(message) != 29:
            self.writeError(tornello, gate, 1, message)
            return {"Result" : False, "Error" : 1}
            
        ticket = self.parseMessage(message)

        #controllo biglietto già letto
        try:
            #chiedo al db di contare quante sono le righe col numero del biglietto
            #in cui la data è not null, se >0 allora il biglietto è già passato
            count = cursor.execute("SELECT ID_Biglietto, Data_Ora  FROM Tabella_1 WHERE ID_Biglietto = ? \
            AND Data_Ora IS NOT NULL", message).rowcount
            if count != 0:
                #Error 2 = biglietto già usato
                self.writeError(tornello, gate, 2, message)
                return {"Result" : False, "Error" : 2}
        except Exception as e:
            print (e)
        
        try:
            cursor.execute("SELECT * FROM Tabella_1 WHERE ID_Biglietto = ?", message)
            result = cursor.fetchall()
            print message
            print result
            #biglietto buono
            if str(result) != "[]":
                self.writeRecord(message, tornello)
                return {"Result" : True}
            else:
                self.writeError(tornello, gate, 1, message)
                #Error 1 = invalid ticket
                return {"Result" : False, "Error" : 1}

        except Exception as e:
            print (e)

    def writeRecord(self, ticket, tornello):
        #funzione che registra le entrate
        try:
            currentTime = strftime("%d/%m/%Y %H:%M:%S", localtime())
            cursor.execute("UPDATE Tabella_1 SET ID_Tornello = ?, Data_Ora = ? \
            WHERE ID_Biglietto=?", tornello, currentTime, ticket)
            cursor.commit()
        except Exception as e:
            print (e)

    def writeError(self, tornello, gate, errorCode, errorReading):
        #funzione che scrive nella tabella degli errori
        try:
            cursor.execute("INSERT INTO Tabella_3(ID_Entrata, ID_Tornello, Lettura_Errore, ID_Errore) \
            VALUES(?, ?, ?, ?)", gate, tornello, errorReading, errorCode)
            cursor.commit()
        except Exception as e:
            print (e)

    def syncQuery(self):
        #funzione con query per sincronizzare il server, controlla solo la prima riga della tabella dei biglietti
        try:
            cursor.execute("SELECT TOP 1 ID_Biglietto FROM Tabella_1")
            result = cursor.fetchall()
            event = str(result)[4:13]
            arena = str(result)[14:18]
            return event, arena

        except Exception as e:
            print (e)

def main():
        
    con = DatabaseConnection()
    result = con.checkTicket("0000-0001-0001-0002-0000-0002", "0002", "0002")
    print result

if __name__ == '__main__':
    main()