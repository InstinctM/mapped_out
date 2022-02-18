from sqlalchemy import create_engine, Column, Integer, Float,String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./mapped_out.db',echo=True,connect_args={"check_same_thread": False})

Session=sessionmaker()
Session.configure(bind=engine) #autocommit, autoflush params
session=Session()

Base=declarative_base()

class post(Base):
    __tablename__="posts"

    rowid=Column(Integer, primary_key=True) #this exists by defualt in sql tables
    link=Column(String,unique=True)
    description=Column(String)
    author=Column(String)
    longitude=Column(Float)
    latitude=Column(Float)

    def __repr__(self):
        return '<post ( rowid=%s , link=%s , description=%s , author=%s , longitude=%s , latitude=%s )> ' % (self.rowid,self.link,self.description,self.author,self.longitude,self.latitude)

for post_entry in session.query(post):
    print(repr(post_entry))







