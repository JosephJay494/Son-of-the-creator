from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String , nullable = False)
    author = Column(String, nullable = False)
    synopsis = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'True', nullable = False)
    created_at = Column(TIMESTAMP (timezone=True), nullable= False, server_default= text('now()'))



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String , nullable = False, unique= True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP (timezone=True), nullable= False, server_default= text('now()'))
    