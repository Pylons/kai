import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form
from pylons.decorators.rest import dispatch_on

from kai.lib.base import BaseController, render
from kai.lib.helpers import success_flash
from kai.model import Human, forms

log = logging.getLogger(__name__)

class AccountsController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True

    def logout(self):
        session.clear()
        session.expire()
        session.save()
        success_flash('You have logged out of your session')
        redirect_to('home')
    
    @dispatch_on(POST='_process_login')
    def login(self):
        return render('/accounts/login.mako')
    
    @authenticate_form
    @validate(forms.LoginForm(), form='login')
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
    
    @dispatch_on(POST='_process_registration')
    def register(self):
        return render('/accounts/register.mako')

    @authenticate_form
    @validate(forms.Registration(), form='register')
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
