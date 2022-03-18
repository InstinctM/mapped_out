"""
This API provides the platform for the FrontEnd to interact with the DB. 
The FrontEnd Should be able to : 
    Request Videos
    Post New Videos
    
    More Features Implementable in due course.
"""


from typing import final
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import Session as ses,post as db_post



app = FastAPI() 


"""
    Allow CORS
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://127.0.0.1:8080",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)



@app.get("/")
def root():
    pass

# Post new user video! 
class Video_Post (BaseModel):
    link : str
    author : str
    description : str
    long : float
    lat : float
    location : str

def get_db():
    db = ses()
    try:
        yield db
    finally:
        db.close()

@app.post('/post')
def post(request : Video_Post, db:Session = Depends(get_db)):
    user_video  = db_post(author = request.author,
                          link = request.link,
                          description = request.description,
                          location = "Un-Implemented",
                          latitude = request.lat,
                          longitude = request.long)
    db.add(user_video)
    db.commit()
    db.refresh(user_video)
    return user_video 

# Get Videos from DB!
@app.get('/get')
def get(db:Session = Depends(get_db)):
    all_videos = db.query(db_post).all()
    return all_videos # Returns as JSON 

# Delete Videos From the DB
@app.delete('/delete/{link}')
def delete(link: str, db:Session = Depends(get_db)):
    db.query(db_post).filter(db_post.link == link).delete(synchronize_session=False)
    db.commit()
    return None

# User Sign UP
class User_Details (BaseModel):
    email : str
    password : str
    
def get_db():
    db = ses()
    try:
        yield db
    finally:
        db.close()

@app.post('/signup')
def post(request : User_Details, db:Session = Depends(get_db)):
    new_user  = db_post(email = request.email,
                          password = request.password,
                          )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
