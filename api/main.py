from fastapi import FastAPI
import sqlite3


app = FastAPI()


@app.get("/")
def root():
    pass

@app.get("/radius/{xCor}/{yCor}")
def get_videos(xCor : str, yCor: str):
    """ Connects to the database, returns all videos in radius. """
    


    


@app.get("/upload/{link}/{title}/{author}/{long}/{lat}")
""" Connects to the database and inserts a record into the table """
def post_videos(link: str,title:str,author:str,long:float,lat:float):
    try:
        con=sqlite3.connect('../db/mapped_out.db')
        cur=con.cursor()
    except sqlite3.Error as error:
        print(error)
        return {"Error":"Can't connect to DB!"}
    try:
        cur.execute('INSERT INTO posts VALUES ("{}","{}","{}","{}","{}","NONE")'.format(link,title,author,long,lat))
        con.commit()
        con.close()
        return{"Success":"ADDED Video to DB!"}
    except sqlite3.Error as error:
        con.commit()
        con.close()
        print(error)
        return {"Error":"Cant insert to DB!"}
    
    
    
    
    
    