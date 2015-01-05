#!/bin/python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Date
from sqlalchemy import create_engine, event, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

IN_USE = "In use";
NOT_IN_USE = "Not in use";
DISPOSED = "Disposed";
INVALID = "Invalid";

class Machine(Base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    serial = Column(String(250), nullable = True)
    unit_value = Column(Float, nullable = True)
    invoice = Column(String(50), nullable = False)
    cap_date = Column(Date, nullable = True)
    base = Column(Float, nullable = True)
    hbase = Column(Float, nullable = True)
    rack_id = Column(Integer, ForeignKey('rack.id'))
    model_id = Column(Integer, ForeignKey('machine_model.id'))
    state_id = Column(Integer, ForeignKey('state.id'))

class MachineType(Base):
    __tablename__ = 'machine_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

class MachineModel(Base):
    __tablename__ = 'machine_model'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    type_num = Column(String(100), nullable = True)
    model_num = Column(String(100), nullable = True)
    size = Column(Float, nullable = True)
    horizontal_space = Column(Float, nullable = True)
    type = Column(Integer, ForeignKey('machine_type.id'))
    brand_id = Column(Integer, ForeignKey('brand.id'))

class Rack(Base):
    __tablename__ = 'rack'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    size = Column(Integer, nullable = True)
    sort = Column(Integer, nullable = True)
    state_id = Column(Integer, ForeignKey('state.id'))

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

def after_create(session):
    session.add(State(name = IN_USE))
    session.add(State(name = NOT_IN_USE))
    session.add(State(name = DISPOSED))
    session.add(State(name = INVALID))
    session.commit()

engine = create_engine('sqlite:///labadmin.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)
session = DBSession()

if session.query(State).count() == 0:
    after_create(session)
