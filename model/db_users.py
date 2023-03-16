import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
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
                    grade VARCHAR(255) DEFAULT "user",
                    token VARCHAR(255) DEFAULT NULL,
                    delay TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
            pswdEncoded  = str(password)
            resultEncoded = str(result[3])
            
            if bcrypt.checkpw(pswdEncoded.encode("utf-8"), resultEncoded.encode("utf-8")):
                return True
            else:
                return False
        
        return True
    
    def get_id_by_email(self,email):
        if self.check_user(email) != True:
            return False
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        try:
            c.execute(f'''
                SELECT id FROM users
                WHERE email = '{email}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        result = c.fetchone()
        return result

    def connect_user(self,email,password):
        if self.check_user(email,password) != True:
            return False
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        time_delay = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
        pswd_bytes = (f"{email}isConneted").encode("utf-8")
        hashed_token = bcrypt.hashpw(pswd_bytes, bcrypt.gensalt()).decode('utf-8')

        try:
            c.execute(f'''
                UPDATE users
                    SET
                        token =  '{hashed_token}',
                        delay = '{time_delay}'
                WHERE email = '{email}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return None
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
                SELECT token,delay FROM users
                WHERE token = '{token}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        
        result = c.fetchone()
        if result == None or result[1] == None:
            cnx.close()
            return False
        if int(result[1].strftime('%Y%m%d%H%M%S')) < int(datetime.now().strftime('%Y%m%d%H%M%S')):
            cnx.close()
            self.remove_token(token)
            return False
            
        cnx.close()
        return True

    def remove_token(self,token):
        if self.connect_database() is not None:
            cnx = self.connect_database()
        else:
            return False
        cnx.autocommit = True
        c = cnx.cursor()

        try:
            c.execute(f'''
                UPDATE users
                SET
                    token = NULL
                WHERE token = '{token}'
            ''')
        except mysql.connector.Error as err:
            cnx.close()
            logging.error(f"{err}")
            return False
        
        return True


