import mysql.connector
import json
import time

class database:
    connexion : dict = {}

    def __init__(self,host:str,user:str,password:str,database:str) -> None: #Initialise la base de donnée
        self.connexion = {
            "host" : host,
            "user" : user,
            "password" : password,
            "database" : database
        }
        self.createDatabase()

    def createDatabase(self): #Création de la base de donnée et de ses tables
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][CREATEDATABASE] {currentTime} Création de la base de donnée et de ses tables.")
        
        try:
            with mysql.connector.connect(**self.connexion) as db:
                db.autocommit = True
                with db.cursor() as c:
                    
                    try: #Créer la table french
                        c.execute("""
                            CREATE TABLE IF NOT EXISTS `french`(
                                `ID` int(255) NOT NULL AUTO_INCREMENT,
                                `normandID` int(255) DEFAULT NULL,
                                `word` varchar(255) NOT NULL,
                                PRIMARY KEY (`ID`)
                            );
                        """)
                        print(f"[DATABASE][CREATEDATABASE] {currentTime} La table 'french' a été crée.")
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")
                    
                    try: #Créer la table normand
                        c.execute("""
                            CREATE TABLE IF NOT EXISTS `normand`(
                                `ID` int(255) NOT NULL AUTO_INCREMENT,
                                `frenchID` int(255) DEFAULT NULL,
                                `word` varchar(255) NOT NULL,
                                PRIMARY KEY (`ID`)
                            );
                        """)
                        print(f"[DATABASE][CREATEDATABASE] {currentTime} La table 'normand' a été crée.")
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")

                    try: #Ajoutes à la colonne normandID une clé étrangère de la table french
                        c.execute("""
                            ALTER TABLE french
                            ADD CONSTRAINT fk_french_normand_id
                            FOREIGN KEY (normandID) REFERENCES normand(ID)
                        """)
                        print(f"[DATABASE][CREATEDATABASE] {currentTime} La clé étrangère 'fk_french_normand_id' a été liée à la colonne normandID de la table french.")
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")

                    try: #Ajoutes à la colonne frenchID une clé étrangère de la table normand
                        c.execute("""
                            ALTER TABLE normand
                            ADD CONSTRAINT fk_normand_french_id
                            FOREIGN KEY (frenchID) REFERENCES french(ID)
                        """)
                        print(f"[DATABASE][CREATEDATABASE] {currentTime} La clé étrangère 'fk_normand_french_id' a été liée à la colonne frenchID de la table normand.")
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")

            print(f"[DATABASE][CREATEDATABASE] {currentTime} Création des tables terminées.")
            db.close()

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            db.close()

    def inTable(self,wordFrench:str,wordNormand:str): #Vérifies si les mots existent dans les tables
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][INTABLE] {currentTime} Vérification du mot {wordFrench} dans la table 'french'.")

        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    try: #Récupères la donnée dans la colonne word de la table french
                        c.execute(f"""
                            SELECT word
                            FROM french
                            WHERE EXISTS (
                                SELECT word
                                FROM french
                                WHERE word = '{wordFrench}'
                            )
                        """)
                        result = c.fetchmany(1)

                        if (len(result) > 0): 
                            print(f"[DATABASE][INTABLE] {currentTime} le mot {wordFrench} est présent dans la table 'french'.")
                            return True
                        else:
                            print(f"[DATABASE][INTABLE] {currentTime} le mot {wordFrench} n'est pas présent dans la table 'french'.")
                    except mysql.connector.Error as err:
                        error1 = str(err)
                        db.close()
                        print(f"[DATABSE][INTABLE] {currentTime} {error1}")
                        return True

                    try: #Récupères la donnée dans la colonne word de la table normand
                        c.execute(f"""
                            SELECT word
                            FROM normand
                            WHERE EXISTS (
                                SELECT word
                                FROM normand
                                WHERE word = '{wordNormand}'
                            )
                        """)
                        result = c.fetchmany(1)

                        if (len(result) > 0): 
                            print(f"[DATABASE][INTABLE] {currentTime} le mot {wordNormand} est présent dans la table 'normand'.")
                            return True
                        else:
                            print(f"[DATABASE][INTABLE] {currentTime} le mot {wordNormand} n'est pas présent dans la table 'normand'.")
                    except mysql.connector.Error as err:
                        error1 = str(err)
                        db.close()
                        print(f"[DATABSE][INTABLE] {currentTime} {error1}")
                        return True
                    
                    return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            db.close()
            
    def addWord(self,wordFrench:str,wordNormand:str): #Ajoutes des mots dans la base de donnée
        currentTime = time.strftime("%x-%X")

        if (self.inTable(wordFrench,wordNormand) == False):
            print(f"[DATABASE][ADDWORD] {currentTime} Ajout du mot français {wordFrench} et du mot normand {wordNormand} dans la base de données.")
        else:
            print(f"[DATABASE][ADDWORD] {currentTime} Les mots {wordFrench} et {wordNormand} sont déjà dans la base de donnée.")
            return 

        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    #Ajoutes le mot français dans la table 'french'
                    print(f"[DATABASE][ADDWORD] {currentTime} INSERT INTO french (word) VALUES ('{wordFrench}')")
                    try:
                        c.execute(f"INSERT INTO french (word) VALUES ('{wordFrench}')")
                        db.commit()
                        print(f"[DATABASE][ADDWORD] {currentTime} COMMIT effectué!")
                    except mysql.connector.Error as err:
                        db.close()
                        error1 = str(err)
                        print(f"[DATABSE][ADDWORD] {currentTime} {error1}")
                    
                    #Ajoutes le mot normand dans la table 'normand'
                    print(f"[DATABASE][ADDWORD] {currentTime} INSERT INTO normand (expression) VALUES ('{wordNormand}')")
                    try:
                        c.execute(f"INSERT INTO normand (word) VALUES ('{wordNormand}')")
                        db.commit()
                        print(f"[DATABASE][ADDWORD] {currentTime} COMMIT effectué!")
                    except mysql.connector.Error as err:
                        db.close()
                        error1 = str(err)
                        print(f"[DATABSE][ADDWORD] {currentTime} {error1}")

                    #Modifies la colonne normandID du mot français qui est lié
                    print(f"[DATABASE][ADDWORD] {currentTime} UPDATE french SET normandID = (SELECT ID FROM normand WHERE word = '{wordNormand}') WHERE word = '{wordFrench}'")
                    try:
                        c.execute(f"UPDATE french SET normandID = (SELECT ID FROM normand WHERE word = '{wordNormand}') WHERE word = '{wordFrench}'")
                        db.commit()
                        print(f"[DATABASE][ADDWORD] {currentTime} COMMIT effectué!")
                    except mysql.connector.Error as err:
                        db.close()
                        error1 = str(err)
                        print(f"[DATABSE][ADDWORD] {currentTime} {error1}")
                    
                    #Modifies la colonne frenchID du mot normand qui est lié
                    print(f"[DATABASE][ADDWORD] {currentTime} UPDATE normand SET frenchID = (SELECT ID FROM french WHERE word = '{wordFrench}') WHERE word = '{wordNormand}'")
                    try:
                        c.execute(f"UPDATE normand SET frenchID = (SELECT ID FROM french WHERE word = '{wordFrench}') WHERE word = '{wordNormand}'")
                        db.commit()
                        print(f"[DATABASE][ADDWORD] {currentTime} COMMIT effectué!")
                    except mysql.connector.Error as err:
                        db.close()
                        error1 = str(err)
                        print(f"[DATABSE][ADDWORD] {currentTime} {error1}")
            print(f"[DATABASE][ADDWORD] {currentTime} Les mots {wordFrench} et {wordNormand} ont été rajoutés dans les tables.")
            db.close()

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            db.close()

    def removeWord(self,ID):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    c.execute(f"SET FOREIGN_KEY_CHECKS=0;")
                    db.commit()
                    
                    print(f"[DATABASE][REMOVEWORD] DELETE FROM french WHERE ID = {ID}")
                    try:
                        c.execute(f"DELETE FROM french WHERE ID = {ID}")
                        db.commit()
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT executé.")
                    except:
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT non executé.")

                    print(f"[DATABASE][REMOVEWORD] DELETE FROM normand WHERE ID = {ID}")
                    try:
                        c.execute(f"DELETE FROM normand WHERE ID = {ID}")
                        db.commit()
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT executé.")
                    except:
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT non executé.")

                    c.execute(f"""
                        SET FOREIGN_KEY_CHECKS=1;
                    """)
                    db.commit()

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            db.close()

    def modifyWord(self,ID,frenchWord,normandWord):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    print(f"[DATABASE][MODIFYWORD] {currentTime} UPDATE french SET word = '{frenchWord}' WHERE ID = {ID}.")
                    try:
                        c.execute(f"UPDATE french SET word = '{frenchWord}' WHERE ID = {ID} ")
                        db.commit()
                        print(f"[DATABASE][MODIFYWORD] {currentTime} COMMIT executé.")
                    except mysql.connector.Error as err:
                        print(f"[DATABASE][MODIFYWORD] {currentTime} Impossible de modifier le mot français.")
                        print(f"[DATABASE][MODIFYWORD] {currentTime} {error1}")
                    
                    print(f"[DATABASE][MODIFYWORD] {currentTime} UPDATE normand SET word = '{normandWord}' WHERE ID = {ID}.")
                    try:
                        c.execute(f"UPDATE normand SET word = '{normandWord}' WHERE ID = {ID} ")
                        db.commit()
                    except mysql.connector.Error as err:
                        print(f"[DATABASE][MODIFYWORD] {currentTime} Impossible de modifier le mot français")
                        print(f"[DATABASE][MODIFYWORD] {currentTime} {error1}")

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][MODIFYWORD] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][MODIFYWORD] {currentTime} {error1}")
            db.close()

    def getWord(self,ID):
        currentTime = time.strftime("%x-%X")

        result : dict = { "word" : []}

        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    try:
                        pass
                    except mysql.connector.Error as err:
                        pass

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][GETWORD] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][GETWORD] {currentTime} {error1}")
            db.close()

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
#DATABASE.addWord("bonjour","bonjou")
DATABASE.addWord("bonjour","bonjou")
DATABASE.addWord("bonjoure","bonjoue")      
DATABASE.addWord("bonjoura","bonjoua")
DATABASE.addWord("bonjouri","bonjoui") 

DATABASE.removeWord(4)
DATABASE.removeWord(5)
DATABASE.removeWord(6)
DATABASE.removeWord(7)