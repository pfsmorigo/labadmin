#!/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import *

engine = create_engine('sqlite:///labadmin.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def database_init():
    session.add(State(name = IN_USE))
    session.add(State(name = NOT_IN_USE))
    session.add(State(name = DISPOSED))
    session.add(State(name = INVALID))
    session.commit()



