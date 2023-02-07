import mysql.connector
import time

class words(object):
    connexion : dict = {}

    def __init__(self,host:str,user:str,password:str,database:str): #Initialise la base de donnée
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
                           CREATE TABLE dictionary (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                fr VARCHAR(255) NOT NULL,
                                normand VARCHAR(255) NOT NULL
                            );
                        """)
                        print(f"[DATABASE][CREATEDATABASE] {currentTime} La table 'dictionary' a été crée.")
                        db.close()
                        return True
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False

    def word_exists(self,word:str): #Vérifies si les mots existent dans les tables
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][INTABLE] {currentTime} Vérification du mot {word} dans la table 'dictionnary'.")

        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    try: #Récupères la donnée dans la colonne word de la table dictionnary
                        c.execute(f"""
                            SELECT id
                            FROM dictionary
                            WHERE fr = '{word}'
                        """)
                        result = c.fetchone()

                        if result != None: 
                            return result[0]

                        c.execute(f"""
                            SELECT id
                            FROM dictionary
                            WHERE normand = '{word}'
                        """)
                        result = c.fetchone()

                        if result != None: 
                            return result[0]

                        print(f"[DATABASE][INTABLE] {currentTime} le mot {word} n'est pas présent dans la table 'french'.")
                        db.close()
                        return False
                    except mysql.connector.Error as err:
                        error1 = str(err)
                        db.close()
                        print(f"[DATABSE][INTABLE] {currentTime} {error1}")
                        return False

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False
            
    def addWord(self,wordFrench:str,wordNormand:str): #Ajoutes des mots dans la base de donnée
        currentTime = time.strftime("%x-%X")

        if self.word_exists(wordFrench) != False and self.word_exists(wordNormand) != False:
            return False
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    
                    #Ajoutes le mot français et le mot normand dans la table 'dictionaru'
                    print(f"[DATABASE][ADDWORD] {currentTime} INSERT INTO dictionary (fr,normand) VALUES ('{wordFrench}','{wordNormand}')")
                    try:
                        c.execute(f"INSERT INTO dictionary (fr,normand) VALUES ('{wordFrench}','{wordNormand}')")
                        db.commit()
                        print(f"[DATABASE][ADDWORD] {currentTime} COMMIT effectué!")
                        db.close()
                        print(f"[DATABASE][ADDWORD] {currentTime} Les mots {wordFrench} et {wordNormand} ont été rajoutés dans les tables.")
                        return True
                    except mysql.connector.Error as err:
                        error1 = str(err)
                        print(f"[DATABSE][ADDWORD] {currentTime} {error1}")
                        db.close()
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False

    def removeWord(self,ID):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    print(f"[DATABASE][REMOVEWORD] DELETE FROM dictionary WHERE id = {ID}")
                    try:
                        c.execute(f"DELETE FROM dictionary WHERE id = {ID};")
                        db.commit()
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT executé.")
                        db.close()
                        return True
                    except:
                        print(f"[DATABASE][REMOVEWORD] {currentTime} COMMIT non executé.")
                        db.close()
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False

    def updateWord(self,ID,frenchWord,normandWord):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor() as c:
                    print(f"[DATABASE][MODIFYWORD] {currentTime} UPDATE dictionary SET fr = '{frenchWord}', normand = '{normandWord}' WHERE ID = {ID};")
                    try:
                        c.execute(f"UPDATE dictionary SET fr = '{frenchWord}', normand = '{normandWord}' WHERE ID = {ID};")
                        db.commit()
                        print(f"[DATABASE][MODIFYWORD] {currentTime} COMMIT executé.")
                        db.close()
                        return True
                    except mysql.connector.Error as err:
                        print(f"[DATABASE][MODIFYWORD] {currentTime} Impossible de modifier!")
                        print(f"[DATABASE][MODIFYWORD] {currentTime} {error1}")
                        db.close()
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][MODIFYWORD] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][MODIFYWORD] {currentTime} {error1}")

    def getWord(self,ID):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor(buffered=True) as c:
                    try:
                        c.execute(f"SELECT fr, normand FROM dictionary WHERE id = {ID};")
                        db.commit()
                        result = c.fetchone()
                        db.close()
                    except mysql.connector.Error as err:
                        print(f"[DATABASE][GETWORD] {currentTime} Impossible de récupérer le mot!")
                        print(f"[DATABASE][GETWORD] {currentTime} {error1}")
                        db.close()
                        return None

                    if result:
                        return {"fr": result[0], "normand": result[1]}
                    else:
                        return None

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][GETWORD] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][GETWORD] {currentTime} {error1}")
            db.close()

    def getAllWord(self):
        currentTime = time.strftime("%x-%X")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                with db.cursor(buffered=True) as c:
                    try:
                        c.execute(f"SELECT id, fr, normand FROM dictionary")
                        db.commit()
                        result = c.fetchall()
                        print (result)
                        db.close()
                    except mysql.connector.Error as err:
                        print(f"[DATABASE][GETWORD] {currentTime} Impossible de récupérer les mots!")
                        print(f"[DATABASE][GETWORD] {currentTime} {error1}")
                        db.close()
                        return None
                    
                    database = []
                    for word in result:
                        temp = {
                            'id' : word[0],
                            'fr' : word[1],
                            'normand' : word[2]
                            }
                        database.append(temp)
                    return database

        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][GETWORD] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][GETWORD] {currentTime} {error1}")
            db.close()