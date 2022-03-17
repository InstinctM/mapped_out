"""
This API provides the platform for the FrontEnd to interact with the DB. 
The FrontEnd Should be able to : 
    Request Videos
    Post New Videos
    
    More Features Implementable in due course.
"""


from typing import final
from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Session as ses,post as db_post
app = FastAPI() 

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
