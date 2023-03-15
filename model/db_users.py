import mysql.connector
from mysql.connector import errorcode
import time
import bcrypt
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)

class Users(object):
    def __init__(self,host:str,user:str,password:str,database:str): #Initialise la base de donnée
        self.connexion = {
            "host" : host,
            "user" : user,
            "password" : password,
            "database" : database
        }
        self.cnx = mysql.connector
        self.create()

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

    def create(self): 
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()
        try:
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    grade VARCHAR(255) DEFAULT "user"
                )
            ''')
        except mysql.connector.Error as err:
            logging.error(f"{err}")
        
        try:
            c.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    token VARCHAR(255) NOT NULL,
                    delay TIMESTAMP NOT NULL
                )
            ''')
        except mysql.connector.Error as err:
            logging.error(f"{err}")
        
        cnx.close()
        return True

    # Add a user to the database
    def add_user(self,username, email, password):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('UTF-8')

        try:
            c.execute(f'''
                INSERT INTO users (username, email, password_hash)
                VALUES ('{username}', '{email}', '{hashed_password}')
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        
        try:
            c.execute(f'''
                INSERT INTO users (username, email, password_hash)
                VALUES ('{username}', '{email}', '{hashed_password}')
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        
        cnx.close()
        return True

    # Check if a user exists with a given email and password
    def check_user(self,email, password=None):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        try:
            c.execute(f'''
                SELECT * FROM users
                WHERE email = '{email}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False

        result = c.fetchone()

        if result is None:
            return False

        if password is not None:
            pswdEncoded : bytes = bytes(password.encode('utf-8'))
            resultEncoded : bytes = bytes(result[3].encode('utf-8'))
            if bcrypt.checkpw(pswdEncoded, resultEncoded):
                return True
            else:
                return False
        
        return True
    
    def connect_user(self,email,password):
        if self.check_user(email,password) != True:
            return False

        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        delay = time.time() + (120 * 10)
        token = f"{email}isConneted"
        hashed_token = bcrypt.hashpw(token, bcrypt.gensalt()).decode('UTF-8')

        try:
            c.execute(f'''
                INSERT INTO sessions (token, delay)
                VALUES ('{token}', '{delay}')
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        cnx.close() 
        return hashed_token

    def check_token(self,token):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        try:
            c.execute(f'''
                SELECT token FROM sessions
                WHERE token = '{token}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        
        result = c.fetchone()
        if result != None:
            cnx.close()
            return True
        
        cnx.close()
        return False
        
         


