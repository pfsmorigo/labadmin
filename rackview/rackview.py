#!/usr/bin/python

import sys
import svgwrite
import sqlite3 as sqlite
import os.path

filename = os.path.basename(sys.argv[0]).split('.')[0]

unit_size = 10
rack_total_u = 42

rack_width = 150
rack_height = ((rack_total_u*10)+20)

rack_base_width = rack_width+(unit_size*2)
rack_base_height = unit_size

u_width = rack_width-(unit_size*2)
u_height = unit_size

height = rack_height+rack_base_height+(unit_size*2)
width = rack_base_width+(unit_size*2)

dwg = svgwrite.Drawing(filename = filename+".svg", size = (width, height))
dwg.add_stylesheet(filename+".css", title = filename)

rack = dwg.g(class_="rack")
rack.add(dwg.rect(insert = (0, height-unit_size),
                  size = (rack_base_width, rack_base_height)))
rack.add(dwg.rect(insert = (unit_size, height-rack_height-unit_size),
                  size = (rack_width, rack_height)))

for current_u in range(0, rack_total_u):
    rack_num_pos = height-rack_height-unit_size+((rack_total_u-current_u)*unit_size)
    rack.add(dwg.rect(insert = (unit_size*2, rack_num_pos),
                      size = (u_width, unit_size)))
    rack.add(dwg.text(current_u+1, insert = (unit_size+(unit_size/2),
                      rack_num_pos+(unit_size/2)),
                      class_ = "rack_number"))

print 'Number of arguments:', len(sys.argv), 'arguments.'

if len(sys.argv) == 2:
    con = sqlite.connect(sys.argv[1])
    cursor = con.cursor()
    cursor.execute('''SELECT * FROM machine_list''')
    all_rows = cursor.fetchall()
    for row in all_rows:
        machine_name = row[0]
        machine_size = row[2]*u_height
        machine_base = (rack_height+unit_size)-((row[1]-1)*u_height)

        print "%15s: %4.1f (%5.1f) %4.1f (%5.1f)" % (machine_name, row[1], machine_base, row[2], machine_size)

        #if not "baboon" in machine_name:
            #continue

        machine = dwg.g(class_="machine")
        machine.add(dwg.rect(insert = (unit_size*2, machine_base-machine_size),
                             size = (u_width, machine_size)))
        machine.add(dwg.text(machine_name,
                             insert = ((unit_size*2)+(u_width/2),
                                       machine_base-(machine_size/2))))
        rack.add(machine)

dwg.add(rack)

#print(dwg.tostring())

dwg.save()
