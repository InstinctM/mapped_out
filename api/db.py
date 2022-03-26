#import this and use the functions to access the db

from multiprocessing import synchronize
from sqlalchemy import create_engine, Column, Integer, Float,String, null, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from geopy import distance
from time import sleep

from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

opencageKey="06fee6e0f0fd4b82972c28992c487837"
geocoder=OpenCageGeocode(opencageKey)

engine = create_engine('sqlite:///./mapped_out.db',connect_args={"check_same_thread": False})

metadata=MetaData()

Base=declarative_base()
#use session.query (sqlalchemy) with record objects
#represents records in post table
class post(Base):
    def __init__(self,author,link,desc, likes, latitude, longitude, location):
        self.author=author
        self.link=link
        self.description=desc
        self.likes=likes
        self.latitude=latitude
        self.longitude=longitude
        self.location=location

    __tablename__="posts"

    rowid = Column(Integer, primary_key=True) #this exists by default in sql tables
    author = Column(Integer, nullable=False)
    link = Column(String,unique=True, nullable=False)
    description = Column(String)
    likes = Column(Integer)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(String)

    def __repr__(self):
        return '<post ( rowid=%s , author=%s, link=%s, description=%s, likes=%s, latitude=%s, longitude=%s, location=%s )> ' % (self.rowid, self.author, self.link, self.description, self.likes, self.latitude, self.longitude, self.location)

#records in user table
class user(Base):

    def __init__(self,userid,username,password,token,tokenExpire,country,points):
        self.userid = userid
        self.username = username
        self.password = password
        self.token = token
        self.tokenExpire = tokenExpire
        self.country = country
        self.points = points
        
    __tablename__ = "users"
    

    rowid = Column(Integer, primary_key=True)
    userid = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    password = Column(String, nullable=False) 
    token = Column(String, nullable=False) 
    tokenExpire = Column(Integer, nullable=False)
    country = Column(String)
    points = Column(Integer)


    def __repr__(self):
        return '<user ( rowid=%s , userid=%s , username=%s, password=%s, token=%s, tokenExpire=%s, country=%s, points=%s ) >' % ( self.rowid, self.userid, self.username, self.password, self.token, self.tokenExpire, self.country, self.points)

Base.metadata.create_all(engine)

Session=sessionmaker()
Session.configure(bind=engine)
session=Session()

def add_post(entry):
    #entry is a post object

    #reverse geocode
    tries=0
    while(tries<4):
        try:
            results=geocoder.reverse_geocode(entry.latitude,entry.longitude,language='en')
            if results and len(results):
                loc=results[0]['formatted']
                entry.location=loc
                break
            else:
                tries+=1
                continue
        except RateLimitExceededError as err:
            print(err)
            print("---- Opencage Rate Limit.")
            sleep(1)
            tries+=1
            continue
        except InvalidInputError as err:
            print(err)
            break

    try:
        session.add(entry)
        session.commit()
        return True
    except Exception as err:
        print(err)
        session.rollback()
        return False

def search_location(find_s):
    try:
        results=geocoder.geocode(find_s,no_annotations='1')
        if results and len(results):
            longitude=results[0]['geometry']['lat']
            latitude=results[0]['geometry']['lng']
            return (latitude, longitude)
            """
            post_mtch=session.query(post).filter(post.description.like("%"+find_s+"%")).all()
            #if want to search posts aswell
            ret={
                "coord":(latitude,longitude),
                "posts": post_mtch
            }
            return ret
            """
        else:
            return None
    except Exception as err:
        print(err)
        return None

def modify_post(link_n,newlink_n=None,author_n=None,desc_n=None,likes_n=None,lat_n=None,long_n=None,loc_n=None):
    #use keywords as arguements, only changes for those given
    result=session.query(post).filter(post.link==link_n).scalar()
    if result==None:
        return False
    else:
        #this is lazy and makes me look like i did a lot of hard coding ;)
        if newlink_n!=None:
            result.link=newlink_n
        if author_n!=None:
            result.author=author_n
        if desc_n!=None:
            result.description=desc_n
        if likes_n!=None:
            result.likes=likes_n
        if lat_n!=None:
            result.latitude=lat_n
        if long_n!=None:
            result.longitude=long_n
        if loc_n!=None:
            result.location=loc_n
        
        #reverse geocode
        tries=0
        while(tries<4):
            try:
                geocode_results=geocoder.reverse_geocode(result.latitude,result.longitude,language='en')
                if geocode_results and len(geocode_results):
                    loc=geocode_results[0]['formatted']
                    result.location=loc
                    break
                else:
                    tries+=1
                    continue
            except RateLimitExceededError as err:
                print(err)
                print("---- Opencage Rate Limit.")
                sleep(1)
                tries+=1
                continue
            except InvalidInputError as err:
                print(err)
                break


        try:
            session.commit()
            return True
        except Exception as err:
            print(err)
            session.rollback()
            return False

def add_user(entry):
    #entry is a user object
    try:
        session.add(entry)
        session.commit()
        return True
    except Exception as err:
        print(err)
        session.rollback()
        return False
def delete_video(link):
    try:
        session.query(post).filter(post.link == link).delete(synchronize_session=False)
        session.commit()
        return True
    except Exception as err:
        print(err)
        session.rollback()
        return False

def return_video(id,link):
    try:
        print(id, link)
        return session.query(post).filter(post.author == id, post.link == link).scalar()
    except Exception as err:
        print(err)
        session.rollback()
        return False

def updateLikes(link,upOrDown):
    video = session.query(post).filter(post.link == link).scalar()
    author = session.query(user).filter(user.userid == video.author).scalar()
    if (video!=None) or (author!=None):
        video.likes += upOrDown
        author.points += upOrDown
        try:
            session.commit()
            return True
        except Exception as err:
            print(err)
            session.rollback()
            return False
    else:
        return False
    
def post_query_radius(latitude, longitude, radius): #assuming radius is in miles for now
    matches=[]
    for post_entry in session.query(post):
        coord=(post_entry.latitude, post_entry.longitude)
        print(distance.distance((latitude,longitude),coord).miles)
        if(distance.distance((latitude,longitude),coord).miles<radius):
            author = session.query(user).filter(user.userid == post_entry.author).scalar()
            if author == None: # Should not happen
                continue # ignore this post
            matches.append({
                "userid": str(author.userid),
                "username": author.username,
                "link": post_entry.link,
                "description": post_entry.description,
                "latitude": post_entry.latitude,
                "longitude": post_entry.longitude,
                "likes": post_entry.likes,
                "location": post_entry.location,
            })
    return {"result": "success", "posts": matches}

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
