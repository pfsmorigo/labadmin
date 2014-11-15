#!/bin/python

import sys
import sqlite3 as sqlite
import subprocess
from bottle import run, route, request, response, template, static_file

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
#@route('/<name>')
def main():
    subprocess.call(["python", "rackview/rackview.py", sys.argv[1]])
    db = sqlite.connect(sys.argv[1])
    c = db.cursor()
    c.execute("SELECT machine,rack,description,type_model,serial FROM machine_list ORDER BY machine")
    data = c.fetchall()
    c.close()
    output = template('default', rows=data)
    return output

run(host='localhost', port=8080, debug=True)
