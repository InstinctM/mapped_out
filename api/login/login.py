import requests
import secrets


class LoginAuthentication:
    """Handle user login authentication.
    """

    def __init__(self, **kwargs):
        pass

    @classmethod
    def authenticate(cls, username, token):
        """Returns True if user is authenticated."""
        # Get correctToken from database
        correctToken = token
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
        # Insert new user {
        #   "userId": userId,
        #   "username": user["username"],
        #   "password": user["password"],
        #   "country": user["country"],
        #   "points": 0,
        #}
        return True

    @classmethod
    def login(cls, username, password):
        """Takes username and hashed password as parameters.
           Returns a token if successful. Returns None otherwise.
        """
        # Get hashed password from database
        correctPassword = password
        if (password == correctPassword):
            token = secrets.token_hex(32)
            # Update token to database
            return token
        return None

    #@classmethod
    #def googleLogin(cls, token):
    #    redirectUrl = ""
    #    return redirectUrl
