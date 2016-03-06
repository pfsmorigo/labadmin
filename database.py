#!/bin/python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Date
from sqlalchemy import create_engine, event, func, collate, and_, or_, sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, aliased

Base = declarative_base()

IN_USE = "In use";
NOT_IN_USE = "Not in use";
INVALID = "Invalid";

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    state_id = Column(Integer, ForeignKey('state.id'))

    state = relationship('State')

    __mapper_args__ = {
        'polymorphic_identity': 'equipment'
    }

class TypeModel(Base):
    __tablename__ = 'type_model'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    type_num = Column(String(100), nullable = True)
    model_num = Column(String(100), nullable = True)
    brand_id = Column(Integer, ForeignKey('brand.id'))

    brand = relationship('Brand')

    def __repr__(self):
        return "<TypeModel('%s')>" % self.name

    def get_description(self):
        if self.type_num == None and self.model_num == None:
            return self.name
        elif self.type_num == None:
            return self.name+' ('+self.model_num+')'
        elif self.model_num == None:
            return self.name+' ('+self.type_num+')'
        else:
            return self.name+' ('+self.type_num+'-'+self.model_num+')'

    def get_type_model(self):
        if self.type_num == None and self.model_num == None:
            return ''
        elif self.type_num == None:
            return self.model_num
        elif self.model_num == None:
            return self.type_num
        else:
            return self.type_num+'-'+self.model_num

class Rack(Equipment):
    __tablename__ = 'rack'
    id = Column(Integer, ForeignKey('equipment.id'), primary_key = True)
    sort = Column(Integer, nullable = True)
    type_model_id = Column(Integer, ForeignKey('rack_type_model.id'))

    type_model = relationship('RackTypeModel')

    __mapper_args__ = {
        'polymorphic_identity': 'rack',
        'inherit_condition': (id == Equipment.id)
    }

    def __init__(self, name, type_model_id, state_id, sort = None):
        self.name = name 
        self.type_model_id = type_model_id
        self.state_id = state_id
        self.sort = sort

    def __repr__(self):
        return "<Rack('%s')>" % self.name

class RackTypeModel(TypeModel):
    __tablename__ = 'rack_type_model'
    id = Column(Integer, ForeignKey('type_model.id'), primary_key = True)
    size = Column(Integer, nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'rack_type_model',
        'inherit_condition': (id == TypeModel.id)
    }

    def __init__(self, name, type_num, model_num, brand_id, size):
        self.name = name 
        self.type_num = type_num
        self.model_num = model_num
        self.size = size 

    def __repr__(self):
        return "<RackTypeModel('%s')>" % self.name

class Machine(Equipment):
    __tablename__ = 'machine'
    id = Column(Integer, ForeignKey('equipment.id'), primary_key = True)
    base = Column(Float, nullable = True)
    hbase = Column(Float, nullable = True)
    rack_id = Column(Integer, ForeignKey('equipment.id'))
    type_model_id = Column(Integer, ForeignKey('machine_type_model.id'))

    type_model = relationship('MachineTypeModel')

    __mapper_args__ = {
        'polymorphic_identity': 'machine',
        'inherit_condition': (id == Equipment.id)
    }

    def __init__(self, name, type_model_id, state_id, base = None, hbase = None, rack_id = None):
        self.name = name 
        self.type_model_id = type_model_id
        self.state_id = state_id
        self.base = base
        self.hbase = hbase
        self.rack_id = rack_id

    def __repr__(self):
        return "<Machine('%s')>" % self.name

    def get_base(self):
        return str('{:g}'.format(float(self.base)))

    def get_size(self):
        return '{:g}'.format(float(self.model.size))

    def get_location(self):
        if self.base == None or self.rack.state_id != 1:
            return '-'
        elif self.model.size == 1:
            return self.get_base()
        else:
            return self.get_base()+' - '+str('{:g}'.format(float(self.base+self.model.size-1)))

