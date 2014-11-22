% rebase('base.tpl', title='machines')
		<div id="menu">
			<div style="float: right">
				<a href="/">done</a>
				<a href="/machine">cancel</a>
			</div>
			<a href="/machine">list</a>
			<a href="/machine/edit">edit</a>
		</div>

		<table id="machine_list">
			<tr>
				<th><a href="/machine">Machine</a></th>
				<th><a href="/machine/by/model">Model</a></th>
				<th><a href="/machine/by/serial">Serial</a></th>
				<th><a href="/machine/by/size">Size</a></th>
				<th><a href="/machine/by/rack">Rack</a></th>
			</tr>
			%for machine in machine_list[:-1]:
<% size = '{:g}'.format(float(machine[5])) %>
			<tr>
				<td><a href="/id/{{machine[0]}}">{{machine[1]}}</a></td>
				<td><a href="/model/{{machine[2]}}">{{machine[3]}} ({{machine[4]}})</a></td>
				<td><a href="/serial/{{machine[6]}}">{{machine[6]}}</a></td>
				<td style="text-align: right"><a href="/size/{{size}}">{{size}}U</a></td>
				<td><a href="/rack/{{machine[7]}}"{{!' class="deleted"' if machine[9] == 1 else ''}}>{{machine[8]}}</a></td>
			</tr>
			%end
		</table>

