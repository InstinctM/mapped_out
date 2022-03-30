"""
This API provides the platform for the FrontEnd to interact with the DB. 
The FrontEnd Should be able to : 
    Request Videos
    Post New Videos
    
    More Features Implementable in due course.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import Session as ses, post as db_post, user as db_user, add_post,delete_video,return_video,updateLikes
from db import post_query_radius, modify_post, search
from login import LoginAuthentication

import sys
sys.path.append("../web")
import web
from fastapi.middleware.wsgi import WSGIMiddleware

app = FastAPI() 

app.mount("/web",WSGIMiddleware(web.app))

def get_db():
    db = ses()
    try:
        yield db
    finally:
        db.close()


### Endpoints
@app.get("/")
def root():
    return RedirectResponse("/web/about",302)

# Post new user video! 
class Video_Post (BaseModel):
    userid : int
    token : str
    link : str
    description : str
    lon : float
    lat : float
    location : str

@app.post('/post')
def post(request : Video_Post):
    user = LoginAuthentication.authenticate(request.userid, request.token)
    if user == None: # authenticate user
        return {"result": "unauthorized"}
    user_video  = db_post(
        author = request.userid,
        link = request.link,
        desc = request.description,
        location = "Un-Implemented", # Call geo-coding?
        latitude = request.lat,
        longitude = request.lon,
        likes = 0,
    )
    if add_post(user_video): # add_post returns true if success
        return {"result": "success"}
    return {"result": "fail-add"}

# Get Videos from DB!
class GetPosts(BaseModel):
    lat : float
    lon : float
    radius : float

@app.get('/get-posts')
def get(lat : float, lon : float, radius : float):
    posts = post_query_radius(lat, lon, radius)
    return posts

class Video_Delete(BaseModel):
    userid : int
    token : str
    link: str
# Delete Videos From the DB
@app.post('/delete')
def delete(request:Video_Delete):
    
    user = LoginAuthentication.authenticate(request.userid, request.token)
    if user == None: 
        return None
    video = return_video(user.userid,request.link)
    if not video:
        return None
    delete_video(video.link)
    return True

class Video_Edit(BaseModel):
    userid : int
    token : str
    oldlink : str
    link : str
    description : str
    lat : float
    lon : float

@app.post('/edit-video')
def edit(request:Video_Edit):
    user = LoginAuthentication.authenticate(request.userid, request.token)
    if user == None: # authenticate user
        return {"result": "unauthorized"}
    video = return_video(user.userid, request.oldlink)
    if video == None: # authenticate user
        return {"result": "no-video"}
    result = modify_post(request.oldlink,newlink_n=request.link,
        lat_n=request.lat, long_n=request.lon, desc_n=request.description)
    if (result):
        return {"result": "success"}
    return {"result": "failed"}


@app.get('/search-post')
def searchPost(kw : str, mode : str):
    result = search(kw)
    if (mode == "coord"):
        lat, lon = result["coord"]
        if (lat == None or lon == None):
            return {"result": "notfound"}
        return {"result": "success", "latitude": lat, "longitude": lon}
    elif (mode == "post"):
        joined = result["location"] + result["posts"]
        joined = list(dict.fromkeys(joined)) # remove duplicate
        posts = []
        for post in joined:
            author = LoginAuthentication.getUserProfile(post.author)
            if (author == None):
                continue
            posts.append({
                "username": author["username"],
                "link": post.link,
                "description": post.description,
                "location": post.location,
                "latitude": post.latitude,
                "longitude": post.longitude,
                "likes": post.likes,
            })
        
        return {"result": "success", "posts": posts}
    elif (mode == "user"):
        return {"result": "success", "posts": result["users"]}
    return {"result": "invalid-mode"}


# User Sign UP
class UserSignUp (BaseModel):
    username : str
    password : str
    country : str
@app.post('/signup')
def signup(user: UserSignUp):
    result = LoginAuthentication.createNewUser(user.dict())
    if result:
        return {"result": "success"}
    return None
    
class UserLogin(BaseModel):
    username : str
    password : str
@app.post('/user-login')
def user_login(user : UserLogin):
    result = LoginAuthentication.login(user.username, user.password)
    return result


class GUserLogin(BaseModel):
    token : str
@app.post('/google-login')
def google_login(guser : GUserLogin):
    result = LoginAuthentication.googleLogin(guser.token)
    return result

class UserUpdate(BaseModel):
    userid : int
    token : str
    newUsername : str
    password : str
    newPassword : str
    country : str
@app.post('/user-update')
def user_update(request : UserUpdate):
    user = LoginAuthentication.authenticate(request.userid, request.token)
    if user == None: 
        return {"result": "unauthorized"}
    return LoginAuthentication.updateUserProfile(
        request.userid, request.newUsername, request.password, request.newPassword, request.country,
    )


#Update Likes
class Like_or_Dislike(BaseModel):
    link : str
    like : bool
@app.post('/updateLikes')
def update_likes(request : Like_or_Dislike):
    if request.like:
        updateLikes(request.link,1)
    else:
        updateLikes(request.link,-1)
    return True

@app.get('/get-user')
def getUser(userid : str):
    useridint = int(userid)
    return LoginAuthentication.getUserProfile(useridint)

@app.get('/get-users')
def getUsers():
    return LoginAuthentication.getAllUsers()
