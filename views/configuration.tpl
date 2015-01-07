% rebase('base.tpl', title='configuration')
		<div id="menu">
			<a href="/configuration/brand">brands</a>
			<a href="/configuration/rack_model">rack models</a>
			<a href="/configuration/machine_model">machine models</a>
		</div>

		<h2>{{subject}}</h2>

%for item in result:
{{item[1]}}
%end


