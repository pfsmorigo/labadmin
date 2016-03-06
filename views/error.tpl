<%
title = 'error %s' % info['error'].status_code
%>
% rebase('base.tpl', info = info)
		<div id="menu">
			<a href="/">{{info['error'].status}}</a>
		</div>

		<img src="/static/error.svg" />
		<h1>{{info['error'].status}}</h1>
