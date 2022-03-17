#import this and use the functions to access the db

from sqlalchemy import create_engine, Column, Integer, Float,String, null
from sqlalchemy.orm import declarative_base, sessionmaker
from geopy import distance

engine = create_engine('sqlite:///./mapped_out.db',echo=True,connect_args={"check_same_thread": False})

Session=sessionmaker()
Session.configure(bind=engine)
session=Session()

Base=declarative_base()
#use session.query (sqlalchemy) with record objects
#represents records in post table
class post(Base):
    __tablename__="posts"

    rowid=Column(Integer, primary_key=True) #this exists by default in sql tables
    author=Column(Integer)
    link=Column(String,unique=True)
    description=Column(String)
    likes=Column(Integer)
    latitude=Column(Float)
    longitude=Column(Float)
    location=Column(String)

    def __repr__(self):
        return '<post ( rowid=%s , link=%s , description=%s , author=%s , longitude=%s , latitude=%s , location=%s )> ' % (self.rowid,self.link,self.description,self.author,self.longitude,self.latitude,self.location)

#records in user table
class user(Base):
    __tablename__="users"

    rowid=Column(Integer, primary_key=True)
    userid=Column(Integer, unique=True)
    username=Column(String)
    token=Column(String) 
    tokenExpire=Column(Integer)
    country=Column(String)
    points=Column(Integer)


    def __repr__(self):
        return '<user ( rowid=%s , name=%s , accessToken=%s ) >' % ( self.rowid, self.name, self.accessToken)


def add_post(uid,lnk,desc,like_n,lat,long,loc):
    entry=post(author=uid,link=lnk,description=desc,likes=like_n,latitude=lat,longitude=long,location=loc)
    session.add(entry)
    session.flush()

def add_user(uid,uname,tkn,tokenexpr,cty,pnts):
    entry=user(userid=uid,username=uname,token=tkn,tokenExpire=tokenexpr, country=cty, points=pnts)
    session.add(entry)
    session.flush()

def post_query_radius(latitude, longitude, radius): #assuming radius is in miles for now
    matches=[]
    for post_entry in session.query(post):
        coord=(post_entry.latitude, post_entry.longitude)
        if(distance.distance((latitude,longitude),coord).miles<radius):
            matches.append(post_entry)
    return matches