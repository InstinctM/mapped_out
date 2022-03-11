#import this and use the functions to access the db

from sqlalchemy import create_engine, Column, Integer, Float,String, null
from sqlalchemy.orm import declarative_base, sessionmaker
from opencage.geocoder import OpenCageGeocode, InvalidInputError, RateLimitExceededError, UnknownError
from geopy import distance

engine = create_engine('sqlite:///./mapped_out.db',echo=True,connect_args={"check_same_thread": False})

opencageKey="06fee6e0f0fd4b82972c28992c487837"
geocoder=OpenCageGeocode(opencageKey)

Session=sessionmaker()
Session.configure(bind=engine) #autocommit, autoflush params
session=Session()

Base=declarative_base()
#use session.query (sqlalchemy) with record objects
#represents records in post table
class post(Base):
    __tablename__="posts"

    rowid=Column(Integer, primary_key=True) #this exists by default in sql tables
    link=Column(String,unique=True)
    description=Column(String)
    author=Column(String)
    latitude=Column(Float)
    longitude=Column(Float)
    location=Column(String)

    def __repr__(self):
        return '<post ( rowid=%s , link=%s , description=%s , author=%s , longitude=%s , latitude=%s , location=%s )> ' % (self.rowid,self.link,self.description,self.author,self.longitude,self.latitude,self.location)

#records in user table
class user(Base):
    __tablename__="users"

    rowid=Column(Integer, primary_key=True)
    userid=Column(String, unique=True)
    name=Column(String)
    accessToken=Column(String, unique=True)

    def __repr__(self):
        return '<user ( rowid=%s , name=%s , accessToken=%s ) >' % ( self.rowid, self.name, self.accessToken)


def add_post(p_link, p_desc, p_author, p_lat, p_long):
    entry=post(link=p_link,author=p_author, description=p_desc, latitude=p_lat, longitude=p_long)
    session.add(entry)
    session.flush()

def post_query_radius(latitude, longitude, radius): #assuming radius is in miles for now
    matches=[]
    for post_entry in session.query(post):
        coord=(post_entry.latitude, post_entry.longitude)
        if(distance.distance((latitude,longitude),coord).miles<radius):
            matches.append(post_entry)
    return matches


#dont use these geocode functions (yet)
'''
def forward_geocode(location):
    try:
        results=geocoder.forward_geocode(location,language='en',limit=1, annotations=1)
        if results and len(results):
            return (results[0]['geometry']['lat'],results[0]['geometry']['lng'])
    except RateLimitExceededError as err:
        print(err)
        return null
    except InvalidInputError as err:
        print(err)
        return null


def reverse_geocode(latitude, longitude):
    try:
        results=geocoder.reverse_geocode(latitude,longitude,language='en',limit=1, annotations=1)
        if results and len(results):
            return (results[0]['formatted'])
    except RateLimitExceededError as err:
        print(err)
        return null
    except InvalidInputError as err:
        print(err)
        return null

def print_db():
    for post_entry in session.query(post):
        print(repr(post_entry))

    for user_entry in session.query(user):
        print(repr(user_entry))
'''