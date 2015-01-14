#!/bin/python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Date
from sqlalchemy import create_engine, event, func, collate, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, aliased

Base = declarative_base()

IN_USE = "In use";
NOT_IN_USE = "Not in use";
DISPOSED = "Disposed";
INVALID = "Invalid";

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    type_model_id = Column(Integer, ForeignKey('type_model.id'))
    state_id = Column(Integer, ForeignKey('state.id'))

    type_model = relationship('TypeModel')
    state = relationship('State')

    def __init__(self, name, type_model_id, state_id):
        self.name = name
        self.type_model_id = type_model_id
        self.state_id = state_id

    def __repr__(self):
        return "<Equipment('%s')>" % self.name

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

class EquipmentFieldType(Base):
    __tablename__ = 'equipment_field_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<EquipmentFieldType('%s')>" % self.name

class EquipmentField(Base):
    __tablename__ = 'equipment_field'
    id = Column(Integer, primary_key = True)
    description = Column(String(250), nullable = False)
    equipment_id = Column(Integer, ForeignKey('equipment.id'))

    def __init__(self, description, equipment_id):
        self.description = description
        self.equipment_id = equipment_id

    def __repr__(self):
        return "<EquipmentFieldType('%s')>" % self.description

class TypeModel(Base):
    __tablename__ = 'type_model'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    type_num = Column(String(100), nullable = True)
    model_num = Column(String(100), nullable = True)
    size = Column(Float, nullable = True)
    horizontal_space = Column(Float, nullable = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    brand_id = Column(Integer, ForeignKey('brand.id'))

    def __init__(self, name, type_num, model_num, size, horizontal_space,
            category_id, brand_id):
        self.name = name
        self.type_num = type_num
        self.model_num = model_num
        self.size = size
        self.horizontal_space = horizontal_space
        self.category_id = category_id
        self.brand_id = brand_id

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

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category('%s')>" % self.name

class MachineRack(Base):
    __tablename__ = 'machine_rack'
    id = Column(Integer, primary_key = True)
    base = Column(Float, nullable = True)
    hbase = Column(Float, nullable = True)
    machine_id = Column(Integer, ForeignKey('equipment.id'))
    rack_id = Column(Integer, ForeignKey('equipment.id'))

    def __init__(self, base, hbase, machine_id, rack_id):
        self.base = base
        self.hbase = hbase
        self.machine_id = machine_id
        self.rack_id = rack_id

    def __repr__(self):
        return "<MachineRack('%u, %u')>" % (self.machine_id, self.rack_id)

class RackOrder(Base):
    __tablename__ = 'rack_order'
    id = Column(Integer, primary_key = True)
    sort = Column(Integer, nullable = False)
    rack_id = Column(Integer, ForeignKey('equipment.id'))

    def __init__(self, sort, rack_id):
        self.sort = sort
        self.rack_id = rack_id

    def __repr__(self):
        return "<RackOrder('%s')>" % self.sort

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
    session.add_all([State(IN_USE), State(NOT_IN_USE), State(DISPOSED), State(INVALID)])

    category_rack = Category('Rack')
    category_machine = Category('Machine')
    session.add_all([category_rack, category_machine])
    session.flush()

    session.add(TypeModel('Generic rack', '11U', None, 11, None, category_rack.id, None))
    session.add(TypeModel('Generic rack', '25U', None, 25, None, category_rack.id, None))
    session.add(TypeModel('Generic rack', '42U', None, 42, None, category_rack.id, None))
    session.add(TypeModel('Generic machine', '1U', None, 1, None, category_machine.id, None))
    session.add(TypeModel('Generic machine', '2U', None, 2, None, category_machine.id, None))
    session.add(TypeModel('Generic machine', '3U', None, 3, None, category_machine.id, None))
    session.add(TypeModel('Generic machine', '4U', None, 4, None, category_machine.id, None))
    session.add(TypeModel('Generic machine', '5U', None, 5, None, category_machine.id, None))
    session.flush()

    #select_string = str(rack_list(session).statement.compile(compile_kwargs = {"literal_binds": True}))
    #session.execute("CREATE VIEW rackview_racks AS "+select_string+";")

#SELECT machine.*, machine_typemodel.name AS typemodel_name, machine_typemodel.type_num,
#machine_typemodel.model_num AS model_num,
                    #machine_typemodel.size AS size,
                    #machine_typemodel.horizontal_space
                #FROM machine, machine_typemodel
                #WHERE machine.typemodel_id = machine_typemodel.id
                #ORDER BY machine.name COLLATE NOCASE ASC

    #session.execute("""
            #CREATE VIEW "rackview_machines" AS SELECT
                    #machine.id AS id,
                    #machine.name,
                    #machine_typemodel.id AS typemodel_id,
                    #machine_typemodel.name AS model_name,
                    #machine_typemodel.category_id AS category_id,
                    #machine_typemodel.type_num AS type_num,
                    #machine_typemodel.model_num AS model_num,
                    #machine_typemodel.size AS size,
                    #machine_typemodel.horizontal_space AS hspace,
                    #machine.serial AS serial,
                    #machine.unit_value AS unit_value,
                    #machine.invoice AS invoice,
                    #machine.cap_date AS cap_date,
                    #machine.rack_id AS rack_id,
                    #rack.name AS rack_name,
                    #rack.sort AS rack_sort,
                    #rack.state_id AS rack_state_id,
                    #machine.base,
                    #machine.hbase,
                    #machine.state_id
                #FROM machine, machine_typemodel
                #LEFT OUTER JOIN rack
                #WHERE (machine.rack_id IS 0 OR machine.rack_id = rack.rowid)
                #AND machine.typemodel_id = machine_typemodel.id
                #GROUP BY machine.id
                #ORDER BY machine.name COLLATE NOCASE ASC;
            #""")

    session.commit()

def database_example(session):
    state_in_use = session.query(State).filter(State.name == IN_USE).first().id
    rack = session.query(Category).filter(Category.name == 'Rack').first().id
    rack_11u = session.query(TypeModel).filter(TypeModel.category_id == rack, TypeModel.size == 11).first().id
    rack_25u = session.query(TypeModel).filter(TypeModel.category_id == rack, TypeModel.size == 25).first().id
    machine = session.query(Category).filter(Category.name == 'Machine').first().id
    machine_1u = session.query(TypeModel).filter(TypeModel.category_id == machine, TypeModel.size == 1).first().id
    machine_2u = session.query(TypeModel).filter(TypeModel.category_id == machine, TypeModel.size == 2).first().id
    machine_5u = session.query(TypeModel).filter(TypeModel.category_id == machine, TypeModel.size == 5).first().id

    elves = Equipment('elves', rack_25u, state_in_use)
    legolas = Equipment('legolas', machine_1u, state_in_use)
    finwe = Equipment('finwe', machine_1u, state_in_use)
    celeborn = Equipment('celeborn', machine_1u, state_in_use)
    tuor = Equipment('tuor', machine_1u, state_in_use)
    elros = Equipment('elros', machine_1u, state_in_use)
    turgon = Equipment('turgon', machine_1u, state_in_use)
    galadriel = Equipment('galadriel', machine_1u, state_in_use)

    men = Equipment('men', rack_25u, state_in_use)
    boromir = Equipment('boromir', machine_1u, state_in_use)
    aragorn = Equipment('aragorn', machine_1u, state_in_use)
    faramir = Equipment('faramir', machine_1u, state_in_use)
    turgon = Equipment('turgon', machine_1u, state_in_use)
    turin = Equipment('turin', machine_1u, state_in_use)
    beren = Equipment('beren', machine_1u, state_in_use)
    denethor = Equipment('denethor', machine_1u, state_in_use)

    dwarves = Equipment('dwarves', rack_11u, state_in_use)
    hurin = Equipment('hurin', machine_1u, state_in_use)
    egalmoth = Equipment('egalmoth', machine_1u, state_in_use)
    bofur = Equipment('bofur', machine_1u, state_in_use)
    thorin = Equipment('thorin', machine_1u, state_in_use)
    oin = Equipment('oin', machine_1u, state_in_use)
    dori = Equipment('dori', machine_1u, state_in_use)
    balin = Equipment('balin', machine_1u, state_in_use)
    gloin = Equipment('gloin', machine_1u, state_in_use)

    session.add_all([elves, legolas, finwe, celeborn, tuor, elros, turgon, galadriel,
                     men, boromir, aragorn, faramir, turgon, turin, beren, denethor,
                     dwarves, hurin, egalmoth, bofur, thorin, oin, dori, balin, gloin])
    session.flush()

    session.add(MachineRack(1, None, legolas.id, elves.id))
    session.add(MachineRack(2, None, finwe.id, elves.id))
    session.add(MachineRack(3, None, celeborn.id, elves.id))
    session.add(MachineRack(4, None, tuor.id, elves.id))
    session.add(MachineRack(5, None, elros.id, elves.id))
    session.add(MachineRack(6, None, turgon.id, elves.id))
    session.add(MachineRack(7, None, galadriel.id, elves.id))

    session.add(MachineRack(1, None, boromir.id, men.id))
    session.add(MachineRack(1, None, aragorn.id, men.id))
    session.add(MachineRack(1, None, faramir.id, men.id))
    session.add(MachineRack(1, None, turgon.id, men.id))
    session.add(MachineRack(1, None, turin.id, men.id))
    session.add(MachineRack(1, None, beren.id, men.id))
    session.add(MachineRack(1, None, denethor.id, men.id))

    session.add(MachineRack(1, None, hurin.id, dwarves.id))
    session.add(MachineRack(1, None, egalmoth.id, dwarves.id))
    session.add(MachineRack(1, None, bofur.id, dwarves.id))
    session.add(MachineRack(1, None, thorin.id, dwarves.id))
    session.add(MachineRack(1, None, oin.id, dwarves.id))
    session.add(MachineRack(1, None, dori.id, dwarves.id))
    session.add(MachineRack(1, None, balin.id, dwarves.id))
    session.add(MachineRack(1, None, gloin.id, dwarves.id))

    session.commit()

def get_session():
    engine = create_engine('sqlite:///labadmin.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    return DBSession()

#def rack_list(session):
    #query = session.query(Rack).filter(Rack.state_id == 1).order_by(Rack.sort, collate(Rack.name, 'NOCASE'))
    ##print str(query.statement.compile())
    #return query

#def machine_typemodel_list(session):
    #query = session.query(TypeModel).order_by(collate(TypeModel.name, 'NOCASE'))
    #return query

#def machine_list(session, id = '', sort = ''):
    #query = session.query(Machine).order_by(collate(Machine.name, 'NOCASE'))
    #return query

session = get_session()
if session.query(State).count() == 0:
    database_init(session)
    database_example(session)

print ""
print "labadmin"
print "--------"
print "  equipments ... %2u" % session.query(Equipment.id).count()
print "  type models .. %2u" % session.query(TypeModel.id).count()
print "  categories ... %2u" % session.query(Category.id).count()
print "  brands ....... %2u" % session.query(Brand.id).count()
print "  states ....... %2u" % session.query(State.id).count()
print ""
