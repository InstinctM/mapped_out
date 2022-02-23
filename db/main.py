from sqlalchemy import create_engine, Column, Integer, Float,String, null
from sqlalchemy.orm import declarative_base, sessionmaker
from opencage.geocoder import OpenCageGeocode, InvalidInputError, RateLimitExceededError, UnknownError

engine = create_engine('sqlite:///./mapped_out.db',echo=True,connect_args={"check_same_thread": False})

Session=sessionmaker()
Session.configure(bind=engine) #autocommit, autoflush params
session=Session()

Base=declarative_base()

class post(Base):
    __tablename__="posts"

    rowid=Column(Integer, primary_key=True) #this exists by default in sql tables
    link=Column(String,unique=True)
    description=Column(String)
    author=Column(String)
    longitude=Column(Float)
    latitude=Column(Float)
    location=Column(String)

    def __repr__(self):
        return '<post ( rowid=%s , link=%s , description=%s , author=%s , longitude=%s , latitude=%s , location=%s )> ' % (self.rowid,self.link,self.description,self.author,self.longitude,self.latitude,self.location)

class user(Base):
    __tablename__="users"

    rowid=Column(Integer, primary_key=True)
    name=Column(String)
    accessToken=Column(String, unique=True)

    def __repr__(self):
        return '<user ( rowid=%s , name=%s , accessToken=%s ) >' % ( self.rowid, self.name, self.accessToken)

for post_entry in session.query(post):
    print(repr(post_entry))

for user_entry in session.query(user):
    print(repr(user_entry))



opencageKey="06fee6e0f0fd4b82972c28992c487837"
geocoder=OpenCageGeocode(opencageKey)

def add_post(link, description, author, latitude=None, longitude=None, location=None):
    #if given both coordinates and a text location (address) not going to check they are in the same place

    assert ((longitude!=None and latitude!=None) or location!=None), "Incorrect location Data given"

    if (longitude==None and latitude==None ) and location!=None:
        result=forward_geocode(location)
        if result!=null:
            pass
        else:
            pass

    elif (location==None) and (longitude!=None and latitude!=None):
        pass


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