<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd" xml:lang="en">

	<head>
		<title>labadmin</title>
		<link rel="stylesheet" type="text/css" href="/static/default.css">
		<link rel="icon" type="image/png" href="/static/favicon.png" />
	</head>

	<body>

	<div id="header">
		<div id="title">labadmin</div>
		<a href="/">machines</a>
	</div>

%if view == 'list':
	<object class="rackview" type="image/svg+xml" data="static/rackview.svg"></object>
	<table id="machine_list">
		<tr>
			<th>Machine</th>
			<th>Serial</th>
			<th>Rack</th>
			<th>Model</th>
		</tr>

	%for machine in machine_list:
		<tr>
			<td><a href="/id/{{machine[0]}}">{{machine[1]}}</a></td>
			<td><a href="/serial/{{machine[2]}}">{{machine[2]}}</a></td>
			<td><a href="/rack/{{machine[3]}}">{{machine[4]}}</a></td>
			<td><a href="/model/{{machine[5]}}">{{machine[6]}} ({{machine[7]}})</a></td>
		</tr>
	%end
	</table>
%else:
	<h2>Machine details by {{view}} (Total: {{len(machine_list)}})</h2>
	<form method="POST" id="machine" action="/">
		<table class="machine_details">
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
%end

		<div id="footer">
			<div id="title">labadmin</div>
			lab administration tool
		</div>
	</body>

</html>
