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

    session.execute("""
            CREATE VIEW "rack_list" AS SELECT
                    rack.*,
                    SUM(mmm.used) AS used
                FROM rack
                LEFT JOIN (SELECT machine.rack_id,
                                  MAX(machine_model.size) AS used
                           FROM machine, machine_model
                           WHERE machine.model_id = machine_model.rowid
                           GROUP BY rack_id, base) AS mmm
                ON rack.id = mmm.rack_id
                WHERE (mmm.rack_id IS NULL OR mmm.rack_id = rack.id)
                AND rack.state_id == 1
                GROUP BY rack.id
                ORDER BY sort, name COLLATE NOCASE ASC;
            """)

    session.execute("""
            CREATE VIEW "machine_list" AS SELECT
                    machine.id AS id,
                    machine.name,
                    machine_model.id AS model_id,
                    machine_model.name AS model_name,
                    machine_model.type_id AS type_id,
                    machine_model.type_num AS type_num,
                    machine_model.model_num AS model_num,
                    machine_model.size AS size,
                    machine_model.horizontal_space AS hspace,
                    machine.serial AS serial,
                    machine.unit_value AS unit_value,
                    machine.invoice AS invoice,
                    machine.cap_date AS cap_date,
                    machine.rack_id AS rack_id,
                    rack.name AS rack_name,
                    rack.sort AS rack_sort,
                    rack.state_id AS rack_state_id,
                    machine.base,
                    machine.hbase,
                    machine.state_id
                FROM machine, machine_model
                LEFT OUTER JOIN rack
                WHERE (machine.rack_id IS 0 OR machine.rack_id = rack.rowid)
                AND machine.model_id = machine_model.id
                GROUP BY machine.id
                ORDER BY machine.name COLLATE NOCASE ASC;
            """)

    session.commit()

def database_example(session):
    rack_elves = Rack('Elves', 42, 1)
    rack_dwalves = Rack('Dwalves', 30, 1, 2)
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

def get_session():
    engine = create_engine('sqlite:///labadmin.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    return DBSession()

def rack_list(session):
    return (session.query(Rack))

    #return (session.query(Rack, func.count(Client.id)).
            #outerjoin(ClientIp, ClientIp.ip_id==Ip.id).
            #outerjoin(Client, Client.id==ClientIp.client_id).
            #group_by(Rack.id))


session = get_session()
if session.query(State).count() == 0:
    database_init(session)
    database_example(session)

print ""
print "labadmin"
print "--------"
print "%5u racks" % session.query(Rack.id).count()
print "%5u machines" % session.query(Machine.id).count()
print "%5u machine models" % session.query(MachineModel.id).count()
print "%5u machine types" % session.query(MachineType.id).count()
print "%5u brands" % session.query(Brand.id).count()
print "%5u states" % session.query(State.id).count()
print ""
