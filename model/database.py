import mysql.connector
import json
import time

class database:
    connexion : dict = {}

    def __init__(self,host:str,user:str,password:str,database:str) -> None:
        self.connexion = {
            "host" : host,
            "user" : user,
            "password" : password,
            "database" : database
        }
        self.createDatabase()

    def createDatabase(self):
        print("[DATABASE] "+time.strftime("%x, %X,")+" Création de la base de donnée et de ses tables.")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                db.autocommit = True
                with db.cursor() as c:
                    try:
                        c.execute("""
                            CREATE TABLE IF NOT EXISTS `french`(
                                `ID` int(255) NOT NULL AUTO_INCREMENT,
                                `normandID` int(255),
                                `expression` varchar(255) NOT NULL,
                                PRIMARY KEY (`ID`)
                            );
                        """)
                        print("[DATABASE] "+time.strftime("%x, %X,")+" La table 'french' a été crée.")
                    except:
                        print("[DATABASE] "+time.strftime("%x, %X,")+" La table 'french' n'a pas pu être crée!")
                    
                    try:
                        c.execute("""
                            CREATE TABLE IF NOT EXISTS `normand`(
                                `ID` int(255) NOT NULL AUTO_INCREMENT,
                                `frenchID` int(255),
                                `expression` varchar(255) NOT NULL,
                                PRIMARY KEY (`ID`)
                            );
                        """)
                        print("[DATABASE] "+time.strftime("%x, %X,")+" La table 'normand' a été crée.")
                    except:
                        print("[DATABASE] "+time.strftime("%x, %X,")+" La table 'normand' n'a pas pu être crée!")

                    try:
                        c.execute("""
                            ALTER TABLE french ADD FOREIGN KEY (normandID) REFERENCES normand(ID);
                        """)
                        print("[DATABASE] "+time.strftime("%x, %X,")+" L'ID de la table 'normand' a été rajouté dans la colonne 'normandID' de la table 'french'")
                    except:
                        print("[DATABASE] "+time.strftime("%x, %X,")+" L'ID de la table 'normand' n'a pas pu être rajouté dans la colonne 'normandID' de la table 'french'")

                    try:
                        c.execute("""
                            ALTER TABLE normand ADD FOREIGN KEY (frenchID) REFERENCES french(ID);
                        """)
                        print("[DATABASE] "+time.strftime("%x, %X,")+" L'ID de la table 'french' a été rajouté dans la colonne 'frenchID' de la table 'normand'")
                    except:
                        print("[DATABASE] "+time.strftime("%x, %X,")+" L'ID de la table 'french' n'a pas pu être rajouté dans la colonne 'frenchID' de la table 'normand'")
            print("[DATABASE] "+time.strftime("%x, %X,")+" Création des tables terminées.")
        except:
            print("[DATABASE] "+time.strftime("%x, %X,")+" Impossible de se connecter à les tables.")

access = None

try:
    with open("model/database.json","r") as file:
            print("Fichier trouvé!")
            access = json.loads(file.read())
            file.close()
            print("Accès à la base de données récupérés!")
except:
    print("Fichier non trouvé!")
    access = None

DATABASE = database(access['host'],access['user'],access['password'],access['database'])
                
                

