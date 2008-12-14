<%!
    from kai.model.forms import login_form
%>
<div class="yui-b content">
    <h1>Login</h1>
    
    ${login_form(action=url.current()) | n}    
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />