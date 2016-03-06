<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd" xml:lang="en">

	<head>
		<title>{{info['area']}}s | labadmin</title>
		<link rel="stylesheet" type="text/css" href="/static/default.css" />
		<link rel="icon" type="image/png" href="/static/favicon.png" />
	</head>

	<body>
		<div id="header">
			<div style="float: right">
				<a href="/configuration"{{!' class="current"' if info['area'] == 'configuration' else ''}}>configuration</a>
				<a href="/about"{{!' class="current"' if info['area'] == 'about' else ''}}>{{info['name']}} {{info['version']}}</a>
			</div>
%for area in info['areas']:
			<a href="/{{area}}"{{!' class="current"' if info['area'] == area else ''}}>{{area}}s</a>
%end
		</div>
{{!base}}
	</body>
</html>
