

# mock della classe che dovrebbe controllare se il biglietto e' nel db
# e scrivere in questo l'orario di entrata/uscita

class dbAccess():

    def queryDb(self, numero):
        numeri_biglietti = ["123456", "654321", "7890", "001", "aaaa"]
        if numero in numeri_biglietti:
            return True
        else:
            return False