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

def add_post(p_link, p_description, p_author, p_latitude=None, p_longitude=None, p_location=None):
    #if given both coordinates and a text location (address) not going to check they are in the same place

    assert ((p_longitude!=None and p_latitude!=None) or p_location!=None), "Incorrect location Data given"

    if (p_longitude==None and p_latitude==None ) and p_location!=None:
        result=forward_geocode(p_location)
        if result!=null:
            entry=post(link=p_link,description=p_description,latitude=result[0],longitude=result[1],location=p_location)
            session.add(entry)
            session.flush()
        else:
            print("unable to perform forward geocoding.") #TODO more informative error messages

    elif (p_location==None) and (p_longitude!=None and p_latitude!=None):
        result=reverse_geocode(p_latitude,p_longitude)
        if result!=null:
            entry=post(link=p_link,description=p_description,latitude=p_latitude,longitude=p_longitude,location=result)
            session.add(entry)
            session.flush()
        else:
            print("Unable to perform reverse geocoding.") #TODO ^

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
