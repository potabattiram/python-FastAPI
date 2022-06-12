from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from MiddleWares import addToActiveUsersList, authenticateUser, createAccessToken, decodeAccessToken, removeFromActiveUsersList,checkUserInList

"""
    Additional Information- 
        1. In this project, we will be using OAuth2 for authentication.
        2. We will be using JWT for encoding and decoding access token.
        3. We will be using FastAPI for creating REST API.
        4. We will be using MiddleWares for adding and removing users from activeUsers list.
        5. We will be using Data for userList and activeUserList.
        6. We will be using config for SECRET_KEY and ALGORITHM.
"""

# App and Router Initialization
app = FastAPI()

# Pass in the tokenUrl parameter to the OAuth2PasswordBearer class
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Welcome Route
@app.get("/")
def Main():
        return "Welcome to Auth Feed System project by @RamPotabatti"


"""
Login Route- 
    1. Requests for Username and Password
    2. Authenticate user
    3. Create/encode access token
    4. Add user to activeUsers list
    5. Return access token
"""
@app.post("/api/login")
def Login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    access_token = createAccessToken(data={"username":username})
    
    if authenticateUser(username,password):
        if checkUserInList(username):
            removeFromActiveUsersList(username)
            Logout(access_token)
            print("Logged out successfully from Previous Session")
        else:
            pass
        addToActiveUsersList(username)
        return {"access_token": access_token,"message":"Logged in successfully"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


"""
Validate Token Route
    1. Requests for access token from frontend
    2. Decodes access token
"""
@app.get("/api/validate")
def validate(token: str = Depends(oauth2_scheme)):
    username = decodeAccessToken(token)
    if checkUserInList(username):
        return {"message":"success"}
    else:
        raise HTTPException(status_code=400, detail="Token expired")


"""
Logout Route
    1. Requests for access token from frontend
    2. Decodes access token
    3. Removes user from activeUsers list
"""        
@app.get("/api/logout")
def Logout(token: str = Depends(oauth2_scheme)):
    username = decodeAccessToken(token)
    if checkUserInList(username):
        removeFromActiveUsersList(username)
        return {"message":"Logged out successfully"}
    else:
        return {"message": "Already Logged out"}


