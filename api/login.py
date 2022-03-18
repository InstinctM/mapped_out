import os
import time
from google.oauth2 import id_token
import requests
import secrets
import db


class LoginAuthentication:
    """Handle user login authentication.
    """

    GOOGLE_CLIENT_ID = "1047753082993-1iftbpo90ar6die9le8hffheu3pscik0.apps.googleusercontent.com"
    EXPIRE_TIME = 60 * 60  # Time in seconds

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
        correctToken=db.session.query(db.user).filter_by(userid=userId).one().token
        tokenExpire=db.session.query(db.user).filter_by(userid=userId).scalar().tokenExpire
        if (correctToken == None) or (tokenExpire == None):
            return None

        if (time.time() > tokenExpire):
            return None
            
        return token == correctToken

    @classmethod
    def createNewUser(cls, userDict):
        """Takes in user as dictionary.
           Returns True if sucessful.
        """
        userId = hash(userDict["username"])
        # See if userId already exist in database
        if(db.exists(db.user,db.user.userid==userId)):
            return False
        userDict["userid"]=userId
        if(db.add_user(db.user(**userDict))):
            return True
        else:
            return False

    @classmethod
    def login(cls, userid, password):
        """Takes username and hashed password as parameters.
           Returns a (userId, token) if successful. Returns None otherwise.
        """
        # Get hashed password from database

        user=db.session.query(db.user).filter_by(userid=userid).scalar()
        if (user==None):
            return None
        if (password == user.token):
            user.token = secrets.token_hex(32)
            # Update token to database
            user.tokenExpire = int(time.time() + cls.EXPIRE_TIME)

            try:
                db.session.commit()
                return (user.username, user.token)

            except Exception as err:
                print(err)
                return None
        return None

    @classmethod
    def googleLogin(cls, token):
        """Takes user and google token as parameter.
           Returns idinfo if successful. Returns None otherwise.
        """
        #@benkol003 - what is the 'user' argument for?
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), cls.GOOGLE_CLIENT_ID)
            userId = idinfo['sub']
            print(userId) # debug
        except ValueError:
            return None

        # Check if userid exist in db
        # If not, then create new user with the given userid
        user=db.session.query(db)
        user=db.session.query(db).filter_by(userid=userId).scalar()
        tokenExpire = int(time.time() + cls.EXPIRE_TIME)
        if (user == None):
            # Need to think of a way to get their country if logging in for the first time
            # Create user with no password, indicating user signs in with google
            user=db.user(userId,None,token,tokenExpire,None,0)
        user.token=token
        user.tokenExpire=tokenExpire
        try:
            db.session.commit()
        except Exception as err:
            print(err)
            return None

        return idinfo
