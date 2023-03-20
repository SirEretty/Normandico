import mysql.connector
from mysql.connector import errorcode
import time
import logging


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)

class Dict(object):
    def __init__(self,host:str,user:str,password:str,database:str): #Initialise la base de donnée
        self.connexion = {
            "host" : host,
            "user" : user,
            "password" : password,
            "database" : database
        }
        self.cnx = mysql.connector
        self.createDatabase()

    def connect_database(self):
        try:
            cnx = mysql.connector.connect(**self.connexion)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database does not exist")
            else:
                logging.error(f"{err}")
            return None
        return cnx

    def createDatabase(self): #Création de la base de donnée et de ses tables
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        
        cnx.autocommit = True
        c = cnx.cursor()

        try:
            c.execute("""
                CREATE TABLE IF NOT EXISTS dictionary (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fr VARCHAR(255) NOT NULL,
                    normand VARCHAR(255) NOT NULL
                );
            """)
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        cnx.close()
        return True

    def word_exists(self,word:str): #Vérifies si les mots existent dans les tables
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        c = cnx.cursor()
                    
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

        cnx.close()
        return False
            
    def addWord(self,wordFrench:str,wordNormand:str): #Ajoutes des mots dans la base de donnée
        if self.word_exists(wordFrench) != False and self.word_exists(wordNormand) != False:
            return False
        
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        c = cnx.cursor()
                    
        try:
            c.execute(f"INSERT INTO dictionary (fr,normand) VALUES ('{wordFrench.lower()}','{wordNormand.lower()}')")
        except mysql.connector.Error as err:
            cnx.rollback()
            cnx.close()
            logging.error(f"{err}")
            return False
        cnx.commit()
        cnx.close()
        return True

    def removeWord(self,ID):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        c = cnx.cursor()
        
        try:
            c.execute(f"DELETE FROM dictionary WHERE id = {ID};")
        except mysql.connector.Error as err:
            cnx.rollback()
            cnx.close()
            logging.error(f"{err}")
            return False
        cnx.commit()
        cnx.close()
        return True

    def updateWord(self,ID,frenchWord,normandWord):
        if self.word_exists(frenchWord) != False and self.word_exists(normandWord) != False:
            return False
        
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        c = cnx.cursor()

        try:
            c.execute(f"UPDATE dictionary SET fr = '{frenchWord.lower()}', normand = '{normandWord.lower()}' WHERE ID = {ID};")
        except mysql.connector.Error as err:
            cnx.rollback()
            cnx.close()
            logging.error(f"{err}")
            return False
        cnx.commit()
        cnx.close()
        return True

    def getWord(self,ID):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return None
        c = cnx.cursor(buffered=True)

        try:
            c.execute(f"SELECT id, fr, normand FROM dictionary WHERE id = {ID};")
        except mysql.connector.Error as err:
            cnx.rollback()
            cnx.close()
            logging.error(f"{err}")
            return None
        cnx.commit()
        result = c.fetchone()
        cnx.close()
                    
        if result:
            return {"id":result[0],"fr": result[1], "normand": result[2]}
        else:
            return None

    def getAllWord(self):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return None
        c = cnx.cursor(buffered=True)

        try:
            c.execute(f"SELECT id, fr, normand FROM dictionary")
        except mysql.connector.Error as err:
            cnx.rollback()
            cnx.close()
            logging.error(f"{err}")
            return None
        cnx.commit()
        result = c.fetchall()
        cnx.close()

        database = []
        for word in result:
            temp = {
                'id' : word[0],
                'fr' : word[1],
                'normand' : word[2]
                }
            database.append(temp)
        return database