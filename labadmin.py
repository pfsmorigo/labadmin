#!/bin/python

import sys
import subprocess
import commands
from bottle import run, route, request, response, template, static_file, redirect, error
from database import *

session = get_session()

info = {
    "name"     : "labadmin",
    "version"  : commands.getstatusoutput('git describe --abbrev=0 --tags')[1],
    "racks"    : session.query(Rack.id).count(),
    "machines" : session.query(Machine.id).count()
}

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
def url_redirect():
    redirect("/rack")

@route('/rack')
def rack_view():
    return rack()

@route('/rack', method='POST')
def rack_post():
    new_name = ''
    new_size = ''
    new_order = ''
    for attribute, value in request.forms.allitems():
        if value == "None":
            continue
        item_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]
        if item_id == "new":
            if column_name == 'name':
                new_name = value
            if column_name == 'size':
                try:
                    new_size = int(value)
                except ValueError:
                    print "ERROR: Invalid size value (%s)." % value
            if column_name == 'sort':
                try:
                    new_sort = int(value)
                except ValueError:
                    print "ERROR: Invalid sort value (%s)." % value
        else:
            db.query("UPDATE rack SET %s = \"%s\" WHERE id = %s" % (column_name, value, item_id))
    if new_name and new_size and new_sort:
        db.query("INSERT INTO rack VALUES(NULL, '%s', %d, %d, 0)" % (new_name, new_size, new_sort))
    return rack()

@route('/rack/edit')
def rack_edit():
    return rack('edit')

def rack(view = ''):
    subprocess.call(["python", "rackview/rackview.py", "labadmin.db"])
    return template('rack', info = info, view = view, rack_list = rack_list(session))

@route('/machine')
def machine_edit():
    return machine()

@route('/machine', method='POST')
def machine_post():
    for attribute, value in request.forms.allitems():
        if value == "None":
            continue
        item_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]
        if item_id == "new":
            print "new: "+item_id+" - "+column_name+" - "+value
        else:
            db.query("UPDATE machine SET %s = \"%s\" WHERE id = %s" % (column_name, value, item_id))
    return machine()

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

def machine(view = '', id = '', sort = ''):
    query = "SELECT * FROM machine_list"
    if id:
            query += ' WHERE id = '+id
    if sort:
        if sort == 'model':
            query += ' ORDER BY model_name'
        elif sort == 'location':
            query += ' ORDER BY rack_id = 0, rack_sort, base DESC'
        else:
            query += ' ORDER BY '+sort
    machine_list = db.query(query).fetchall()
    machine_list.append(['new', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    rack_list = db.query("SELECT * FROM rack_list").fetchall()
    machine_model_list = db.query("SELECT * FROM machine_model ORDER BY name").fetchall()
    output = template('machine', info = info, view = view, sort = sort,
                      machine_list = machine_list,
                      rack_list = rack_list,
                      machine_model_list = machine_model_list)
    return output

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

def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))

run(host='0.0.0.0', port = 8080, debug = True)
