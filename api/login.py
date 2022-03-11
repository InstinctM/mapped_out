import os, sys
from google.oauth2 import id_token
import requests
import secrets
import sqlite3


class LoginAuthentication:
    """Handle user login authentication.
    """

    GOOGLE_CLIENT_ID = ""

    def __init__(self, **kwargs):
        pass

    @classmethod
    def _getDBCur(cls):
        """ Returns the sqlite3 cursor object """
        try:
            dbPath = os.path.join(__file__, "../db/mapped_out.db")
            con = sqlite3.connect(dbPath)
            cur = con.cursor()
        except:
            print("Database Error")
            return None
        return cur

    @classmethod
    def authenticate(cls, userId, token):
        """ Returns True if user is authenticated.
            For both login methods.
        """
        # Get correctToken from database
        cur = cls._getDBCur()
        if (cur == None):
            return False
        cur.execute(f"SELECT token from users WHERE userId = '{userId}';")
        correctToken = cur.fetchone()
        if (correctToken == None):
            return None
        correctToken = correctToken[0]

        return token == correctToken

    @classmethod
    def createNewUser(cls, user):
        """Takes in user as dictionary.
           Returns True if sucessful.
        """
        userId = hash(user["username"])
        # See if userId already exist in database
        query = True
        if (query):
            return False

        cur = cls._getDBCur()
        if (cur == None):
            return False

        cur.execute(f"""
            INSERT INTO users (userId, username, password, token, country, points) 
            VALUES ({userId}, '{user["username"]}', '{user["password"]}', '', '{user["country"]}', 0);
        """)
        
        return True

    @classmethod
    def login(cls, username, password):
        """Takes username and hashed password as parameters.
           Returns a token if successful. Returns None otherwise.
        """
        # Get hashed password from database
        cur = cls._getDBCur()
        if (cur == None):
            return None
        cur.execute(f"SELECT password from users WHERE username = '{username}';")
        correctPassword = cur.fetchone()
        if (correctPassword == None):
            return None
        correctPassword = correctPassword[0]

        if (password == correctPassword):
            token = secrets.token_hex(32)
            # Update token to database
            cur.execute(f"UPDATE users SET token = '{token}' WHERE username = '{username}';")
            return token
        return None

    @classmethod
    def googleLogin(cls, user, token):
        """Takes user and google token as parameter.
           Returns idinfo if successful. Returns None otherwise.
        """
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), cls.GOOGLE_CLIENT_ID)
            userId = idinfo['sub']
            print(userId) # debug
        except ValueError:
            return None

        # Check if userid exist in db
        # If not, then create new user with the given userid
        cur = cls._getDBCur()
        if (cur == None):
            return None
        cur.execute(f"SELECT username from users WHERE userId = '{userId}';")
        existingUser = cur.fetchone()
        if (existingUser == None):
            # Need to think of a way to get their country if logging in for the first time
            # Create user with no password, indicating user signs in with google
            cur.execute(f"""
                INSERT INTO users (userId, username, password, token, country, points) 
                VALUES ({userId}, 'temp_username', '', '', 'a_country', 0);
            """)

        # Update token
        cur.execute(f"UPDATE users SET token = '{token}' WHERE userId = '{userId}';")

        return idinfo
