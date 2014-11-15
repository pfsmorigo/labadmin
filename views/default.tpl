<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd" xml:lang="en">

	<head>
		<title>labadmin</title>
		<link rel="stylesheet" type="text/css" href="/static/default.css">
	</head>

    <body>

	<h1>labadmin</h1>
	<object class="rackview" type="image/svg+xml" data="static/rackview.svg"></object>
	<table>
		<tr>
			<th>Machine</th>
			<th>Rack</th>
			<th>Description</th>
			<th>Type-Model</th>
			<th>Serial</th>
			<th>Details</th>
		</tr>

%for row in rows:
		<tr>
    %for col in row:
			<td>{{col}}</td>
    %end
			<td>[I]</td>
		</tr>
%end
	</table>

	</body>

</html>


