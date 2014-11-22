<%
title = 'error %s' % error.status_code
%>
% rebase('base.tpl', title = title)
		<div id="menu">
			<a href="/">{{error.status}}</a>
		</div>

		<img src="/static/error.svg" />
		<h1>{{error.status}}</h1>

