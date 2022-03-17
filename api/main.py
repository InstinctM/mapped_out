from fastapi import FastAPI
import sqlite3
from geopy import distance


app = FastAPI()


@app.get("/")
def root():
    pass

@app.get("/radius/{xCor}/{yCor}")
def get_videos(xCor : str, yCor: str):

    """ Connects to the database, returns all videos in radius. """
    
    json = {"Videos":[]}

    center_point = [{'lat': xCor, 'lng': yCor}]
    center_point_tuple = tuple(center_point[0].values()) # (-7.7940023, 110.3656535)
    radius = 5 #IN KM

    try:
        con=sqlite3.connect('../db/mapped_out.db')
        cur=con.cursor()
    except sqlite3.Error as error:
        print(error)
        return {"Error":"Can't connect to DB!"}


    for row in cur.execute('SELECT * FROM posts'):
        pass


        vid = [{'lat': -7.79457, 'lng': 110.36563}]
        vid_tuple = tuple(vid[0].values()) # (-7.79457, 110.36563)

        dis = distance.distance(center_point_tuple, vid_tuple).km
        print("Distance: {}".format(dis)) # Distance: 0.0628380925748918

        if dis <= radius:
            json["Videos"].append(vid)
            


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
    
    
    
    
    
    