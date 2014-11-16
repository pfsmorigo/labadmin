#!/bin/python

import sys
import sqlite3 as sqlite
import subprocess
from bottle import run, route, request, response, template, static_file

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
def main():
    subprocess.call(["python", "rackview/rackview.py", sys.argv[1]])
    db = sqlite.connect(sys.argv[1])
    c = db.cursor()
    c.execute("SELECT id, name, serial, rack_id, rack, model_id, model_name, type_model FROM machine_list ORDER BY name")
    machine_list = c.fetchall()
    db.close()
    output = template('default', view = 'list', machine_list = machine_list)
    return output

@route('/', method='POST')
def form_post():
    db = sqlite.connect(sys.argv[1])
    c = db.cursor()
    for attribute, value in request.forms.allitems():
        if value == "None": continue
        machine_id = attribute.split('_', 1)[0]
        column_name = attribute.split('_', 1)[1]
        query = "UPDATE machine SET %s = \"%s\" WHERE id = %s" % (column_name, value, machine_id)
        print query
        c.execute(query)
    db.commit()
    db.close()

@route('/<view>/<value>')
def main(view, value):
    db = sqlite.connect(sys.argv[1])
    c = db.cursor()
    c.execute("SELECT * FROM machine WHERE "+view+" = '"+value+"' ORDER BY name")
    machine_list = c.fetchall()
    c.execute("SELECT * FROM rack_list ORDER BY name")
    rack_list = c.fetchall()
    c.execute("SELECT * FROM machine_model ORDER BY name")
    machine_model_list = c.fetchall()
    db.close()
    output = template('default', view = view, value = value,
                      machine_list = machine_list,
                      rack_list = rack_list,
                      machine_model_list = machine_model_list)
    return output

run(host='localhost', port=8080, debug=True)