class MachineTypeModel(TypeModel):
    __tablename__ = 'machine_type_model'
    id = Column(Integer, ForeignKey('type_model.id'), primary_key = True)
    size = Column(Float, nullable = True)
    horizontal_space = Column(Float, nullable = True)

    __mapper_args__ = {
        'polymorphic_identity': 'machine_type_model',
        'inherit_condition': (id == TypeModel.id)
    }

    def __init__(self, name, type_num, model_num, brand_id, size, horizontal_space = None):
        self.name = name 
        self.type_num = type_num
        self.model_num = model_num
        self.size = size 
        self.horizontal_space = horizontal_space

    def __repr__(self):
        return "<MachineTypeModel('%s')>" % self.name

class Field(Base):
    __tablename__ = 'field'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    field_id = Column(Integer, ForeignKey('field_type.id'))
    equipment_id = Column(Integer, ForeignKey('equipment.id'))

    def __init__(self, name, field_id, equipment_id):
        self.name = name
        self.field_id = field_id
        self.equipment_id = equipment_id

    def __repr__(self):
        return "<Field('%s')>" % self.name

class FieldType(Base):
    __tablename__ = 'field_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<FieldType('%s')>" % self.name

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Brand('%s')>" % self.name

class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<State('%s')>" % self.name

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key = True)
    description = Column(String(250), nullable = True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'))
    event_type_id = Column(Integer, ForeignKey('event_type.id'))

    def __init__(self, description, event_type_id, equipment_id):
        self.description = description
        self.event_type_id = event_type_id
        self.equipment_id = equipment_id

    def __repr__(self):
        return "<Event('%s')>" % self.description

class EventType(Base):
    __tablename__ = 'event_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<EventType('%s')>" % self.name

def database_init(session):
    session.add(State(IN_USE))
    session.add(State(NOT_IN_USE))
    session.add(State(INVALID))
    session.add(RackTypeModel('Generic rack', '11U', None, None, 11))
    session.add(RackTypeModel('Generic rack', '25U', None, None, 25))
    session.add(RackTypeModel('Generic rack', '42U', None, None, 42))
    session.add(MachineTypeModel('Generic machine', '1U', None, None, 1))
    session.add(MachineTypeModel('Generic machine', '2U', None, None, 2))
    session.add(MachineTypeModel('Generic machine', '3U', None, None, 3))
    session.add(MachineTypeModel('Generic machine', '4U', None, None, 4))
    session.add(MachineTypeModel('Generic machine', '5U', None, None, 5))
    session.flush()

    #Machine = aliased(Equipment, name='machine')
    #Rack = aliased(Equipment, name='rack')

    #query_rack = session.query(Rack.id.label('id'),
                               #Rack.name.label('name'),
                               #TypeModel.size.label('size'),
                               #TypeModel.horizontal_space.label('horizontal_space'),
                               #Category.name.label('category'),
                               #sql.null().label('rack'),
                               #sql.null().label('base'),
                               #sql.null().label('hbase')
                               #).filter(Rack.type_model_id == TypeModel.id,
                                        #TypeModel.category_id == Category.id,
                                        #Rack.state_id == state_in_use.id,
                                        #Category.id == category_rack.id)

    #query_machine = session.query(Machine.id.label('id'),
                                  #Machine.name.label('name'),
                                  #TypeModel.size.label('size'),
                                  #TypeModel.horizontal_space.label('horizontal_space'),
                                  #Category.name.label('category'),
                                  #Rack.name.label('rack'),
                                  #MachineRack.base,
                                  #MachineRack.hbase
                                  #).filter(Machine.type_model_id == TypeModel.id,
                                           #TypeModel.category_id == Category.id,
                                           #Machine.state_id == state_in_use.id,
                                           #Rack.state_id == state_in_use.id,
                                           #MachineRack.machine_id == Machine.id,
                                           #MachineRack.rack_id == Rack.id
                                           #)
                                  #.order_by(MachineRack.base.desc(),
                                                      #collate(Machine.name, 'NOCASE'))

    #query = query_rack.union(query_machine)
    #query = aliased(query_union, name='all')
    #select_string = str(query.statement.compile().statement.compile(compile_kwargs = {"literal_binds": True}))
    #print select_string
    #session.execute("CREATE VIEW rackview AS "+select_string+";")

    session.commit()

def database_example(session):
    state_in_use = session.query(State).filter(State.name == IN_USE).first().id
    rack_11u = session.query(RackTypeModel).filter(RackTypeModel.size == 11).first().id
    rack_25u = session.query(RackTypeModel).filter(RackTypeModel.size == 25).first().id
    machine_1u = session.query(MachineTypeModel).filter(MachineTypeModel.size == 1).first().id
    machine_2u = session.query(MachineTypeModel).filter(MachineTypeModel.size == 2).first().id
    machine_5u = session.query(MachineTypeModel).filter(MachineTypeModel.size == 5).first().id

    elves = Rack('elves', rack_25u, state_in_use)
    men = Rack('men', rack_25u, state_in_use)
    dwarves = Rack('dwarves', rack_11u, state_in_use)
    session.add_all([elves, men, dwarves])
    session.flush()

    session.add(Machine('legolas', machine_1u, state_in_use, 25, None, elves.id))
    session.add(Machine('finwe', machine_2u, state_in_use, 20, None, elves.id))
    session.add(Machine('tuor', machine_2u, state_in_use, 17, None, elves.id))
    session.add(Machine('elros', machine_1u, state_in_use, 16, None, elves.id))
    session.add(Machine('turgon', machine_5u, state_in_use, 6, None, elves.id))
    session.add(Machine('galadriel', machine_5u, state_in_use, 1, None, elves.id))

    session.add(Machine('boromir', machine_1u, state_in_use, 20, None, men.id))
    session.add(Machine('aragorn', machine_2u, state_in_use, 15, None, men.id))
    session.add(Machine('faramir', machine_2u, state_in_use, 13, None, men.id))
    session.add(Machine('turin', machine_5u, state_in_use, 6, None, men.id))
    session.add(Machine('beren', machine_1u, state_in_use, 3, None, men.id))
    session.add(Machine('denethor', machine_1u, state_in_use, 2, None, men.id))

    session.add(Machine('hurin', machine_2u, state_in_use, 10, None, dwarves.id))
    session.add(Machine('bofur', machine_1u, state_in_use, 8, None, dwarves.id))
    session.add(Machine('thorin', machine_2u, state_in_use, 6, None, dwarves.id))
    session.add(Machine('oin', machine_1u, state_in_use, 4, None, dwarves.id))
    session.add(Machine('dori', machine_1u, state_in_use, 3, None, dwarves.id))
    session.add(Machine('balin', machine_1u, state_in_use, 2, None, dwarves.id))
    session.add(Machine('gloin', machine_1u, state_in_use, 1, None, dwarves.id))

    session.flush()
    session.commit()

def get_session():
    engine = create_engine('sqlite:///labadmin.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    return DBSession()

def rack_list():
    return session.query(Rack).order_by(Rack.sort, collate(Rack.name, 'NOCASE'))

def rack_type_model_list():
    return session.query(RackTypeModel).order_by(collate(RackTypeModel.name, 'NOCASE'), RackTypeModel.type_num, RackTypeModel.model_num)

def machine_list(id = '', sort = ''):
    return session.query(Machine).order_by(collate(Machine.name, 'NOCASE'))

session = get_session()
if session.query(State).count() == 0:
    database_init(session)
    database_example(session)

print ""
print "labadmin"
print "--------"
print "  equipments (total: %u):" % session.query(Equipment.id).count()
print "     racks....... %2u" % session.query(Rack.id).count()
print "     machines.... %2u" % session.query(Machine.id).count()
print "  type models (total: %u):" % session.query(TypeModel.id).count()
print "     racks ...... %2u" % session.query(RackTypeModel.id).count()
print "     machines ... %2u" % session.query(MachineTypeModel.id).count()
print "  brands ........ %2u" % session.query(Brand.id).count()
print "  states ........ %2u" % session.query(State.id).count()
print ""

column_name = 'name'
value = 'xavier'


print session.query(Rack).filter(id == 2)
#session.query(Rack).filter(id == 2).update({column_name: value})

for rack in rack_list():
    print rack.name




