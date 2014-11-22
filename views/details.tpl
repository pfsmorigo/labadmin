% rebase('base.tpl', title='details')

	<h2>Machine details by {{view}} (Total: {{len(machine_list)}})</h2>
	<form method="POST" id="machine" action="/">
		<table id="details">
			<tr>
				<th>Name</th>
				<th>U Base</th>
				<th>H Base</th>
				<th>Rack</th>
				<th>Capitalization date</th>
				<th>Model</th>
				<th>Serial</th>
				<th>Unit Value</th>
				<th>Invoice</th>
			</tr>
	%for machine in machine_list:
		<tr>
			<td><input type="text" class="name" name="{{machine[0]}}_name" value="{{machine[1]}}" /></td>
			<td><input type="text" class="base" name="{{machine[0]}}_base" value="{{machine[2]}}" /></td>
			<td><input type="text" class="baseh" name="{{machine[0]}}_hbase" value="{{machine[3]}}" /></td>
			<td />
				<select class="rack" name="{{machine[0]}}_rack" form="machine">
		%for rack in rack_list:
			%if rack[0] == machine[4]:
				    <option value="{{rack[0]}}" selected="selected">{{rack[1]}}</option>
			%else:
				    <option value="{{rack[0]}}">{{rack[1]}}</option>
			%end
		%end
				    <option value="">None</option>
				</select>
			</td>
			<td><input type="text" class="cap_date" name="{{machine[0]}}_cap_date" value="{{machine[5]}}" /></td>
			<td>
				<select class="model" name="{{machine[0]}}_model" form="machine">
		%for machine_model in machine_model_list:
			%if machine_model[0] == machine[6]:
				    <option value="{{machine_model[0]}}" selected="selected">{{machine_model[1]}} ({{machine_model[2]}})</option>
			%else:
				    <option value="{{machine_model[0]}}">{{machine_model[1]}} ({{machine_model[2]}})</option>
			%end

		%end
				</select>
			</td>
			<td><input type="text" class="serial" name="{{machine[0]}}_serial" value="{{machine[7]}}" /></td>
			<td><input type="text" class="unit_value" name="{{machine[0]}}_unit_value" value="{{machine[8]}}" /></td>
			<td><input type="text" class="invoice" name="{{machine[0]}}_invoice" value="{{machine[9]}}" /></td>
		</tr>
	%end

		</table>
		<hr />
		<button type="submit">save</button>
	</form>
