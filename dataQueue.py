from sqlalchemy import create_engine, Integer, String, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.exc
import json
import logging
from logging.config import dictConfig

"""

try:
    file = open('logging_config.ini', "r")
except FileNotFoundError as e:
    pass

try:
    config = json.load(file)
except json.JSONDecodeError as e:
    pass
dictConfig(config)

"""
file = open('logging_config.ini', "r")
config = json.load(file)
dictConfig(config)

logger = logging.getLogger('connection_module')


Base = declarative_base()


class User(Base):
    __tablename__ = "person"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True, nullable=True)
    comment = Column('comment', String)


try:
    engine = create_engine('sqlite:///users.db')
    Base.metadata.create_all(bind=engine)
except sqlalchemy.exc.ArgumentError as e:
    logger.error(e)
