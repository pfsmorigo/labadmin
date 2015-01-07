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
    invoice = Column(String(50), nullable = True)
    cap_date = Column(Date, nullable = True)
    base = Column(Float, nullable = True)
    hbase = Column(Float, nullable = True)
    rack_id = Column(Integer, ForeignKey('rack.id'))
    model_id = Column(Integer, ForeignKey('machine_model.id'))
    state_id = Column(Integer, ForeignKey('state.id'))

    def __init__(self, name, serial, unit_value, invoice, cap_date,
            base, hbase, rack_id, model_id, state_id):
        self.name = name
        self.serial = serial
        self.unit_value = unit_value
        self.invoice = invoice
        self.cap_date = cap_date
        self.base = base
        self.hbase = hbase
        self.rack_id = rack_id
        self.model_id = model_id
        self.state_id = state_id

    def __repr__(self):
        return "<Machine('%s')>" % self.name

class MachineType(Base):
    __tablename__ = 'machine_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    machine_model = relationship("MachineModel")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<MachineType('%s')>" % self.name

class MachineModel(Base):
    __tablename__ = 'machine_model'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    type_num = Column(String(100), nullable = True)
    model_num = Column(String(100), nullable = True)
    size = Column(Float, nullable = True)
    horizontal_space = Column(Float, nullable = True)
    type_id = Column(Integer, ForeignKey('machine_type.id'))
    brand_id = Column(Integer, ForeignKey('brand.id'))

    machine = relationship("Machine")

    def __init__(self, name, type_num, model_num, size, horizontal_space,
            type_id, brand_id):
        self.name = name
        self.type_num = type_num
        self.model_num = model_num
        self.size = size
        self.horizontal_space = horizontal_space
        self.type_id = type_id
        self.brand_id = brand_id

    def __repr__(self):
        return "<MachineModel('%s')>" % self.name

class Rack(Base):
    __tablename__ = 'rack'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    size = Column(Integer, nullable = False)
    sort = Column(Integer, nullable = True)
    state_id = Column(Integer, ForeignKey('state.id'))

    machine = relationship("Machine")

    def __init__(self, name, size, state_id, sort = None):
        self.name = name
        self.size = size
        self.sort = sort
        self.state_id = state_id

    def __repr__(self):
        return "<Rack('%s')>" % self.name

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    machine_model = relationship("MachineModel")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Brand('%s')>" % self.name

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    machine = relationship("Machine")
    rack = relationship("Rack")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<State('%s')>" % self.name

def database_init(session):
    session.add(State(IN_USE))
    session.add(State(NOT_IN_USE))
    session.add(State(DISPOSED))
    session.add(State(INVALID))

    brand = Brand('Generic')
    session.add(Brand('Generic'))
    session.flush()

    type = MachineType('Generic')
    session.add(MachineType('Generic'))
    session.flush()

    session.add(MachineModel('Generic', '1U', None, 1, None, type.id, brand.id))
    session.add(MachineModel('Generic', '2U', None, 2, None, type.id, brand.id))
    session.add(MachineModel('Generic', '3U', None, 3, None, type.id, brand.id))
    session.add(MachineModel('Generic', '4U', None, 4, None, type.id, brand.id))
    session.add(MachineModel('Generic', '5U', None, 5, None, type.id, brand.id))
    session.flush()

    session.commit()

def database_example(session):
    rack_elves = Rack('Elves', 42, 1)
    rack_dwalves = Rack('Dwalves', 10, 1, 2)
    rack_men = Rack('Men', 42, 1, 1)
    session.add(rack_elves)
    session.add(rack_dwalves)
    session.add(rack_men)
    session.flush()

    brand = Brand('Middle-earth')
    session.add(brand)
    session.flush()

    machine_type_server = MachineType('Server')
    machine_type_network = MachineType('Network')
    machine_type_storage = MachineType('Storage')
    session.add(machine_type_server)
    session.add(machine_type_network)
    session.add(machine_type_storage)
    session.flush()

    machine_model_server = MachineModel('Server', 'AAA', '1234', 2,
            None, machine_type_server.id, brand.id)
    machine_model_big_server = MachineModel('Big Server', 'AAA', '4321', 5,
            None, machine_type_server.id, brand.id)
    machine_model_switch = MachineModel('Switch', 'XYZ', '9999', 1,
            None, machine_type_network.id, brand.id)
    session.add(machine_model_server)
    session.add(machine_model_big_server)
    session.add(machine_model_switch)
    session.flush()

    machine_galadriel = Machine('Galadriel', '1362', None, None, None, 10, 10,
            rack_elves.id, machine_model_big_server.id, 1)
    machine_turgon = Machine('Turgon', '1300', None, None, None, 10, 10,
            rack_elves.id, machine_model_big_server.id, 1)
    machine_finwe = Machine('Finwe', '1300', None, None, None, 10, 10,
            rack_elves.id, machine_model_big_server.id, 1)
    machine_elros = Machine('Elros', '1300', None, None, None, 10, 10,
            rack_elves.id, machine_model_server.id, 1)
    machine_tuor = Machine('Tuor', '1300', None, None, None, 10, 10,
            rack_elves.id, machine_model_server.id, 1)
    session.add(machine_galadriel)
    session.add(machine_turgon)
    session.add(machine_finwe)
    session.add(machine_elros)
    session.add(machine_tuor)
    session.flush()

    session.commit()

engine = create_engine('sqlite:///labadmin.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)
session = DBSession()

if session.query(State).count() == 0:
    database_init(session)
    database_example(session)

print "Racks:    %u" % session.query(Rack.id).count()
print "Machines: %u" % session.query(Machine.id).count()
