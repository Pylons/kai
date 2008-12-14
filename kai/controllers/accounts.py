from datetime import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import rest, secure, jsonify
from tw.mods.pylonshf import validate

from kai.lib.base import BaseController, render
from kai.lib.helpers import failure_flash, success_flash
from kai.lib.mail import EmailMessage
from kai.model import Human, forms

log = logging.getLogger(__name__)

class AccountsController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True

    @rest.dispatch_on(POST='_forgot_password')
    def forgot_password(self):
        return render('/accounts/forgot_password.mako')
    
    @validate(form=forms.forgot_password_form, error_handler='forgot_password')
    @secure.authenticate_form
    def _forgot_password(self):
        user = list(Human.by_email(self.db)[self.form_result['email_address']])[0]
        user.password_token = user.generate_token()
        c.password_token = user.password_token
        user.password_token_issue = datetime.now()
        user.store(self.db)
        message = EmailMessage(subject="PylonsHQ - Lost Password", 
                               body=render('/email/lost_password.mako'),
                               from_email="PylonsHQ <pylons@pylonshq.com>",
                               to=[self.form_result['email_address']])
        message.send(fail_silently=True)
        success_flash('An e-mail has been sent to your account to verify the password reset request.')
        redirect_to('account_login')
    
    @rest.dispatch_on(POST='_change_password')
    def change_password(self, token):
        users = list(Human.by_password_token(self.db)[token])
        if not users:
            failure_flash('That password token is no longer valid.')
            redirect_to('account_login')
        
        user = users[0]
        diff = datetime.now() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        return render('/accounts/change_password.mako')
    
    @validate(form=forms.change_password_form, error_handler='change_password')
    @secure.authenticate_form
    def _change_password(self, token):
        users = list(Human.by_password_token(self.db)[token]) or abort(401)
        user = users[0]
        diff = datetime.now() - user.password_token_issue
        if diff.days > 1 or diff.seconds > 3600:
            failure_flash('Password token is no longer valid, please make a new password reset request.')
            redirect_to('forgot_password')
        user.password_token = user.password_token_issue = None
        user.password = user.hash_password(self.form_result['password'])
        user.store(self.db)
        success_flash('Your password has been reset successfully')
        redirect_to('account_login')

    def logout(self):
        c.user.session_id = None
        c.user.store(self.db)
        session.clear()
        session.expire()
        session.save()
        success_flash('You have logged out of your session')
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_login')
    def login(self):
        return render('/accounts/login.mako')
    
    @validate(form=forms.login_form, error_handler='login')
    @secure.authenticate_form
    def _process_login(self):
        user = self.form_result['user']
        session['logged_in'] = True
        session['displayname'] = user.displayname
        session['user_id'] = user.id
        session.save()
        user.session_id = session.id
        user.store(self.db)
        success_flash('You have logged into PylonsHQ')
        redirect_to('home')
    
    @rest.dispatch_on(POST='_process_registration')
    def register(self):
        return render('/accounts/register.mako')

    @secure.authenticate_form
    @validate(form=forms.registration_form, error_handler='register')
    def _process_registration(self):
        new_user = Human(displayname=self.form_result['displayname'],
                         email=self.form_result['email'])
        new_user.password = Human.hash_password(self.form_result['password'])
        session['logged_in'] = True
        session['displayname'] = new_user.displayname
        session.save()
        new_user.session_id = session.id
        new_user.store(self.db)
        session['user_id'] = new_user.id
        success_flash("User account '%s' created successfully" %
            new_user.displayname)
        redirect_to('home')
