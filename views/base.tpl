<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd" xml:lang="en">

	<head>
		<title>{{title}} | labadmin</title>
		<link rel="stylesheet" type="text/css" href="/static/default.css" />
		<link rel="icon" type="image/png" href="/static/favicon.png" />
	</head>

	<body>
		<div id="header">
			<div style="float: right">
				<a href="/configuration"{{!' class="current"' if title == 'configuration' else ''}}>configuration</a>
				<a href="/about"{{!' class="current"' if title == 'about' else ''}}>{{info['name']}} {{info['version']}}</a>
			</div>
			<a href="/rack"{{!' class="current"' if title == 'racks' else ''}}>racks ({{info['racks']}})</a>
			<a href="/machine"{{!' class="current"' if title == 'machines' else ''}}>machines ({{info['machines']}})</a>
		</div>
{{!base}}
	</body>
</html>
