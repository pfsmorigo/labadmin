% rebase('base.tpl', title='machines')
		<div id="menu">
%if view == "edit":
			<div style="float: right">
				<a href="#" onclick="document.machine.submit();">done</a>
				<a href="/machine">cancel</a>
			</div>
%end
			<a href="/machine"{{!' class="current"' if view == '' else ''}}>list</a>
			<a href="/machine/edit"{{!' class="current"' if view == 'edit' else ''}}>edit</a>
		</div>
		<h2>Machines by {{sort}} (Total: {{len(machine_list)-1}})</h2>
%if view == "edit":
		<form method="POST" id="machine" action="/">
			<table id="details">
				<tr>
					<th>Remove</th>
					<th>Name</th>
					<th>Model</th>
					<th>Serial</th>
					<th>Unit Value</th>
					<th>Invoice</th>
					<th>Capitalization date</th>
					<th>Rack</th>
					<th>U Base</th>
					<th>H Base</th>
				</tr>
	%for machine in machine_list:
				<tr{{!' class="new"' if machine[0] == 'new' else ''}}>
		%if machine[0] != 'new':
					<td><input type="checkbox" name="{{machine[0]}}_del" value="1"></td>
		%else:
					<th>New</th>
		%end
					<td><input type="text" class="name" name="{{machine[0]}}_name" value="{{machine[1]}}" /></td>
					<td>
						<select class="model" name="{{machine[0]}}_model" form="machine">
		%for machine_model in machine_model_list:
<%
type_num = str(machine_model[3])
model_num = str(machine_model[4])

type_model = type_num if model_num == '' else type_num+'-'+model_num
%>
						    <option value="{{machine_model[0]}}"{{!' selected="selected"' if machine_model[0] == machine[2] else ''}}>{{machine_model[1]}} ({{type_model}})</option>
		%end
						</select>
					</td>
					<td><input type="text" class="serial" name="{{machine[0]}}_serial" value="{{machine[9]}}" /></td>
					<td><input type="text" class="unit_value" name="{{machine[0]}}_unit_value" value="{{machine[10]}}" /></td>
					<td><input type="text" class="invoice" name="{{machine[0]}}_invoice" value="{{machine[11]}}" /></td>
					<td><input type="text" class="cap_date" name="{{machine[0]}}_cap_date" value="{{machine[12]}}" /></td>
					<td>
						<select class="rack" name="{{machine[0]}}_rack" form="machine">
							<option value="0">None</option>
		%for rack in rack_list:
						    <option value="{{rack[0]}}"{{!' selected="selected"' if rack[0] == machine[13] else ''}}>{{rack[1]}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="base" name="{{machine[0]}}_base" value="{{machine[17]}}" /></td>
					<td><input type="text" class="baseh" name="{{machine[0]}}_hbase" value="{{machine[18]}}" /></td>
				</tr>
	%end

			</table>
		</form>
%else:
		<table id="machine_list">
			<tr>
				<th><a href="/machine">Machine {{!'&#9650;' if sort == 'name' else ''}}</a></th>
				<th><a href="/machine_by_model">Model{{!' &#9650;' if sort == 'model' else ''}}</a></th>
				<th><a href="/machine_by_serial">Serial{{!' &#9650;' if sort == 'serial' else ''}}</a></th>
				<th><a href="/machine_by_unit_value">Unit Value{{!' &#9650;' if sort == 'unit_value' else ''}}</a></th>
				<th><a href="/machine_by_invoice">Invoice{{!' &#9650;' if sort == 'invoice' else ''}}</a></th>
				<th><a href="/machine_by_cap_date">Cap. Date{{!' &#9650;' if sort == 'cap_date' else ''}}</a></th>
				<th><a href="/machine_by_size">Size{{!' &#9650;' if sort == 'size' else ''}}</a></th>
				<th colspan="2"><a href="/machine_by_location">Location{{!' &#9650;' if sort == 'location' else ''}}</a></th>
			</tr>
			%for machine in machine_list[:-1]:
<%
size = '{:g}'.format(float(machine[7]))
base = str('{:g}'.format(float(machine[17])))
uvalue = base if size == '1' else base+' - '+str('{:g}'.format(float(machine[17]+machine[7]-1)))
type_num = machine[5]
model_num = machine[6]
type_model = type_num if model_num == '' else type_num+'-'+model_num
%>
			<tr>
				<td><a href="/id/{{machine[0]}}">{{machine[1]}}</a></td>
				<td><a href="/model/{{machine[2]}}">{{machine[3]}} ({{type_model}})</a></td>
				<td><a href="/serial/{{machine[9]}}">{{machine[9]}}</a></td>
				<td><a href="/unit_value/{{machine[10]}}">{{machine[10]}}</a></td>
				<td><a href="/invoice/{{machine[11]}}">{{machine[11]}}</a></td>
				<td><a href="/cap_date/{{machine[12]}}">{{machine[12]}}</a></td>
				<td style="text-align: right"><a href="/size/{{size}}">{{size}}U</a></td>
				<td><a href="/rack/{{machine[13]}}"{{!'' if machine[14] != 1 else ' class="deleted"'}}>{{!machine[14] if machine[13] != 0 else 'None'}}</a></td>
				<td style="text-align: center"><a href="/rack/{{machine[13]}}"{{!'' if machine[14] != 1 else ' class="deleted"'}}>{{!uvalue if machine[13] != 0 else '-'}}</a></td>
			</tr>
			%end
		</table>
%end
