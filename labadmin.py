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
    "name"    : "labadmin",
    "version" : commands.getstatusoutput('git describe --abbrev=0 --tags')[1],
    "areas"   : [ "rack", "machine" ]
}

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
def url_redirect():
    redirect("/rack")

@route('/<area>')
@route('/<area>/<view>')
@route('/<area>/<view>/<item>')
def page(area, view = '', item = ''):
    info['area'] = area
    info['view'] = view
    info['item'] = item
    info['sort'] = 'name' # default sort is by name

    if area == "rack":
        subprocess.call(["python", "rackview/rackview.py", "labadmin.db"])
        info['rack_list'] = rack_list()
        info['rack_type_model_list'] = rack_type_model_list()
        info['brand_list'] = brand_list()

    if area == "machine":
        if view.startswith('by_'):
            info['sort'] = view[3:]
        info['rack_list'] = rack_list()
        info['machine_list'] = machine_list(item, info['sort'])
        info['machine_type_model_list'] = machine_type_model_list()

    return template(area, info = info)

@route('/<area>', method='POST')
@route('/<area>/<view>', method='POST')
@route('/<area>/<view>/<item>', method='POST')
def page_post(area, view = '', item = ''):
    if area == "rack" and view == "":
        new = {}
        for attribute, value in request.forms.allitems():
            if value == "None":
                continue

            item_id = attribute.split('_', 1)[0]
            column_name = attribute.split('_', 1)[1]

            if item_id != "new":
                print "db update, rack id %s: %s = %s" % (item_id, column_name, value)

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

    if area == "rack" and view == "brand":
        new = {}
        for attribute, value in request.forms.allitems():
            if value == "None":
                continue

            item_id = attribute.split('_', 1)[0]
            column_name = attribute.split('_', 1)[1]

            if column_name == "del":
                print "db delete, brand id %s" % item_id
                session.query(Brand).filter_by(id = item_id).delete()
                session.commit()
                continue

            if item_id != "new":
                print "db update, brand id %s: %s = %s" % (item_id, column_name, value)

                session.query(Brand).filter_by(id = item_id).update({column_name: value})
                session.commit()
            else:
                if value:
                    new[column_name] = value
                else:
                    new[column_name] = None

        if new['name']:
            print "db insert: brand: %s" % new
            session.add(Brand(new['name']))
            session.commit()

    return page(area, view, item)

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
            print "db update, machine id %s: %s = %s" % (item_id, column_name, value)
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

@error(404)
@error(500)
def error(error):
    info['error'] = error
    return template('error', info = info)

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
