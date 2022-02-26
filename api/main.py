from fastapi import FastAPI
import sqlite3


app = FastAPI()


@app.get("/")
def root():
    pass

@app.get("/radius/")
def get_videos(xCor : str, yCor: str):
    """ Connects to the database, returns all videos in radius. """
    return {xCor, yCor}

@app.get("/upload/{link}/{title}/{author}/{long}/{lat}")
def post_videos(link: str,title:str,author:str,long:float,lat:float):
    try:
        con=sqlite3.connect('../db/mapped_out.db')
        cur=con.cursor()
        try:
            cur.execute('INSERT INTO posts VALUES ("{}","{}","{}","{}","{}","NONE")'.format(link,title,author,long,lat))
        except sqlite3.Error as error:
            print(error)
        con.commit()
        con.close()
    except sqlite3.Error as error:
        print(error)
    
    
    