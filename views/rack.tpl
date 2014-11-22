% rebase('base.tpl', title='racks')
		<div id="menu">
%if view == "edit":
			<div style="float: right">
				<a href="#" onclick="document.rack.submit();">done</a>
				<a href="/rack">cancel</a>
			</div>
%end
			<a href="/rack"{{!' class="current"' if view == '' else ''}}>view</a>
			<a href="/rack/edit"{{!' class="current"' if view == 'edit' else ''}}>edit</a>
		</div>
%if view == "edit":
		<form method="POST" name="rack" action="/rack">
			<table id="details">
				<tr>
					<th>Remove</th>
					<th>Name</th>
					<th>Size</th>
					<th>Order</th>
				</tr>
	%for rack in rack_list:
				<tr{{!' class="new"' if rack[0] == 'new' else ''}}>
		%if rack[0] != 'new':
					<td><input type="checkbox" name="{{rack[0]}}_del" value="1"></td>
		%else:
					<th>New</th>
		%end
					<td><input type="text" class="name" name="{{rack[0]}}_name" value="{{rack[1]}}" /></td>
					<td><input type="text" class="size" name="{{rack[0]}}_size" value="{{rack[2]}}" /></td>
					<td><input type="text" class="sort" name="{{rack[0]}}_sort" value="{{rack[3]}}" /></td>
				</tr>
	%end
			</table>
			<hr />
		</form>
%end

%if len(rack_list) == 1:
		<img src="/static/error.svg" />
		<div id="norack">There is not racks at all!</div>
%else:
		<object class="rackview" type="image/svg+xml" data="/static/rackview.svg"></object>
%end


