import mysql.connector
import time
import bcrypt

class users(object):
    connexion : dict = {}

    def __init__(self,host:str,user:str,password:str,database:str): #Initialise la base de donnée
        self.connexion = {
            "host" : host,
            "user" : user,
            "password" : password,
            "database" : database
        }
        self.createDB()

    def createDB(self): # Create the table if it doesn't exist
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][CREATEDATABASE] {currentTime} Création de la base de donnée et de ses tables.")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                db.autocommit = True
                with db.cursor() as c:
                    try:
                        c.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) NOT NULL,
                                email VARCHAR(255) NOT NULL,
                                password_hash VARCHAR(255) NOT NULL
                            )
                        ''')
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

    # Add a user to the database
    def add_user(self,username, email, password):
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][CREATEDATABASE] {currentTime} Création de la base de donnée et de ses tables.")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                db.autocommit = True
                with db.cursor() as c:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('UTF-8')
                    print(hashed_password)

                    try:
                        c.execute(f'''
                            INSERT INTO users (username, email, password_hash)
                            VALUES ('{username}', '{email}', '{hashed_password}')
                        ''')
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

    # Check if a user exists with a given email and password
    def check_user(self,email, password):
        currentTime = time.strftime("%x-%X")
        print(f"[DATABASE][CREATEDATABASE] {currentTime} Création de la base de donnée et de ses tables.")
        try:
            with mysql.connector.connect(**self.connexion) as db:
                db.autocommit = True
                with db.cursor() as c:
                    try:
                        c.execute(f'''
                            SELECT * FROM users
                            WHERE email = {email}
                        ''')
                        
                        print(c.fetchone())

                        if c.fetchone() is not None and bcrypt.checkpw(password.encode('utf-8'), c.fetchone()[2]):
                            
                            c.fetchone() is not None
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False
