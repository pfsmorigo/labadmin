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
					<th>Model</th>
					<th>Order</th>
	%for rack in rack_list:
				<tr>
					<td><input type="checkbox" name="{{rack.id}}_state_id" value="2"></td>
					<td><input type="text" class="name" name="{{rack.id}}_name" value="{{rack.name}}" /></td>

					<td>
						<select class="type_model" name="{{rack.id}}_type_model_id">
		%for rack_type_model in rack_type_model_list:
						    <option value="{{rack_type_model.id}}"{{!' selected="selected"' if rack.type_model.id == rack_type_model.id else ''}}>{{rack_type_model.get_description()}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="sort" name="{{rack.id}}_sort" value="{{rack.sort}}" /></td>
				</tr>
	%end
				<tr class="new">
					<th>New</th>
					<td><input type="text" class="name" name="new_name" value="" /></td>
					<td>
						<select class="type_model" name="{{rack.id}}_type_model_id">
		%for rack_type_model in rack_type_model_list:
						    <option value="{{rack_type_model.id}}">{{rack_type_model.get_description()}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="sort" name="new_sort" value="" /></td>
				</tr>
			</table>
			<hr />
		</form>
%end

%if rack_list.count():
		<object class="rackview" type="image/svg+xml" data="/static/rackview.svg"></object>
%else:
		<img src="/static/error.svg" />
		<div id="norack">There is not racks at all!</div>
%end
