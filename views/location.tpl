% rebase('base.tpl')
		<div id="menu">
			<a href="/location"{{!' class="current"' if info['view'] == '' else ''}}>view</a>
			<a href="/location/edit"{{!' class="current"' if info['view'] == 'edit' else ''}}>edit</a>
		</div>

