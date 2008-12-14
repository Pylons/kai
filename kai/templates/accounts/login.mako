<%!
    from kai.model.forms import login_form, openid_login_form
%>
<div class="yui-b content">
    <h1>Login</h1>
    ${login_form(action=url('account_login')) | n}
    
    <hr noshade="noshade" size="1" />
    <h1>Login with OpenID</h1>
    ${openid_login_form(action=url('openid_login')) | n}
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />