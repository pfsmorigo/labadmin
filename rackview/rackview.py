#!/usr/bin/python

import sys
import svgwrite
import sqlite3 as sqlite
import os
import fileinput
import re

filename = os.path.dirname(os.path.realpath(__file__))+"/"+os.path.basename(sys.argv[0]).split('.')[0]

unit_size = 15
rack_width = unit_size*12
rack_title_size = unit_size*2
border_size = unit_size

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

    width = ((rack_base_width+unit_size)*rack_total)-unit_size+(border_size*2)
    height = rack_title_size+(rack_max_size*unit_size)+rack_base_height+(unit_size*2)+(border_size*2)

    dwg = svgwrite.Drawing(filename = filename+".svg", size = (width, height))
    #dwg.add_stylesheet(filename+".css", title = filename)

    shift = border_size

    cursor_rack.execute("SELECT name, size FROM rack ORDER BY sort")
    rack_rows = cursor_rack.fetchall()
    for rack_row in rack_rows:
        rack_name = rack_row[0]
        rack_size = rack_row[1]
        rack_height = ((rack_size*unit_size)+(border_size*2))

        rack = dwg.g(class_="rack")
        rack.add(dwg.text(rack_name,
                          insert = (shift+(unit_size*2)+(u_width/2),
                                    height-rack_height-(unit_size*2)-border_size),
                          class_ = "name"))
        rack.add(dwg.rect(insert = (shift+unit_size,
                                    height-rack_height-unit_size-border_size),
                          size = (rack_width, rack_height),
                          class_ = "body"))
        rack.add(dwg.rect(insert = (shift,
                                    height-unit_size-border_size),
                          size = (rack_base_width, rack_base_height),
                          class_ = "base"))

        for current_u in range(0, rack_size):
            rack_num_pos = height-rack_height-border_size-unit_size+((rack_size-current_u)*unit_size)
            rack.add(dwg.rect(insert = (shift+(unit_size*2),
                                        rack_num_pos),
                              size = (u_width, unit_size),
                              class_ = "slot"))
            rack.add(dwg.text(current_u+1,
                              insert = (shift+unit_size+(unit_size/2),
                                        rack_num_pos+(unit_size/2)),
                              class_ = "slot_number"))

        cursor_machine = con.cursor()
        cursor_machine.execute("SELECT id, name, base, hbase, size, hspace, model_name, type_model, serial FROM machine_list WHERE rack = ?", [(rack_row[0])])
        machine_rows = cursor_machine.fetchall()
        for machine_row in machine_rows:
            machine_id = machine_row[0]
            machine_name = machine_row[1]
            machine_base = rack_title_size+border_size+rack_height-rack_base_height-((machine_row[2]-1)*u_height)
            machine_hbase = machine_row[3]
            machine_size = machine_row[4]*u_height
            machine_hspace = machine_row[5]
            machine_model_name = str(machine_row[6])
            machine_type = str(machine_row[7].split('-',1)[0])
            machine_serial = str(machine_row[8])

            #print "%15s | %15s: %4.1f (%5.1f) %4.1f (%5.1f)" % (rack_name, machine_name, machine_row[1], machine_base, machine_row[2], machine_size)

            if machine_serial == "None":
                url_view = "/id/"+str(machine_id)
            else:
                url_view = "/serial/"+machine_serial

            machine = dwg.a(url_view, target = "_parent", class_ = "machine")

            base_horizontal = shift+(unit_size*2)+(u_width*machine_hbase)

            machine.add(dwg.rect(insert = (base_horizontal,
                                           machine_base-machine_size),
                                 size = (u_width*machine_hspace, machine_size),
                                 class_ = "body"))
            machine.add(dwg.text(machine_name,
                                 insert = (base_horizontal+((u_width*machine_hspace)/2),
                                           machine_base-(machine_size/2)),
                                 class_ = "title"))
            rack.add(machine)
        dwg.add(rack)
        shift += rack_base_width+unit_size

#print(dwg.tostring())
dwg.save()

with open (filename+".svg", "r") as myfile:
    svg_data=myfile.read()

with open (filename+".css", "r") as myfile:
    css_data=myfile.read()

css_prefix="\n<style type=\"text/css\" >\n<![CDATA[\n"
css_suffix="]]>\n</style>\n"

i = svg_data.find("<defs />")

output = open(filename+".svg", "w")
output.write(svg_data[:i]+css_prefix+css_data+css_suffix+svg_data[i:])
output.close()

print filename+".svg generated."
