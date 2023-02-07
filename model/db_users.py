import mysql.connector
import time

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
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                email TEXT NOT NULL,
                                password_hash TEXT NOT NULL
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
                    
                    try:
                        c.execute(f'''
                            INSERT INTO users (username, email, password_hash)
                            VALUES ({username}, {email}, {password})
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
                        c.execute('''
                            SELECT * FROM users
                            WHERE email = ? AND password_hash = ?
                        ''', (email, password))
                        return cursor.fetchone() is not None
                    except mysql.connector.Error as err:
                        error = str(err)
                        print(f"[DATABSE][CREATEDATABASE] {currentTime} {error}")
                        return False
        except mysql.connector.Error as err:
            error1 = str(err)
            print(f"[DATABASE][INTABLE] {currentTime} Impossible de se connecter à la base de données")
            print(f"[DATABASE][INTABLE] {currentTime} {error1}")
            return False
