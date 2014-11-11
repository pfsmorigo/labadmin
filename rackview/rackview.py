#!/usr/bin/python

import sys
import svgwrite
import sqlite3 as sqlite
import os.path

filename = os.path.basename(sys.argv[0]).split('.')[0]

unit_size = 10
rack_width = 150

rack_base_width = rack_width+(unit_size*2)
rack_base_height = unit_size

u_width = rack_width-(unit_size*2)
u_height = unit_size

if len(sys.argv) == 2:
    con = sqlite.connect(sys.argv[1])
    cursor_rack = con.cursor()
    cursor_rack.execute("SELECT COUNT(name),MAX(size) FROM rack")
    rack_info = cursor_rack.fetchall()
    rack_total = rack_info[0][0]
    rack_max_size = rack_info[0][1]

    width = (rack_base_width+(unit_size*2))*rack_total
    height = (rack_max_size*unit_size)+rack_base_height+(unit_size*2)

    dwg = svgwrite.Drawing(filename = filename+".svg", size = (width, height))
    dwg.add_stylesheet(filename+".css", title = filename)

    shift = 0

    cursor_rack.execute("SELECT * FROM rack")
    rack_rows = cursor_rack.fetchall()
    for rack_row in rack_rows:
        rack_name = rack_row[0]
        rack_size = rack_row[1]
        rack_height = ((rack_size*unit_size)+20)

        rack = dwg.g(class_="rack")
        rack.add(dwg.rect(insert = (shift, height-unit_size),
                          size = (rack_base_width, rack_base_height)))
        rack.add(dwg.rect(insert = (shift+unit_size, height-rack_height-unit_size),
                          size = (rack_width, rack_height)))

        for current_u in range(0, rack_size):
            rack_num_pos = height-rack_height-unit_size+((rack_size-current_u)*unit_size)
            rack.add(dwg.rect(insert = (shift+(unit_size*2), rack_num_pos),
                              size = (u_width, unit_size)))
            rack.add(dwg.text(current_u+1, insert = (shift+unit_size+(unit_size/2),
                              rack_num_pos+(unit_size/2))))

        cursor_machine = con.cursor()
        cursor_machine.execute("SELECT * FROM machine_list where rack = ?", [(rack_row[0])])
        machine_rows = cursor_machine.fetchall()
        for machine_row in machine_rows:
            machine_name = machine_row[0]
            machine_size = machine_row[2]*u_height
            machine_base = rack_height-rack_base_height-((machine_row[1]-1)*u_height)

            print "%15s | %15s: %4.1f (%5.1f) %4.1f (%5.1f)" % (rack_name, machine_name, machine_row[1], machine_base, machine_row[2], machine_size)

            machine = dwg.g(class_="machine")
            machine.add(dwg.rect(insert = (shift+(unit_size*2), machine_base-machine_size),
                                 size = (u_width, machine_size)))
            machine.add(dwg.text(machine_name,
                                 insert = (shift+(unit_size*2)+(u_width/2),
                                           machine_base-(machine_size/2))))
            rack.add(machine)
        dwg.add(rack)
        shift += rack_base_width

#print(dwg.tostring())
dwg.save()
