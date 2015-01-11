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
		<h2>Machines by {{sort}} (Total: {{machine_list.count()}})</h2>
%if view == "edit":
		<form method="POST" name="machine" action="/machine">
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
				<tr>
					<td><input type="checkbox" name="{{machine.id}}_del" value="1"></td>
					<td><input type="text" class="name" name="{{machine.id}}_name" value="{{machine.name}}" /></td>
					<td>
						<select class="model" name="{{machine.id}}_model" form="machine">
		%for machine_model in machine_model_list:
<%
type_num = str(machine_model[3])
model_num = str(machine_model[4])

type_model = type_num if model_num == '' else type_num+'-'+model_num
%>
						    <option value="{{machine_model.id}}"{{!' selected="selected"' if machine_model.id == machine.model_id else ''}}>{{machine_model.name}} ({{type_model}})</option>
		%end
						</select>
					</td>
					<td><input type="text" class="serial" name="{{machine.id}}_serial" value="{{machine.serial}}" /></td>
					<td><input type="text" class="unit_value" name="{{machine.id}}_unit_value" value="{{machine.unit_value}}" /></td>
					<td><input type="text" class="invoice" name="{{machine.id}}_invoice" value="{{machine.invoice}}" /></td>
					<td><input type="text" class="cap_date" name="{{machine.id}}_cap_date" value="{{machine.cap_date}}" /></td>
					<td>
						<select class="rack" name="{{machine.id}}_rack" form="machine">
							<option value="0">None</option>
		%for rack in rack_list:
						    <option value="{{rack.id}}"{{!' selected="selected"' if rack.id == machine.rack_id else ''}}>{{rack.name}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="base" name="{{machine.id}}_base" value="{{machine.base}}" /></td>
					<td><input type="text" class="baseh" name="{{machine.id}}_hbase" value="{{machine.hbase}}" /></td>
				</tr>
	%end
				<tr class="new">
					<th>New</th>
					<td><input type="text" class="name" name="new_name" /></td>
					<td>
						<select class="model" name="new_model" form="machine">
		%for machine_model in machine_model_list:
<%
type_model = machine_model.type_num if machine_model.model_num == '' else machine_model.type_num+'-'+machine_model.model_num
%>
						    <option value="{{machine_model.id}}">{{machine_model.name}} ({{type_model}})</option>
		%end
						</select>
					</td>
					<td><input type="text" class="serial" name="new_serial" /></td>
					<td><input type="text" class="unit_value" name="new_unit_value" /></td>
					<td><input type="text" class="invoice" name="new_invoice" /></td>
					<td><input type="text" class="cap_date" name="new_cap_date" /></td>
					<td>
						<select class="rack" name="new_rack" form="machine">
							<option value="0">None</option>
		%for rack in rack_list:
						    <option value="{{rack.id}}">{{rack.name}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="base" name="new_base" /></td>
					<td><input type="text" class="baseh" name="new_hbase" /></td>
				</tr>
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
			%for machine in machine_list:
			<tr>
				<td><a href="/machine/id/{{machine.id}}">{{machine.name}}</a></td>
				<td><a href="/model/{{machine.model.id}}">{{machine.model.name}} ({{machine.get_type_model()}})</a></td>
				<td><a href="/serial/{{machine.serial}}">{{machine.serial}}</a></td>
				<td><a href="/unit_value/{{machine.unit_value}}">{{machine.unit_value}}</a></td>
				<td><a href="/invoice/{{machine.invoice}}">{{machine.invoice}}</a></td>
				<td><a href="/cap_date/{{machine.cap_date}}">{{machine.cap_date}}</a></td>
				<td style="text-align: right"><a href="/size/{{machine.get_size()}}">{{machine.get_size()}}U</a></td>
				<td><a href="/rack/{{machine.rack_id}}"{{!'' if machine.rack.state_id == 1 else ' class="deleted"'}}>{{!machine.rack.name if machine.rack_id != 0 else 'None'}}</a></td>
				<td style="text-align: center"><a href="/rack/{{machine.rack_id}}"{{!'' if machine.rack.state_id == 1 else ' class="deleted"'}}>{{machine.get_location()}}</a></td>
			</tr>
			%end
		</table>
%end
