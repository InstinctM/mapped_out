import os
import time
from google.oauth2 import id_token
from google.auth.transport import requests
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
    def authenticate(cls, userId, token):
        """ Returns True if user is authenticated.
            For both login methods.
        """
        # Get correctToken from database
        user = db.session.query(db.user).filter_by(userid=userId).scalar()
        if (user == None):
            return None
        correctToken = user.token
        tokenExpire = user.tokenExpire
        if (correctToken == None) or (tokenExpire == None):
            return None
        elif (time.time() > tokenExpire):
            return None
        elif (token != correctToken):
            return None
            
        return user

    @classmethod
    def createNewUser(cls, userDict):
        """Takes in user as dictionary.
           Returns True if sucessful.
        """
        userId = hash(userDict["username"])
        # See if userId already exist in database
        if(db.exists(db.user, db.user.username == userDict["username"])):
            return False

        # Add default values
        userDict["userid"] = userId
        userDict["token"] = ""
        userDict["tokenExpire"] = 0
        userDict["points"] = 0

        if(db.add_user(db.user(**userDict))):
            return True
        else:
            return False

    @classmethod
    def login(cls, username, password):
        """Takes username and hashed password as parameters.
           Returns a (userId, token) if successful. Returns None otherwise.
        """
        # Get hashed password from database

        user = db.session.query(db.user).filter(db.user.username == username, db.user.password != "").first()
        if (user == None):
            return None
        if (password == user.password):
            user.token = secrets.token_hex(32)
            # Update token to database
            user.tokenExpire = int(time.time() + cls.EXPIRE_TIME)

            try:
                db.session.commit()
                return {
                    "userid": str(user.userid), # javascript cannot take this big of an int
                    "token": user.token,
                    "tokenExpire": user.tokenExpire,
                }
            except Exception as err:
                print(err)
                return None
        return None

    @classmethod
    def googleLogin(cls, credential):
        """Takes google credential JWT as parameter.
           Returns idinfo if successful. Returns None otherwise.
        """
        try:
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), cls.GOOGLE_CLIENT_ID)
            print(idinfo['sub'])
            userId = hash(idinfo['sub'])
            print(userId)
            username = idinfo['name']
        except ValueError:
            return None

        # Check if userid exist in db
        # If not, then create new user with the given userid
        user = db.session.query(db.user).filter_by(userid=userId).scalar()
        if (user == None):
            # Create user with no password, indicating user signs in with google
            user = db.user(userId, username, "", "", 0, "Country", 0)
        user.token = secrets.token_hex(32)
        user.tokenExpire = int(time.time() + cls.EXPIRE_TIME)

        db.add_user(user)

        try:
            db.session.commit()
        except Exception as err:
            print(err)
            return None

        return {
            "userid": str(userId), # javascript cannot take this big of an int
            "username": user.username,
            "token": user.token,
            "tokenExpire": user.tokenExpire,
        }
        
    @classmethod
    def updateUserProfile(cls, userid, newUsername, password, newPassword, country):
        user = db.session.query(db.user).filter(db.user.userid == userid).scalar()
        if (db.exists(db.user, db.user.username == newUsername) and user.username != newUsername):
            return {"result": "username-taken"}
        if (user == None):
            return {"result": "user-not-exist"}
        if (user.password != password and user.password != ""):
            return {"result": "wrong-old-password"}
        user.username = newUsername
        user.country = country
        user.password = newPassword
        try:
            db.session.commit()
        except Exception as err:
            print(err)
            return {"result": "db-failed"}
        return {"result": "success"}

    @classmethod
    def getUserProfile(cls, userid):
        user = db.session.query(db.user).filter(db.user.userid == userid).scalar()
        if (user == None):
            return {"result": "user-not-exist"}
        return {
            "result": "success",
            "userid": str(user.userid),
            "username": user.username,
            "country": user.country,
            "points": user.points
        }
