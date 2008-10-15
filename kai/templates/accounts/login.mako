<div class="yui-b">
    <h1>Login</h1>
    
    <form action="${url('account_login')}" method="POST">
        ${h.auth_token_hidden_field()}
        <label for="email">Email:</label>
        <input type="text" name="email" /><br />
        
        <label for="password">Password:</label>
        <input type="password" name="password" /><br />
        
        <input type="submit" value="Login" />
    </form>
</div>
<%def name="title()">${parent.title()} - Home</%def>
<%inherit file="../layout.mako" />