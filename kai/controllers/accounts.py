import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from kai.lib.base import BaseController, render
from kai.model import Human

log = logging.getLogger(__name__)

class AccountsController(BaseController):
    def __before__(self):
        c.active_tab = True
        c.active_sub = True

    def login(self):
        return render('/accounts/login.mako')
    
    def register(self):
        return render('/accounts/register.mako')
