#!/bin/python

import sys
import subprocess
import commands
from bottle import run, route, request, response, template, static_file, redirect, error
from classes.database import DatabaseManager

db = DatabaseManager(sys.argv[1], True)

info = {
    "name"     : "labadmin",
    "version"  : commands.getstatusoutput('git describe --abbrev=0 --tags')[1],
    "racks"    : db.query("SELECT COUNT(*) FROM rack_list").fetchone()[0],
    "machines" : db.query("SELECT COUNT(*) FROM machine_list").fetchone()[0]
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
def form_post():
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
    subprocess.call(["python", "rackview/rackview.py", sys.argv[1]])
    rack_list = db.query("SELECT id, name, size, sort, used FROM rack_list").fetchall()
    rack_list.append(['new', '', '', '', ''])
    output = template('rack', info = info, view = view, rack_list = rack_list)
    return output

@route('/machine')
def machine_edit():
    return machine()

@route('/machine/by/model')
def machine_edit():
    return machine(sort = "model_name")

@route('/machine/by/serial')
def machine_edit():
    return machine(sort = "serial")

@route('/machine/by/size')
def machine_edit():
    return machine(sort = "size")

@route('/machine/by/rack')
def machine_edit():
    return machine(sort = "rack_name")

@route('/machine/edit')
def machine_edit():
    return machine(view = 'edit')

def machine(view = '', sort = ''):
    if sort:
        sort = " ORDER BY "+sort
    machine_list = db.query("SELECT id, name, model_id, model_name, type_model, size, serial, rack_id, rack_name, rack_del FROM machine_list"+sort).fetchall()
    machine_list.append(['new', '', '', '', '', '', '', '', ''])
    output = template('machine', info = info, view = view, machine_list = machine_list)
    return output

@route('/', method='POST')
def form_post():
    for attribute, value in request.forms.allitems():
        if value == "None": continue
        machine_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]
        db.query("UPDATE machine SET %s = \"%s\" WHERE id = %s" % (column_name, value, machine_id))

@route('/<view>/<value>')
def views(view, value):
    machine_list = db.query("SELECT * FROM machine WHERE "+view+" = '"+value+"' ORDER BY name").fetchall()
    rack_list = db.query("SELECT * FROM rack_list").fetchall()
    machine_model_list = db.query("SELECT * FROM machine_model ORDER BY name").fetchall()
    output = template('details', view = view, info = info, value = value,
                      machine_list = machine_list,
                      rack_list = rack_list,
                      machine_model_list = machine_model_list)
    return output

@route('/configuration')
@route('/configuration/brand')
@route('/configuration/rack_model')
@route('/configuration/machine_model')
def configuration():
    output = template('configuration', info = info)
    return output

@route('/about')
def about():
    return template('about', info = info)

@error(404)
@error(500)
def error(error):
    return template('error', info = info, error = error)

def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

run(host='0.0.0.0', port=8080, debug=True)
