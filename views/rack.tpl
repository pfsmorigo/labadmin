% rebase('base.tpl')
		<div id="menu">
%if info['view'] == "list" or info['view'] == "brand":
			<div style="float: right">
				<a href="#" onclick="document.edit.submit();">save</a>
				<a href="/rack">cancel</a>
			</div>
%end
			<a href="/rack"{{!' class="current"' if info['view'] == '' else ''}}>visual</a>
			<a href="/rack/list"{{!' class="current"' if info['view'] == 'list' else ''}}>list</a>
			<a href="/rack/brand"{{!' class="current"' if info['view'] == 'brand' else ''}}>brands</a>
			<a href="/rack/model"{{!' class="current"' if info['view'] == 'model' else ''}}>models</a>
		</div>
%if info['view'] == "list":
		<form method="POST" name="edit" action="/rack">
			<table id="details">
				<tr>
					<th>Remove</th>
					<th>Name</th>
					<th>Model</th>
					<th>Order</th>
	%for rack in info['rack_list']:
				<tr>
					<td><input type="checkbox" name="{{rack.id}}_state_id" value="2"></td>
					<td><input type="text" class="name" name="{{rack.id}}_name" value="{{rack.name}}" /></td>

					<td>
						<select class="type_model" name="{{rack.id}}_type_model_id">
		%for rack_type_model in info['rack_type_model_list']:
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
						<select class="type_model" name="new_type_model_id">
		%for rack_type_model in info['rack_type_model_list']:
						    <option value="{{rack_type_model.id}}">{{rack_type_model.get_description()}}</option>
		%end
						</select>
					</td>
					<td><input type="text" class="sort" name="new_sort" value="" /></td>
				</tr>
			</table>
		</form>
%elif info['view'] == "brand":
		<form method="POST" name="edit" action="/rack/brand">
			<table id="details">
				<tr>
					<th>Remove</th>
					<th>Name</th>
	%for brand in info['brand_list']:
				<tr>
					<td><input type="checkbox" name="{{brand.id}}_del" value="1"></td>
					<td><input type="text" class="name" name="{{brand.id}}_name" value="{{brand.name}}" /></td>
				</tr>
	%end
				<tr class="new">
					<th>New</th>
					<td><input type="text" class="name" name="new_name" value="" /></td>
				</tr>
			</table>
		</form>
%elif info['view'] == "model":

model

%else:

	%if info['rack_list'].count():
		<object class="rackview" type="image/svg+xml" data="/static/rackview.svg"></object>
	%else:
		<img src="/static/error.svg" />
		<div id="norack">There is not racks at all!</div>
	%end
%end
