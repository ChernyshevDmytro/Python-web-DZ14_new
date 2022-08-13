from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base() 

many_to_many = Table(
    "many_to_many",
    Base.metadata,
    #Column("id", Integer, primary_key=True),
    #Column("author_id", Integer, ForeignKey("person.id")),  
    Column("keywords_id", Integer, ForeignKey("keywords.id")),
    Column("quotes_id", Integer, ForeignKey("quotes.id")),
)

class Person(Base):
    __tablename__ = "person"    
    id = Column(Integer, primary_key=True)
    author_name = Column(String(50), nullable=False)
    birthday_and_place_of_born= Column(String(50), nullable=True)
    additional_info = Column(String(50), nullable=True)  

class Keywords(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50))
    #author_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE")) 

class Quotes(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    quote = Column(String(50))
    author_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE"))
    keywords = relationship("Keywords", secondary=many_to_many, backref="keywords")

engine = create_engine('sqlite:///dz14.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)    