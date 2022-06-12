from Data.userList import userData
from config import SECRET_KEY, ALGORITHM
import jwt
from Data.activeUserList import activeUsers

# Function that checks whether the user is authenticated or not
def authenticateUser(username,password):
    try:
        for user in userData:
            if user["username"] == username and user["password"] == password:
                return True
    except:
        return False

# Function that creates access token
def createAccessToken(data: dict):
    to_encode = data.copy()
    encoded_JWT = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_JWT

def addToActiveUsersList(username):
    if username not in activeUsers:
        activeUsers.add(username)
    else:
        pass

def removeFromActiveUsersList(username):
    if username in activeUsers:
        activeUsers.remove(username)
    else:
        pass

def decodeAccessToken(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("username")
    except:
        return False
    
def checkUserInList(username):
    if username in activeUsers:
        return True
    else:
        return False