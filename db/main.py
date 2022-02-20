from sqlalchemy import create_engine, Column, Integer, Float,String
from sqlalchemy.orm import declarative_base, sessionmaker

opencageApiKey="06fee6e0f0fd4b82972c28992c487837"

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

    def __repr__(self):
        return '<post ( rowid=%s , link=%s , description=%s , author=%s , longitude=%s , latitude=%s )> ' % (self.rowid,self.link,self.description,self.author,self.longitude,self.latitude)

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

def add_post():
    pass








