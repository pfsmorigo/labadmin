#!/bin/python

import sys
import subprocess
import commands
import datetime
from bottle import run, route, request, response, template, static_file, redirect, error
from database import *
from types import IntType, FloatType

session = get_session()

info = {
    "name"     : "labadmin",
    "version"  : commands.getstatusoutput('git describe --abbrev=0 --tags')[1],
    "racks"    : rack_list().count(),
    "machines" : machine_list().count()
}

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
def url_redirect():
    redirect("/rack")

@route('/rack')
def rack(view = ''):
    subprocess.call(["python", "rackview/rackview.py", "labadmin.db"])
    return template('rack', info = info, view = view, rack_list = rack_list())

@route('/rack/edit')
def rack_edit():
    return rack('edit')

@route('/rack', method='POST')
def rack_post():
    new = {}
    for attribute, value in request.forms.allitems():
        if value == "None":
            continue

        item_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]

        if item_id != "new":
            print "db update: rack, %s, %s, %s." % (item_id, column_name, value)
            session.query(Rack).filter_by(id = item_id).update({column_name: value})
            session.commit()
        else:
            if value:
                new[column_name] = value
            else:
                new[column_name] = None

    if new['name'] and new['size']:
        print "db insert: machine: %s" % new
        session.add(Rack(new['name'], new['size'], new['sort'], 1))
        session.commit()

    return rack()

@route('/machine')
def machine(view = '', id = '', sort = ''):
    return template('machine', info = info, view = view, sort = sort,
            machine_list = machine_list(session, id, sort),
            rack_list = rack_list(session),
            machine_typemodel_list = machine_typemodel_list(session))

@route('/machine/edit')
def machine_edit():
    return machine(view = 'edit')

@route('/machine/id/<id>')
def machine_id(id):
    return machine(id = id)

@route('/machine/id/<id>/edit')
def machine_id_edit(id):
    return machine(id = id, view = 'edit')

@route('/machine_by_<sort>')
def machine_sort(sort):
    return machine(sort = sort)

@route('/machine_by_<sort>/edit')
def machine_sort_edit(sort):
    return machine(sort = sort, view = 'edit')

@route('/machine', method='POST')
def machine_post():
    new = {}
    for attribute, value in request.forms.allitems():
        print '%s -> %s' % ( attribute, value)
        if value == 'None':
            continue

        item_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]

        if item_id != "new":
            print "db update: machine, %s, %s, %s." % (item_id, column_name, value)
            session.query(Machine).filter_by(id = item_id).update({column_name: value})
            session.commit()
        else:
            if value:
                if column_name == 'cap_date':
                    new[column_name] = datetime.date(value)
                else:
                    new[column_name] = value
            else:
                new[column_name] = None

    if new['name'] and new['model_id']:
        print "db insert: rack, %s" % new
        session.add(Machine(new['name'], new['serial'], new['unit_value'], new['invoice'],
                            new['cap_date'], new['base'], new['hbase'], new['rack_id'],
                            new['model_id'], 1))
        session.commit()

    return machine()

@route('/configuration')
@route('/configuration/<subject>')
def configuration(subject = ""):
    if subject == 'brand':
        result = db.query("SELECT * FROM machine_brand").fetchall()
    elif subject == 'rack_model':
        result = db.query("SELECT * FROM model_type").fetchall()
    elif subject == 'machine_model':
        result = db.query("SELECT * FROM machine_model").fetchall()
    else:
        result = ""
    output = template('configuration', info = info, subject = "", result = result)
    return output

@route('/about')
def about(view = 'about'):
    return template('about', info = info, view = view)

@error(404)
@error(500)
def error(error):
    return template('error', info = info, error = error)

def convert(value, var_type):
    try:
        if var_type == IntType:
            return int(value)
        elif var_type == FloatType:
            return float(value)
    except ValueError:
        print "invalid size value (%s)." % value

def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))

run(host='0.0.0.0', port = 8080, debug = True)
