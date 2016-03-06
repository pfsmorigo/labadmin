#!/bin/python

import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'equipment'
    }

class Machine(Equipment):
    __tablename__ = 'machine'
    id = Column(Integer, ForeignKey('equipment.id'), primary_key = True)
    base = Column(Float, nullable = True)

    __mapper_args__ = {
        'polymorphic_identity': 'machine',
        'inherit_condition': (id == Equipment.id)
    }

    def __init__(self, name, base):
        self.name = name
        self.base = base

def get_session():
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    return DBSession()

session = get_session()
session.add(Machine('machine_a', 1))
session.add(Machine('machine_b', 2))
session.add(Machine('machine_c', 3))
session.add(Machine('machine_d', 4))
session.flush()
session.commit()

column_name = 'name'
value = 'machine_e'

for item in session.query(Machine):
    print str(item.id)+"="+item.name

print session.query(Machine).filter(id == 2).one()
#session.query(Machine).filter(id == 2).update({column_name: value})

session.query(Machine).filter(id == 2).one().base = 1
