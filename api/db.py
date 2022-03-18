#import this and use the functions to access the db

from sqlalchemy import create_engine, Column, Integer, Float,String, null, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from geopy import distance

engine = create_engine('sqlite:///./mapped_out.db',connect_args={"check_same_thread": False})

metadata=MetaData()

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
        return '<post ( rowid=%s , author=%s, link=%s, description=%s, likes=%s, latitude=%s, longitude=%s, location=%s )> ' % (self.rowid, self.author, self.link, self.description, self.likes, self.latitude, self.longitude, self.location)

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
        return '<user ( rowid=%s , userid=%s , username=%s, token=%s, tokenExpire=%s, country=%s, points=%s ) >' % ( self.rowid, self.userid, self.username, self.token, self.tokenExpire, self.country, self.points)

Base.metadata.create_all(engine)

Session=sessionmaker()
Session.configure(bind=engine)
session=Session()

def add_post(uid,lnk,desc,like_n,lat,long,loc):
    try:
        entry=post(author=uid,link=lnk,description=desc,likes=like_n,latitude=lat,longitude=long,location=loc)
        session.add(entry)
        session.commit()
        return True
    except Exception as err:
        print(err)
        session.rollback()
        return False

def add_user(uid,uname,tkn,tokenexpr,cty,pnts):
    try:
        entry=user(userid=uid,username=uname,token=tkn,tokenExpire=tokenexpr, country=cty, points=pnts)
        session.add(entry)
        session.commit()
        return True
    except Exception as err:
        print(err)
        session.rollback()
        return False

def post_query_radius(latitude, longitude, radius): #assuming radius is in miles for now
    matches=[]
    for post_entry in session.query(post):
        coord=(post_entry.latitude, post_entry.longitude)
        print(distance.distance((latitude,longitude),coord).miles)
        if(distance.distance((latitude,longitude),coord).miles<radius):
            matches.append(post_entry)
    return matches

def exists(table,condition):
    #table= user or posts
    #condition is a boolean statement e.g. user.userid==123456
    q=session.query(table).filter(condition).exists()
    return session.query(q).scalar()

def print_db():
    print("-------- Users --------")
    for usr in session.query(user):
        print(repr(usr))
    print()
    print("----------------")


    print("-------- Posts --------")
    for pst in session.query(post):
        print(repr(pst))
    print()
    print("----------------")