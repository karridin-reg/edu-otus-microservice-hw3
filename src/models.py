from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from database.core import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)
